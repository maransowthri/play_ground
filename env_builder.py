#!/usr/bin/python

import argparse
import configparser
import copy
import os
import re
import shutil
import textwrap
import yaml

global args_dict
args_dict = {
    'watchdog': False
}


### HELPER FUNCTIONS ###

def _merge_helper(a, b):
    """
    Recursively merges b into a for any mapping/list objects therein.
    Scalar leaves get overwritten with values from 'b' if different.
    Any keys in 'b' prefixed with the char '=' will force an overwrite into 'a' using the value of that key (with the '=' removed) from 'b'.
    """
    for key in b:
        # Check if config wants us to overwrite this key instead of merge
        origkey = key
        overwrite = False
        if key.startswith('='):
            overwrite = True
            key = key[1:]

        if key in a:
            if overwrite:
                a[key] = b[origkey]
            elif isinstance(a[key], dict) and isinstance(b[key], dict):
                _merge_helper(a[key], b[key])
            elif isinstance(a[key], list) and isinstance(b[key], list):
                a[key].extend(b[key])

                dicts = [d for d in a[key] if isinstance(d, dict)]
                # There is no super-easy way to get a unique list of dictionaries, without
                # recursing and doing all sorts of weird stuff. Skipping that for now
                if not dicts:
                    unique_values = set(a[key])
                    a[key] = list(unique_values)
                    a[key].sort()
            elif a[key] == b[key]:
                pass  # same scalar leaf value
            else:
                # In a scalar conflict we want to override with the value from the second dict
                a[key] = b[key]
        else:
            a[key] = b[key]
    return a


def process_vault(text):
    # We hid these tags from the initail YAML parse by quoting the values.
    # Unquote them to expose the tags to Ansible's parser.
    text = re.sub(r"'(!vault.*?)'", r"\1", text, flags=re.DOTALL)
    # Remove the double newlines we used in the master conf to force yaml.dump
    # to not collapse our first two vault lines into one.
    text = text.replace("\n\n", "\n")
    return text


def merge(loader, node):
    merge_data = loader.construct_mapping(node, deep=True)
    merge_base = merge_data['BASE']
    merge_update = merge_data['UPDATE']
    merged = _merge_helper(copy.deepcopy(merge_base), copy.deepcopy(merge_update))
    return merged


def watchdog(loader, node):
    seq = loader.construct_sequence(node)
    if args_dict['watchdog']:
        return seq[0]
    else:
        return seq[1]


def output(config, path, base=True):
    if base:
        if os.path.isdir(path):
            shutil.rmtree(path)
        os.makedirs(path)

    for key in config.keys():
        if key.startswith('~'):
            base_key = key[1:]
            new_path = path + '/' + base_key
            os.mkdir(new_path)
            output(config[key], new_path, base=False)
        else:
            val = yaml.dump(config[key], default_flow_style=False)
            val = val.replace("\n...", "").strip()  # Get rid of the YAML document separator
            val = process_vault(val)

            with open(path + '/vars.yaml', 'a') as f:
                if isinstance(config[key], list) or isinstance(config[key], dict):
                    val = textwrap.indent(val, '  ')
                    f.write(f"{key}: \n" + val + "\n")
                else:
                    f.write(f"{key}: {val}\n")


def set_arg(name, val):
    global args_dict
    args_dict[name] = val


def overlay_config(base, overlay):
    for section in overlay.sections():
        if not base.has_section(section):
            base.add_section(section)
        for key, value in overlay.items(section):
            base.set(section, key, value)
    return base


def add_ara_plugins(config):
    callbacks = ''
    try:
        callbacks = config.get('defaults', 'callback_plugins')
        callbacks = callbacks + ':'
    except configparser.NoOptionError:
        # Key wasn't present. We'll just proceed on to adding the value directly to the empty base.
        pass

    callbacks = callbacks + '~/ansible/lib/python3.6/site-packages/ara/plugins/callback'
    config.set('defaults', 'callback_plugins', callbacks)
    return config


### CORE LOGIC ###

def main():
    parser = argparse.ArgumentParser(
        description='Create the folder/file structure to pre-define facts for the given Ansible env')

    # Named args
    parser.add_argument('-a', '--ara', default='yes', choices=['yes', 'no'], help='')
    parser.add_argument('-c', '--config_root', default='env_config',
                        help='the path where environment config source data is stored')
    parser.add_argument('-o', '--output_dir', default='environments',
                        help='configure the root filepath this builder will output files into')
    parser.add_argument('-v', '--view', action='store_true', default=False,
                        help='also prints the compiled YAML to terminal at end of run')
    parser.add_argument('--watchdog', action='store_true', default=False,
                        help='generate the env spec with watchdog-specific notification parameters')
    parser.add_argument('-w', '--write', action='store_true', default=False,
                        help='writes the compiled YAML to disk for Ansible to consume')

    # Positional args
    parser.add_argument('env', help='the name of the env to generate')

    args = parser.parse_args()

    args_keyval = vars(args)
    for key in args_keyval.keys():
        set_arg(key, args_keyval[key])

    # Compile YAML for inventory fact configuration

    yaml.add_constructor('!merge', merge, Loader=yaml.SafeLoader)
    yaml.add_constructor('!watchdog', watchdog, Loader=yaml.SafeLoader)

    contents = ''
    with open(args.config_root + '/env_master.yaml', 'r') as f:
        contents = f.read()

    master_config = yaml.load(contents, Loader=yaml.SafeLoader)
    env_config = master_config[args.env]

    # Compile CFG file for Ansible configuration

    config = configparser.ConfigParser()
    config.read(args.config_root + '/ansible_config/_global.cfg')

    env_config_path = args.config_root + '/ansible_config/' + args.env + '.cfg'
    if os.path.exists(env_config_path):
        env_ansible_config = configparser.ConfigParser()
        env_ansible_config.read(env_config_path)

        config = overlay_config(config, env_ansible_config)

    if args.ara == 'yes':
        config = add_ara_plugins(config)

        ara_config = configparser.ConfigParser()
        ara_config.read(args.config_root + '/ansible_config/_ara.cfg')

        config = overlay_config(config, ara_config)

    # Output compiled data to terminal and/or filesystem

    if args.view:
        print('')
        print('### /environments/ '.ljust(100, '#') + "\n")
        print(yaml.dump(env_config))

        print('')
        print('### ansible.cfg '.ljust(100, '#') + "\n")
        for section in config._sections.keys():
            print(f'[{section}]')
            for key, value in config._sections[section].items():
                print(f'{key} = {value}')
            print('')

    if args.write:
        if not os.path.isdir(args.output_dir):
            os.makedirs(args.output_dir)
        output(env_config, args.output_dir)
        shutil.copyfile(args.config_root + '/inventory_plugin_config/' + args.env + '.yaml',
                        args.output_dir + '/athenanet.yaml')

        with open(args.output_dir + '/../ansible.cfg', 'w') as ansible_cfg:
            config.write(ansible_cfg)


if __name__ == '__main__':
    main()
