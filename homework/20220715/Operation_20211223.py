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

def parse_filename(filepath):
    r"""
    Parse the info contained in the file path.
    Args:
        filename(string):file path of the data bin file.
    Returns:
        Parsed attributes from the filename.
    """
    filepath, suffix = os.path.splitext(filepath)
    name, light_level, position, label = filepath.split('/')[-4:]
    label = label.split('_')[-1]
    return name, light_level, position, label

def filter_file_list(file_list,  lights = [], positions=[], names=[], labels=[]):
    r"""
    Filter the file path list by the attributes requirements.
    Args:
        file_list(List[str]): List of the files' file path.
        lights(List[str]): An attribute of file name. Light intensities of data.
        positions(List[str]): An attribute of file name. Camera positions of data.
        names(List[str]): An attribute of file name. Actor names of data.
        labels(List[str]): An attribute of file name. Labels of data.
    Returns:
        file_list[List[str]]: Filtered file path List by the attributes requirements.
    """
    #print(list(filter(lambda x: filter_by_attributes(x, lights, positions, names, labels), file_list)))
    return list(filter(lambda x: filter_by_attributes(x, lights=['l01','l02','l04'],labels=['attentive']), file_list))

def filter_by_attributes(filename, lights = [], positions=[], names=[], labels=[]):
    r"""
        Check if the file path meets the attributs requirements.
        Args:
            filename(string): file path of the data file.
            lights(List[str]): An attribute of file name. Light intensities of data.
            positions(List[str]): An attribute of file name. Camera positions of data.
            names(List[str]): An attribute of file name. Actor names of data.
            labels(List[str]): An attribute of file name. Labels of data.
        Returns:
            result(bool): Is the file path meets the attributs requirements.
        """
    name, light_level, position, label = parse_filename(filename)
    if lights:
        if light_level not in lights:
            return False
    if positions:
        if position not in positions:
            return False
    if names:
        if name not in names:
            return False
    if labels:
        if label not in labels:
            return False
    return True

def main():
    """
        1.Directory structure from name/light_ level/position/*. Bin is modified to name/position/light_ level/*. Bin refers to the sequence of light level and position
        2.Only L01, L02, L04 (not L03) are reserved for light intensity
        3.Only retain the attention of the file Bin (do not inattentive.bin and drinking.bin)

        Args:
            old_path_list(list):File path list after filtering illumination and labels

            date(string):First level directory name of the new file

    """
    file_list = get_file_list(directory = '20211223' ,types = ['.bin'])
    old_path_list = filter_file_list(file_list,lights=['l01','l02','l04'],labels=['attentive'])

    date = 'new_20211223'
    for old_path in old_path_list:
        name, light_level, position, label = parse_filename(old_path)
        new_path =  date + '/' + name + '/' + position + '/' + light_level
        print(new_path)
        print(old_path)
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        shutil.copy(old_path,new_path)

if __name__ == '__main__':
    main()

