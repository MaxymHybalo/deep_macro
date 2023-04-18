import os

def frames(path):
    frames = 0
    files = os.listdir(path)

    for f in files:
        f = f.split('.')[0]
        f = int(f)
        if f > frames:
            frames = f
    return frames