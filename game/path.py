"""
path.py
This module provides:
- `get_img_folder_path()`: a method to receive the absolute path of the image folder.
"""

import os


def get_img_folder_path():
    """
    Determines the absolute path to the img folder.

    Returns:
        str: absolute path
    """
    current_file = os.path.abspath(__file__)
    current_directory = os.path.dirname(current_file)

    project_directory = os.path.dirname(current_directory)

    img_folder_path = os.path.join(project_directory, 'img')

    return img_folder_path
