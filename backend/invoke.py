import sys
from launcher import run

if __name__ == '__main__':
    _, handle, char_name = sys.argv
    run(handle, char_name)