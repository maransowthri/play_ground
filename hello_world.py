import sys
import argparse


parser = argparse.ArgumentParser(description='Customized Stacker commands')
parser.add_argument('action', help='Set action as build / destroy')
parser.add_argument('-e', '--environment', required=True, type=str, metavar='', help="Choose environment name as --environment dev/prod")
parser.add_argument('-p', '--product', required=True, type=str, metavar='', help="Choose product name as --product deploy/staging ")
parser.add_argument('--prefix', required=True, type=str, metavar='', help="Choose namespace as --namespace yourname-env ")
parser.add_argument('--all', action='store_true', help='Set this to build / destroy all existing stacks')
parser.add_argument('-c', '--components', nargs='+', help='e.g --components loadbalancer iam jenkins')
args = parser.parse_args()

[sys.argv.pop() for _ in range(1, len(sys.argv))]
build_stack(args.environment, args.product, args.prefix, args.action, args.all, args.components)

