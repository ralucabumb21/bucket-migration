import json
import os
from touch import touch


def create_png_file_for_s3(file_path, min_range, max_range):
    for index in range(min_range, max_range):
        touch("{}\\avatar-{}.png".format(file_path, str(index)))


def write_to_file(file_name, list_for_file):
    with open(file_name, "w") as filehandle:
        json.dump(list_for_file, filehandle)


def read_from_file(file_name):
    with open(file_name, 'r') as filehandle:
        list_for_file = json.load(filehandle)
        return list_for_file


def is_file_empty(file_name):
    # Check if file exist and it is empty
    return os.path.isfile(file_name) or read_from_file(file_name) == []
