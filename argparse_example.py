import math
import argparse


parser = argparse.ArgumentParser(description='Calculating volume of a cylinder')
parser.add_argument('-r', '--radius', required=True, type=int, help='Radius')
parser.add_argument('-H', '--height', required=True, type=int, help='Height')
args = parser.parse_args()
print(vars(args))

def cylinder_volume(radius, height):
    return math.pi * (radius ** 2) * height

if __name__ == '__main__':
    print(cylinder_volume(args.radius, args.height))

