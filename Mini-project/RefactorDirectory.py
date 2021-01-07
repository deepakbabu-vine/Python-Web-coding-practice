# This code works only for MAC OSX

import os
import shutil
import sys
import traceback
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler
from send2trash import send2trash

path = "/users/deepak.babu/documents/"
suffices = ["ind", "ukl", "loc", "spn"]
dir_name_index = 1
config_dir_name = ".config"
rm_actual_file = ""

# is_log_only: keep_original_files combinations
# True:True  -> prints logs
# True:false -> prints logs(settings is_log_only disables the other flag)
# false:True -> creates separate file structure based on actual file structure
# false:false-> makes changes to the actual file structure
is_log_only = False
keep_original_files = False
move_under_common_directory = True
reverse_directory_structure = True
renamed_folders = {}
now = datetime.now()

# Hyphen(-) is used between Hour and Minutes
# as MAC OSX doesn't support colon(:) to be used for naming file systems.
# Only latest version support colon.
file_name = now.strftime('logs_%d_%m_%Y,%H-%M.log')
log_formatter = logging.Formatter('[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s')
log_file = "/users/deepak.babu/documents/" + file_name
rotation_handler = RotatingFileHandler(log_file, mode='a', maxBytes=5 * 1024 * 1024, backupCount=2, encoding=None,
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
        if f == sub_dir_name or f == config_dir_name:
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
        if f == config_dir_name:
            continue
        if f.endswith(".properties"):
            if not check_dir_exists(".config"):
                os.makedirs(new_file_path + "/" + directory_name + "/" + config_dir_name)
            shutil.copy(target_file_path + "/" + f,
                        new_file_path + "/" + directory_name + "/" + config_dir_name + "/" + f)
            continue
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


def new_directory_name(files, target_dir, path):
    dir_index = 1
    append_file_name = target_dir + "_" + files
    excepted_dir_name = append_file_name
    while True:
        if check_dir_exists(path + append_file_name):
            append_file_name = target_dir + "_" + files
            append_file_name = append_file_name + "(" + str(dir_index) + ")"
            dir_index += 1
        else:
            if not excepted_dir_name == append_file_name:
                logger.info("(%s) has been renamed to (%s) due to duplicate exists", excepted_dir_name,
                            append_file_name)
            return append_file_name


def create_new_dir(dir_name, path):
    try:
        os.mkdir(path + dir_name)
        return True
    except (OSError, IOError):
        traceback.print_exc()
        logger.exception("Failed to create the directory")
        return False


def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)


def check_latest_dir_available(check_latest_dir):
    index_appender = 1
    while True:
        temp_dir_name = check_latest_dir + "(" + str(index_appender) + ")"
        if check_dir_exists(path + "/" + temp_dir_name):
            index_appender += 1
        else:
            if index_appender >=2:
                temp_dir_name = check_latest_dir + "(" + str(index_appender - 1) + ")"
                return temp_dir_name
            else:
                return check_latest_dir


def verify_before_removing_dir(args_path, args_target_dir):
    count_missing_file = 0
    if not check_dir_exists(args_path + "/" + args_target_dir):
        print "Directory Not found!"
        print "---------"
        sys.exit(0)
    for root_path, current_dir, check_file in os.walk(args_path + "/" + args_target_dir):
        for f in check_file:
            if f == ".DS_Store":
                continue
            extract_dir_name = root_path.partition(args_target_dir)[2]
            if extract_dir_name[0] == '/':
                extract_dir_name = extract_dir_name[1:]
            create_dir_name = args_target_dir + "_" + extract_dir_name
            create_dir_name = check_latest_dir_available(create_dir_name)
            target_file_path = path + "/" + create_dir_name + "/" + f
            if os.path.isfile(target_file_path):
                continue
            else:
                count_missing_file += 1
                print colored(255, 0, 0, "file (" + target_file_path + ") is missing!")
                print "Do you want to add this file :y/n"
                while True:
                    add_file = raw_input()
                    if add_file == 'y':
                        while True:
                            try:
                                shutil.copyfile(root_path + "/" + f, target_file_path)
                                print "File added"
                                if not count_missing_file == 0:
                                    count_missing_file -= 1
                                break
                            except IOError:
                                os.mkdir(path + "/" + create_dir_name)
                        break
                    elif add_file == 'n':
                        print "Skipped!!!"
                        break
                    else:
                        print "Invalid input, enter y/n"
    return not bool(count_missing_file)


