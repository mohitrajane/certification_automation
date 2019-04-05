import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders

from PIL import Image, ImageDraw, ImageFont


# function to open the image
def read_image(path):
    try:
        image = Image.open(path)
    except FileNotFoundError as e:
        print("File not found. Please check your path")
        exit(0)
    return image


# function to read each name from list and created output png certificate
def add_text(name_list, path):
    try:
        font = ImageFont.truetype(font='font/Nexa Bold.otf', size=60)
    except:
        print("couldn't load font. Please check if font file exist in ./font")
        exit(0)
    for name in name_list:
        image = read_image(path)
        draw = ImageDraw.Draw(image)
        '''The line bellow is used to specify where to input the text.
        This values was found by trial and error and
        may change according to input'''
        (x, y) = (1370, 945)
        # print('name[0]:{}\tname[2]:{}'.format(name[0],name[2]))
        message = name[0] + ' (' + name[2] + ')'
        color = 'rgb(0, 0, 0)'
        draw.text((x, y), message, fill=color, font=font)
        output_path = 'output/' + name[0] + '.png'
        image.save(output_path, format='png')
        print("Saved:{}".format(output_path))
        image.close()
        print("Sending mail to {}".format(name[1]))
        # comment the line bellow to not send email
        # send_mail(name[1], output_path)


# Function to extract required data from csv file
def parse_csv(path):
    name_list = list()
    flag = 0
    try:
        with open(path) as name_file:
            csv_reader = csv.reader(name_file, delimiter=',')
            for row in csv_reader:
                if flag == 1:
                    name_list.append([row[0], row[1], row[2]])
                    # 0 == name 1 == email 2 == class
                flag = 1
        name_file.close()
    except:
        print("Couldn't load csv file. Please check filename and path")
        exit(0)
    return name_list


# Function to send mail by default works only with sending from  gmail accounts
def send_mail(receiver_address, attach_file_name):
    n = (attach_file_name.split('/'))[1].split('.')
    mail_content = 'Dear ' + n[0] + ''',\nThank ouy for making Arduino Day 2019 conducted
    by Fisat Students Developer Community(FSDC) a grand success. Your
    certificate has been attached to this mail
    '''
    sender_address = email_id
    sender_pass = email_password

    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Arduino day certificate.'

    # The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    attach_file = open(attach_file_name, 'rb').read()
    image = MIMEImage(attach_file, name=n[1])
    message.attach(image)

    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.starttls()  # enable security
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')


if __name__ == '__main__':
    path = input("Enter image file:")
    name_list_path = input("Enter name file:")
    email_id = input("Enter mail id:")
    email_password = input("Enter password for mail id:")
    name_list = parse_csv(name_list_path)
    add_text(name_list, path)
