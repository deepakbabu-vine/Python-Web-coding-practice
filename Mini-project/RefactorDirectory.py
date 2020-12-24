import os
import traceback

path = "/users/deepak.babu/documents/"
suffices = ["ind", "ukl", "loc", "spn"]
dir_name_index = 1


def check_dir_exists(new_dir):
    return os.path.exists(new_dir)


def append_num_to_dirname(dir_name, index):
    # TODO: index will always start from 0, should start from the last modified value.
    while True:
        temp_dir_name = dir_name + "(" + str(index) + ")"
        if check_dir_exists(temp_dir_name):
            index += 1
            continue
        else:
            return temp_dir_name


def move_file_collection(dir_path, sub_dir_name):
    list_files = os.listdir(dir_path)
    for f in list_files :
        if f == sub_dir_name:
            continue
        existing_file = dir_path + "/" + f
        new_file = dir_path + "/" + sub_dir_name + "/" + f
        try:
            os.rename(existing_file, new_file)
        except OSError:
            traceback.print_exc()
            return False
    return True


for root, dirs, files in os.walk(path):
    for d in dirs:
        for i in range(len(suffices)):
            if (d.rfind(suffices[i])) > 0:
                try:
                    print(d)
                    existing_dir_path = path + d
                    new_dir_name = d.rstrip(suffices[i]).rstrip("_")
                    new_dir_path = path + new_dir_name
                    if check_dir_exists(new_dir_path):
                        new_dir_path = append_num_to_dirname(new_dir_path, dir_name_index)
                    print "existing:", existing_dir_path
                    print "new file:", new_dir_path
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
