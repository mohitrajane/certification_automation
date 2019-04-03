import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
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
        send_mail(name[1], output_path)
        x = input("done with sending file")

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

def send_mail(receiver_address, attach_file_name):
    n = (attach_file_name.split('/'))[1].split('.')
    print(n[0])
    mail_content = 'Dear ' + n[0] +''',\nThank ouy for making Arduino Day 2019 conducted
    by Fisat Students Developer Community(FSDC) a grand success. Your 
    certificate has been attached to this mail
    '''
    sender_address = 'fisatsdc@gmail.com'
    sender_pass = 'fisatsdc123#'
    receiver_address = 'mhit98@gmail.com'

    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Arduino day certificate.'

    # The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    attach_file = open(attach_file_name, 'rb').read()  # Open the file as binary mode
    #payload = MIMEBase('application', 'octate-stream')
    #payload.set_payload((attach_file).read())
    #encoders.encode_base64(payload) #encode the attachment
    # add payload header with filename
    #payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name)
    #message.attach(payload)
    image = MIMEImage(attach_file, name=n[1])
    message.attach(image)

    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.starttls()  # enable security
    session.login(sender_address, sender_pass)  # login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')

if __name__ == '__main__':
    path = input("Enter image file:")
    name_list_path = input("Enter name file ")
    name_list = parse_csv(name_list_path)
    #print(name_list)
    add_text(name_list, path)