# This code works only for MAC OSX

import os
import shutil
import traceback
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler

path = "/users/deepak.babu/documents/"
suffices = ["ind", "ukl", "loc", "spn"]
dir_name_index = 1
is_log_only = False
keep_original_files = True
renamed_folders = {}
now = datetime.now()
file_name = now.strftime('logs_%d_%m_%Y,%H-%M.log')

log_formatter = logging.Formatter('[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s')
log_file = "/users/deepak.babu/documents/" + file_name
rotation_handler = RotatingFileHandler(log_file, mode='a', maxBytes=5*1024*1024,backupCount=2, encoding=None,
                                       delay=False)
rotation_handler.setFormatter(log_formatter)
rotation_handler.setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(rotation_handler)


def check_dirname_exists_in_map(the_d):
    if the_d in renamed_folders.values():
        return True
    else:
        if check_dir_exists(the_d):
            return True
        return False


def check_dir_exists(new_dir):
    """
    Checks if the directory already exists in the specified path

    :param new_dir: Directory path
    :return: True, if directory exists
    """
    if os.path.exists(new_dir):
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


def check_and_add_pairs_to_map(root_path, the_dir_path, the_striped_dir_name, the_index_appender_value):
    if check_dirname_exists_in_map(root_path + the_striped_dir_name):
        while True:
            temp_name = root_path + the_striped_dir_name + "(" + str(the_index_appender_value) + ")"
            if check_dirname_exists_in_map(temp_name):
                the_index_appender_value += 1
                continue
            else:
                renamed_folders[root_path + the_dir_path] = temp_name
                return temp_name
    else:
        renamed_folders[root_path + the_dir_path] = root_path + the_striped_dir_name
        return root_path + the_striped_dir_name


def move_file_collection(new_backup_path,dir_path, sub_dir_name):
    """
    Moves all files except properties file into the sub-directory created using the
    base directory suffix.

    :param dir_path: Gets the path of the directory
    :param sub_dir_name: Gets the suffix name of the directory
    """
    list_files = os.listdir(dir_path)
    if not keep_original_files:
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
    else:
        for f in list_files:
            existing_filepath = dir_path + "/" + f
            new_filepath = new_backup_path + "/" + sub_dir_name + "/" + f
            try:
                shutil.copy(existing_filepath, new_filepath)
                print "Copied files to new path"
            except OSError:
                logger.exception("Failed to copy files!!!")
                traceback.print_exc()
                return False
        return True


if __name__ == "__main__":
    for root, dirs, files in os.walk(path):
        for directory in dirs:
            for index in range(len(suffices)):
                if (directory.rfind(suffices[index])) > 0:
                    try:
                        new_dir_name = directory.rstrip(suffices[index]).rstrip("_")
                        if is_log_only:
                            new_available_name = check_and_add_pairs_to_map(root, directory, new_dir_name,
                                                                            dir_name_index)
                            print "(", root + directory, ")", "will be renamed to ", "(", new_available_name, ")"
                            logger.debug("(%s) will be renamed to (%s)", root+directory, new_available_name)
                        else:
                            existing_dir_path = path + directory
                            new_dir_path = path + new_dir_name
                            if check_dir_exists(new_dir_path):
                                new_dir_path, dir_name_index = append_num_to_dirname(new_dir_path, dir_name_index)
                            if keep_original_files:
                                os.mkdir(new_dir_path)
                                subdir_path = new_dir_path + "/" + suffices[index]
                                if not check_dir_exists(subdir_path):
                                    os.mkdir(subdir_path)
                                if move_file_collection(new_dir_path, existing_dir_path, suffices[index]):
                                    print("Moved files successfully!!!")
                                break
                            else:
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
