import os
import cv2

fourcc = cv2.VideoWriter_fourcc(*'MP4V')
fps = 14
width, height = 256*2, 255*2

source_path = 'logs/we_out'

def generate():

    out = cv2.VideoWriter('logs/mini_output.mp4', fourcc, fps, (width, height))


    files = os.listdir(source_path)

    frames = 0
    for f in files:
        f = f.split('.')[0]
        f = int(f)
        if f > frames:
            frames = f
    print(frames)

    for i in range(frames):
        img = cv2.imread('{}/{}.png'.format(source_path ,i))
        out.write(img)

    out.release()