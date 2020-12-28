# This code works only for MAC OS X

import os
import traceback
import logging


logging.basicConfig(
     filename='log_file_name.log',
     level=logging.INFO,
     format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
     datefmt='%H:%M:%S'
 )
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
logger = logging.getLogger(__name__)

path = "/users/deepak.babu/documents/"
suffices = ["ind", "ukl", "loc", "spn"]
dir_name_index = 1


def check_dir_exists(new_dir):
    return os.path.exists(new_dir)


def append_num_to_dirname(dir_name, index):
    while True:
        temp_dir_name = dir_name + "(" + str(index) + ")"
        if check_dir_exists(temp_dir_name):
            index += 1
            continue
        else:
            return temp_dir_name, index + 1


def move_to_config(dir_path, f):
    config_dir_name = ".config"
    if not check_dir_exists(dir_path + "/" + config_dir_name):
        os.mkdir(dir_path + "/" + config_dir_name)
    try:
        os.rename(dir_path + "/" + f, dir_path + "/" + config_dir_name + "/" + f)
    except OSError:
        traceback.print_exc()
        logger.exception(traceback.print_exc())
        return


def move_file_collection(dir_path, sub_dir_name):
    list_files = os.listdir(dir_path)
    for f in list_files:
        if f == sub_dir_name or f == ".config":
            continue
        if f.endswith(".properties"):
            move_to_config(dir_path, f)
            continue
        existing_file = dir_path + "/" + f
        new_file = dir_path + "/" + sub_dir_name + "/" + f
        try:
            os.rename(existing_file, new_file)
        except OSError:
            traceback.print_exc()
            logger.exception(traceback.print_exc())
            return False
    return True


for root, dirs, files in os.walk(path):
    for d in dirs:
        for i in range(len(suffices)):
            if (d.rfind(suffices[i])) > 0:
                try:
                    existing_dir_path = path + d
                    new_dir_name = d.rstrip(suffices[i]).rstrip("_")
                    new_dir_path = path + new_dir_name
                    if check_dir_exists(new_dir_path):
                        new_dir_path, dir_name_index = append_num_to_dirname(new_dir_path, dir_name_index)
                    os.rename(existing_dir_path, new_dir_path)
                    subdir_path = new_dir_path + "/" + suffices[i]
                    if not check_dir_exists(subdir_path):
                        os.mkdir(subdir_path)
                    if move_file_collection(new_dir_path, suffices[i]):
                        print("Moved files!!!")
                    else:
                        print("Failed to move files!!!")
                    break
                except OSError:
                    traceback.print_exc()
                    logger.exception(traceback.print_exc())
dir_name_index = 1
