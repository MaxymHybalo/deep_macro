import os
import sys
sys.path.insert(0, os.getcwd())

from video_generator import generate
from transformer import search

if __name__ == '__main__':
    search()
    generate()