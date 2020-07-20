import logging

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename='handling_files.log', level=logging.DEBUG, format=LOG_FORMAT, filemode='w')
logger_obj = logging.getLogger()

try:
    with open('users1.txt', 'r') as file_read:
        count = 0
        with open('new_users_male.txt', 'w') as file_write_male, open('new_users_female.txt', 'w') as file_write_female:
            for line in file_read:
                count += 1
                separated = line.split()
                gender = separated[len(separated) - 1]
                if gender == 'M':
                    file_write_male.write(line)
                    logger_obj.info(f"Line {count}: written Successfully")
                elif gender == 'F':
                    file_write_female.write(line)
                    logger_obj.info(f"Line {count}: written Successfully")
                else:
                    logger_obj.error(f"Line {count}: unexpected input found - {gender}")

except:
    logger_obj.critical("Expected file not found")