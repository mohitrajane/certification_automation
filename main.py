import argparse
from PIL import Image, ImageDraw, ImageFont

def read_image(path):
    print(path)
    try:
        image = Image.open(path)
    except FileNotFoundError as e:
        print("File not found. Please check your path")
    return image

def add_text(name_list, path):
    font = ImageFont.truetype(font='font/Roboto-Regular.ttf', size=50)
    for name in name_list:
        image = read_image(path)
        draw = ImageDraw.Draw(image)
        (x, y) = (1170, 950)
        message = name
        color = 'rgb(0, 0, 0)'
        draw.text((x, y), message, fill=color, font=font)
        output_path = 'output/' + name + '.png'
        image.save(output_path, format='png')
        image.close()

if __name__ == '__main__':
    path = input("Enter file name:")
    name_list = ['Mohit Rajan E', 'Alex', 'John', 'Neeraj']
    # name_list = input("Enter list")
    add_text(name_list, path)