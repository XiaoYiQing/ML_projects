
import numpy as np
import os

from PIL import Image

from pathlib import Path

def file_exists(path_str):
    """Return True if the given file path exists and is a file."""
    return Path(path_str).is_file()

def next_free_name(dir_path, base_name, ext=""):
    """
    Return a Path like 'base_name.ext', or 'base_name_1.ext',
    'base_name_2.ext', ... if needed.

    Note: this is straight out of chatGPT.
    """
    dir_path = Path(dir_path)
    candidate = dir_path / f"{base_name}{ext}"
    if not candidate.exists():
        return candidate

    i = 1
    while True:
        candidate = dir_path / f"{base_name}_{i}{ext}"
        if not candidate.exists():
            return candidate
        i += 1