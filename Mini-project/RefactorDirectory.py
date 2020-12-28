# This code works only for MAC OSX

import os
import traceback
import logging


logging.basicConfig(
     filename='refactor_folder_log.log',
     level=logging.DEBUG,
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
    """
    Checks if the directory already exists in the specified path

    :param new_dir: Directory path
    :return: True, if directory exists
    """
    if os.path.exists(new_dir):
        logger.debug("%s Directory already exists", new_dir + ":")
        return True
    else:
        return False


def append_num_to_dirname(dir_name, dir_num_suffix):
    """
    Appends a numberic value to the directory name if duplicate exists

    :param dir_name: Gets the directory name
    :param dir_num_suffix: Gets the numberic value to be assigned
    :return: New directory name, next numberic value for a given directory
    """
    while True:
        temp_dir_name = dir_name + "(" + str(dir_num_suffix) + ")"
        if check_dir_exists(temp_dir_name):
            dir_num_suffix += 1
            continue
        else:
            return temp_dir_name, dir_num_suffix + 1


def move_to_config(dir_path, f):
    """
    Moves properties file to hidden folder config

    :param dir_path: Gets the basepath of the properties file.
    :param f: Gets the properties file
    """
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
    """
    Moves all files except properties file into the sub-directory created using the
    base directory suffix.

    :param dir_path: Gets the path of the directory
    :param sub_dir_name: Gets the suffix name of the directory
    """
    list_files = os.listdir(dir_path)
    for f in list_files:
        if f == sub_dir_name or f == ".config":
            continue
        if f.endswith(".properties"):
            move_to_config(dir_path, f)
            continue
        existing_filepath = dir_path + "/" + f
        new_filepath = dir_path + "/" + sub_dir_name + "/" + f
        try:
            os.rename(existing_filepath, new_filepath)
        except OSError:
            traceback.print_exc()
            logger.exception("Failed to move files!!!")
            return False
    return True


if __name__ == "__main__":
    for root, dirs, files in os.walk(path):
        for directory in dirs:
            for index in range(len(suffices)):
                if (directory.rfind(suffices[index])) > 0:
                    try:
                        existing_dir_path = path + directory
                        new_dir_name = directory.rstrip(suffices[index]).rstrip("_")
                        new_dir_path = path + new_dir_name
                        if check_dir_exists(new_dir_path):
                            new_dir_path, dir_name_index = append_num_to_dirname(new_dir_path, dir_name_index)
                        os.rename(existing_dir_path, new_dir_path)
                        subdir_path = new_dir_path + "/" + suffices[index]
                        if not check_dir_exists(subdir_path):
                            os.mkdir(subdir_path)
                        if move_file_collection(new_dir_path, suffices[index]):
                            print("Moved files successfully!!!")
                        break
                    except OSError:
                        traceback.print_exc()
                        logger.exception("Exception occurred:")
    dir_name_index = 1
