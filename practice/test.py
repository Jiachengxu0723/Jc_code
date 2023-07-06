import os
import shutil

def get_file_list(directory, types , is_sort = True):
    r"""
    Get the list of all files names with certain types in a directory
    Args:
        directory(string): the directory that contains all files
        types(List[str]):
        is_sort:
    Returns:
        file_list(List[str]): List of all the required files
    """
    file_list = []
    for path, dirs, files in os.walk(directory):
        for file in files:
            if os.path.splitext(file)[1] in types:
                file_list.append(os.path.join(path, file))
    if is_sort:
        file_list.sort()
    return file_list

def main():
    dat_file = get_file_list(directory='/home/synsense/下载/imu',types='[.dat]')
    new_path = '/home/synsense/下载/imu/person011/'
    shutil.copy(dat_file,new_path)


if __name__ == '__main__':
    main()

