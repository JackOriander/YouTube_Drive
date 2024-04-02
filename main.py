import numpy as np
import cv2
from qsqrcode.qrcode import Qrcode
from textwrap import wrap
import os
from pathlib import Path
from PIL import Image

def image_putdata(value):
    cmap = {'0': (255,255,255),
            '1': (0,0,0)}

    data = [cmap[letter] for letter in value]
    img = Image.new('RGB', (20, len(value)//20), "white")
    img.putdata(data)
    return img

def file_to_binary_string(file_path):
    with open(file_path, 'rb') as file:
        binary_data = file.read()
        binary_string = ''.join(format(byte, '08b') for byte in binary_data)
    return binary_string

def binary_string_to_file(binary_string, output_file_path):
    with open(output_file_path, 'wb') as file:
        for i in range(0, len(binary_string), 8):
            byte = binary_string[i:i+8]
            file.write(bytes([int(byte, 2)]))

def binary_to_video(binary_string, output_file_path, size=400):
    directory = 'frames'
    frames = []
    frames_bin = wrap(binary_string, width=400)
    for count, data in enumerate(frames_bin):
        #print(f'{count}->{data}')
        #Qrcode(data, 'H').resize(size).generate(f'frames/frame{count}.png')
        frames.append(image_putdata(data))
        
    video = cv2.VideoWriter(output_file_path, cv2.VideoWriter_fourcc(*"mp4v"),  30, (size, size))
    files = Path(directory).glob('*.png')
    for count, frame in enumerate(frames):
        frame.save('frames/'+output_file_path[:-4]+f'_{count}.jpg','JPEG')
    for filename in sorted(files):
        video.write(cv2.imread(str(filename)))
    video.release()

# Example usage:
input_file = 'testing_files/file.txt'
output_file = 'output_files/output_file.txt'
output_vid = 'output_vid2.mp4'

binary_data = file_to_binary_string(input_file)
print(len(binary_data)) # Should print the size of the input file in bytes
binary_to_video(binary_data, output_vid)
#binary_string_to_file(binary_data, output_file)
