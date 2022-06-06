import json
import os
from touch import touch


def create_png_file_for_s3(file_path, min_range, max_range):
    """
    Creates png files to be used as test data
    Parameters
    ----------
    file_path : str, required
    min_range : int, required
    max_range : int, required
    """
    for index in range(min_range, max_range):
        touch("{}\\avatar-{}.png".format(file_path, str(index)))


def write_to_file(file_name, list_for_file):
    """
    Creates a file
    Parameters
    ----------
    file_name : str, required
    list_for_file : str, required
    """
    with open(file_name, "w") as filehandle:
        json.dump(list_for_file, filehandle)


def read_from_file(file_name):
    """
    Reads from file
    Parameters
    ----------
    file_name : str, required

    Returns
    -------
    Content, the array from the file
    """
    with open(file_name, 'r') as filehandle:
        list_for_file = json.load(filehandle)
        return list_for_file


def is_file_empty(file_name):
    """
    Checks if file exists and contains an empty list
    Parameters
    ----------
    file_name : str, required

    Returns
    -------
    True if file exists or has empty list, False otherwise
    """
    return os.path.isfile(file_name) or read_from_file(file_name) == []
