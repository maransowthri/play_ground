import subprocess
import logging

LOG_FORMAT = "%(levelname)s %(asctime)s - (%message)"
logging.basicConfig(filename='subprocess.log', filemode='w', format=LOG_FORMAT, level=logging.DEBUG)
logger_obj = logging.getLogger()
p1 = subprocess.run(['python', '--version'], shell=True, capture_output=True, text=True)
print(type(p1.stdout))
print(p1.stdout)