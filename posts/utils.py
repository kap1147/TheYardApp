from os import path
from random import randint

# get file name extention (jpg, png and etc)
def get_filename_ext(filepath):
    base_name = path.basename(filepath)
    name, ext = path.splitext(base_name)
    return name, ext

# rename file to random integer
def upload_image_path(instance, filename):
    new_filename = randint(1, 2348392030)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "post/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
        )

