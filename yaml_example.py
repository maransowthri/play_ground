import yaml

def yaml_loader(file_path):
    with open(file_path, 'r') as yaml_line:
        data = yaml.load(yaml_line, Loader=yaml.FullLoader)
    return data

def yaml_dump(file_path, data):
    with open(file_path, 'w') as yaml_line:
        yaml.dump(data, yaml_line)

data = yaml_loader('sample.yaml')
yaml_dump('output.yaml', data)