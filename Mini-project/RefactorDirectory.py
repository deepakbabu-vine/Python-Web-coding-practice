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

# is_log_only: keep_original_files combinations
# True:True  -> prints logs
# True:false -> prints logs(settings is_log_only disables the other flag)
# false:True -> creates separate file structure based on actual file structure
# false:false-> makes changes to the actual file structure
is_log_only = False
keep_original_files = False
move_under_common_directory = True
renamed_folders = {}
now = datetime.now()


# Hyphen(-) is used between Hour and Minutes
# as MAC OSX doesn't support colon(:) to be used for naming file systems.
# Only latest version support colon.
file_name = now.strftime('logs_%d_%m_%Y,%H-%M.log')
log_formatter = logging.Formatter('[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s')
log_file = "/users/deepak.babu/documents/" + file_name
rotation_handler = RotatingFileHandler(log_file, mode='a', maxBytes=5*1024*1024, backupCount=2, encoding=None,
                                       delay=True)
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


def move_to_config(dir_path, f, separate_path):
    """
    Moves properties file to config folder which is hidden in MAC OSX.

    :param separate_path: Gets the path of the separate directory
    :param dir_path: Gets the basepath of the properties file.
    :param f: Gets the properties file
    """
    config_dir_name = ".config"
    if not keep_original_files:
        if not check_dir_exists(dir_path + "/" + config_dir_name):
            os.mkdir(dir_path + "/" + config_dir_name)
    else:
        if not check_dir_exists(separate_path + "/" + config_dir_name):
            os.mkdir(separate_path + "/" + config_dir_name)
    try:
        if not keep_original_files:
            os.rename(dir_path + "/" + f, dir_path + "/" + config_dir_name + "/" + f)
            return
        else:
            shutil.copy(dir_path + "/" + f, separate_path + "/" + config_dir_name + "/" + f)
            return
    except OSError:
        traceback.print_exc()
        logger.exception(traceback.print_exc())
        return


def check_and_add_pairs_to_map(root_path, the_dir_path, the_striped_dir_name, the_index_appender_value):
    """
    Uses dictionaries to keep track of the renamed folder without actually renaming the folders.

    :param root_path:
    :param the_dir_path:
    :param the_striped_dir_name:
    :param the_index_appender_value:
    :return: returns a path with a new name for the directory.
    """
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


def move_file_collection(new_separate_path, dir_path, sub_dir_name):
    """
    Moves all files except properties file into the sub-directory created using the
    base directory suffix.

    :param dir_path: Gets the path of the directory
    :param sub_dir_name: Gets the suffix name of the directory
    :param new_separate_path: Gets the path of the alternate directory
    """
    list_files = os.listdir(dir_path)
    new_filepath = ""
    separate_dir_path = ""
    for f in list_files:
        if f == sub_dir_name or f == ".config":
            continue
        if f.endswith(".properties"):
            move_to_config(dir_path, f, new_separate_path)
            continue
        existing_filepath = dir_path + "/" + f
        if not keep_original_files:
            new_filepath = dir_path + "/" + sub_dir_name + "/" + f
        else:
            separate_dir_path = new_separate_path + "/" + sub_dir_name + "/" + f
        try:
            if keep_original_files:
                if not os.path.isdir(existing_filepath):
                    shutil.copy(existing_filepath, separate_dir_path)
                else:
                    shutil.copytree(existing_filepath, separate_dir_path)
            else:
                os.rename(existing_filepath, new_filepath)
        except OSError:
            traceback.print_exc()
            logger.exception("Failed to move files!!!")
            return False
    return True


def move_files_under_common_directory(new_file_path, target_file_path, directory_name):
    try:
        if not check_dir_exists(new_file_path + "/" + directory_name):
            os.makedirs(new_file_path + "/" + directory_name)
        else:
            return False
    except OSError:
        traceback.print_exc()
        logger.exception("Exception occurred:")
    list_files = os.listdir(target_file_path)
    for f in list_files:
        try:
            if os.path.isdir(target_file_path + "/" + f):
                shutil.copytree(target_file_path + "/" + f, new_file_path + "/" + directory_name + "/" + f, False, None)
            else:
                shutil.copyfile(target_file_path + "/" + f, new_file_path + "/" + directory_name + "/" + f)
        except (OSError, IOError):
            traceback.print_exc()
            logger.exception("Exception occurred:")
            continue
        except:
            traceback.print_exc()
            logger.exception("Exception occurred:")
            continue
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
                        elif move_under_common_directory:
                            try:
                                if not check_dir_exists(path + new_dir_name):
                                    os.mkdir(path + new_dir_name)
                            except OSError:
                                traceback.print_exc()
                                logger.exception("Exception occurred:")
                            if move_files_under_common_directory(path + new_dir_name, path + directory, suffices[index]):
                                print "Moved under a common directory!"
                            break
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
                                    print "Moved files successfully!!!"
                                break
                            else:
                                os.rename(existing_dir_path, new_dir_path)
                                subdir_path = new_dir_path + "/" + suffices[index]
                                if not check_dir_exists(subdir_path):
                                    os.mkdir(subdir_path)
                                if move_file_collection("", new_dir_path, suffices[index]):
                                    print "Moved files successfully!!!"
                                else:
                                    print "Directory already exists"
                                break
                    except OSError:
                        traceback.print_exc()
                        logger.exception("Exception occurred:")
    if is_log_only:
        print "Note: Setting (is_log_only)flag to True disables the flag(keep_original_files)"
        logger.info("Note: Setting (is_log_only)flag to True disables the flag(keep_original_files)")
