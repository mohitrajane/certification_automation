import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from PIL import Image, ImageDraw, ImageFont

def read_image(path):
    try:
        image = Image.open(path)
    except FileNotFoundError as e:
        print("File not found. Please check your path")
    return image

def add_text(name_list, path):
    font = ImageFont.truetype(font='font/Nexa Bold.otf', size=60)
    for name in name_list:
        image = read_image(path)
        draw = ImageDraw.Draw(image)
        (x, y) = (1370, 945)
        #print('name[0]:{}\tname[2]:{}'.format(name[0],name[2]))
        message = name[0] + ' (' + name[2] +')'
        color = 'rgb(0, 0, 0)'
        draw.text((x, y), message, fill=color, font=font)
        output_path = 'output/' + name[0] + '.png'
        image.save(output_path, format='png')
        print("Saved:{}".format(output_path))
        image.close()

def parse_csv(path):
    name_list = list()
    flag = 0
    with open(path) as name_file:
        csv_reader = csv.reader(name_file, delimiter=',')
        for row in csv_reader:
            if flag == 1:
                name_list.append([row[0],row[1],row[2]])  #0 == name 1 == email 2 == class
            flag = 1
    name_file.close()
    return name_list

if __name__ == '__main__':
    path = input("Enter image file:")
    name_list_path = input("Enter name file ")
    name_list = parse_csv(name_list_path)
    #print(name_list)
    add_text(name_list, path)