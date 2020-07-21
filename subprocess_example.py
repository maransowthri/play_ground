import subprocess
import logging

p1 = subprocess.run(['python', '--version'], shell=True, capture_output=True, text=True)
print(type(p1.stdout))
print(p1.stdout)