def get_user_input():
    while True:
        user_input = raw_input()
        if user_input == 'y':
            return True
        elif user_input == 'n':
            return False
        else:
            print "Invalid input, enter y/n"


if __name__ == "__main__":
    if not reverse_directory_structure:
        for root, dirs, dir_inside_main_dir in os.walk(path):
            for directory in dirs:
                for index in range(len(suffices)):
                    if (directory.rfind(suffices[index])) > 0:
                        try:
                            new_dir_name = directory.rstrip(suffices[index]).rstrip("_")
                            if is_log_only:
                                new_available_name = check_and_add_pairs_to_map(root, directory, new_dir_name,
                                                                                dir_name_index)
                                print "(", root + directory, ")", "will be renamed to ", "(", new_available_name, ")"
                                logger.debug("(%s) will be renamed to (%s)", root + directory, new_available_name)
                            elif move_under_common_directory:
                                try:
                                    if not check_dir_exists(path + new_dir_name):
                                        os.mkdir(path + new_dir_name)
                                except OSError:
                                    traceback.print_exc()
                                    logger.exception("Exception occurred:")
                                if move_files_under_common_directory(path + new_dir_name, path + directory,
                                                                     suffices[index]):
                                    print "Moved under a common directory!"
                                    if rm_actual_file == 's':
                                        break
                                    if not rm_actual_file == 'a':
                                        print "Do you want to remove this (" + path + directory + ") directory, y/n?"
                                        print "Remove all folders from here - a"
                                        print "Skip all folders from here - s"
                                        rm_actual_file = raw_input("Enter your choice: ")
                                        if rm_actual_file == "y":
                                            shutil.rmtree(path + directory)
                                            rm_actual_file = ""
                                        elif rm_actual_file == "a":
                                            shutil.rmtree(path + directory)
                                        elif rm_actual_file == "s":
                                            pass
                                        else:
                                            rm_actual_file = ""
                                    else:
                                        shutil.rmtree(path + directory)
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
    else:
        delete_main_directory = True
        if delete_main_directory:
            print "provide the directory to be deleted?"
            target_dir = raw_input()
            print "This verification process does not verify the contents of any file"
            print "Checks only the existence of files & directories in the base path"
            print "Make sure you have splitted the common directory"
            print "---------"
            print "Checking..."
            if verify_before_removing_dir(path, target_dir):
                print "Safe to delete!!!"
                print "---------"
                print "Confirm to delete? y/n"
                if get_user_input():
                    shutil.make_archive(path + target_dir, 'zip', path + "/" + target_dir)
                    send2trash(path + "/" + target_dir)
                    print "Directory moved to Trash & Zip file created."
                else:
                    print "Deletion Aborted!"
            else:
                print colored(255, 0, 0, "Files are missing...")
                print "Do you still want to delete it? y/n"
                force_delete = raw_input()
                if force_delete == 'y':
                    send2trash(path + target_dir)
                    print colored(255, 0, 0, "Files Deleted!!!")
                elif force_delete == 'n':
                    print colored(34, 139, 34, "Files not deleted.")

        else:
            print "Provide the directory to be split?"
            target_dir = raw_input()
            if target_dir == "":
                print "Name cannot be empty"
            elif check_dir_exists(path + target_dir):
                destination_path = path + target_dir
                list_subdir_in_dir = os.listdir(destination_path)
                for dir_inside_main_dir in list_subdir_in_dir:
                    if dir_inside_main_dir == ".DS_Store":
                        continue
                    dir_name = new_directory_name(dir_inside_main_dir, target_dir, path)
                    if create_new_dir(dir_name, path):
                        list_files_in_subdir = os.listdir(destination_path + "/" + dir_inside_main_dir)
                        for files_inside_subdir in list_files_in_subdir:
                            try:
                                if os.path.isdir(
                                        destination_path + "/" + dir_inside_main_dir + "/" + files_inside_subdir):
                                    shutil.copytree(
                                        destination_path + "/" + dir_inside_main_dir + "/" + files_inside_subdir,
                                        path + dir_name + "/" + files_inside_subdir, False, None)
                                else:
                                    shutil.copyfile(
                                        destination_path + "/" + dir_inside_main_dir + "/" + files_inside_subdir,
                                        path + dir_name + "/" + files_inside_subdir)
                            except (OSError, IOError):
                                traceback.print_exc()
                                logger.exception("Failed to copy files")
                    print "Files moved Successfully!!!"
            else:
                print "Directory does not exists!!!"
