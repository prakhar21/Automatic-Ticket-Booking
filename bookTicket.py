'''
    @author: Prakhar Mishra
    @date: 16/02/2016
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
import pyscreenshot as ImageGrab
import time
import pytesseract
import Image
import sys
import re
from pyvirtualdisplay import Display
import datetime
import imaplib
import email
from bs4 import BeautifulSoup
import urllib
import csv




#display = Display(visible=0, size=(1920,1280))
#display.start()

socialcops_website = 'https://collect.socialcops.org/#login'
email = 'pmprakhargenius@gmail.com'
password_social = 'mishra2121'


driver = webdriver.Firefox()
# # Open socialcops 'collect' website get the user credetials
driver.get(socialcops_website)

time.sleep(2)

email_socialcops = driver.find_element_by_id('username')
email_socialcops.send_keys(email)

password_socialcops = driver.find_element_by_id('password')
password_socialcops.send_keys(password_social)

submit_socialcops = driver.find_element_by_id('submit').click()

# Change for page till loaded
time.sleep(12)

driver.find_element_by_id('download').click()

time.sleep(2)

driver.find_element_by_id('send').click()
print 'Data sent !!'

time.sleep(1)
driver.quit()

time.sleep(20)

# Wait for email to come
#Open Gmail and download data

username_gmail = 'pmprakhargenius@gmail.com'
password_gmail = 'asddsazxccxz'

## GMAIL AUTHENTICATION
def gmail_authenticate(u,p):
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(u, p)
    return mail

def parse_email(r):
    regex01 = '<a.+?(http:.+?.csv)'
    inter_link = re.findall(regex01,str(r))
    final_link = inter_link[0].replace('=\\r\\n','')
    return final_link


def get_mail_uid(u):
    u.select("inbox")
    result , data = u.uid('search', None, '(HEADER Subject "SocialCops Collect : Raw Data Report")')
    latest_email_uid = data[0].split()[-1]
    result, data = u.uid('fetch', latest_email_uid, '(RFC822)')
    raw_email = data[0][1]
    return latest_email_uid, raw_email

def download_data(u):
    urllib.urlretrieve(u, filename="/home/prakhar/Desktop/scraping/Reservation/data.csv")

mail = gmail_authenticate(username_gmail,password_gmail)
print 'Gmail Authentication Successful !!\n'
raw_email = get_mail_uid(mail)
link_to_data = parse_email(raw_email)
print link_to_data
download_data(link_to_data)



## Updating Variables
data_dict = {}
data_list = []

outfile_all = open('/home/prakhar/Desktop/scraping/Reservation/data.csv','rb' )
reader = csv.reader(outfile_all)
for row in reader:
    data_list.append(row)

for i in data_list:
    data_dict['Name'] = i[8]
    data_dict['Age'] = i[9]
    data_dict['Mobile'] = i[10]
    if i[12] == 'No':
        data_dict['Gender'] = 'Female'
    elif i[12] == 'Yes':
        data_dict['Gender'] = 'Male'
    data_dict['From'] = i[14]
    data_dict['To'] = i[15]
    data_dict['Date'] = i[16]
    data_dict['Train'] = i[17]
    data_dict['Class'] = i[18]


# ## Passenger Details
SOURCE = data_dict['From']
DESTINATION = data_dict['To']
DATE = '19-03-2016'#data_dict['Date']
TRAIN_NUMBER = data_dict['Train']
CLASS = data_dict['Class']
YOUR_NAME = data_dict['Name']
AGE = data_dict['Age']
GENDER = data_dict['Gender']
CHECK_AUTO_UPGRADE = False
MOBILE_NO = data_dict['Mobile']




# display = Display(visible=0, size=(1920,1280))
# display.start()

driver = webdriver.Firefox()


irctc_website = 'https://www.irctc.co.in/eticketing/loginHome.jsf'
user_name = 'anilkr_15'
pwd = 'mishranita'


driver.get(irctc_website)

time.sleep(2)

## Login Details - Autofill
Id = driver.find_element_by_id('usernameId')
Id.send_keys(user_name)

time.sleep(1)

Password = driver.find_element_by_name('j_password')
Password.send_keys(pwd)

time.sleep(1)

## Crack Captcha - Autofill
Captcha = driver.find_element_by_name('j_captcha')
im=ImageGrab.grab(bbox=(768,385,890,420)) # X1,Y1,X2,Y2
im.save('picT1.png')
temp = pytesseract.image_to_string(Image.open('picT1.png'))
temp = temp.replace(' ','')
Captcha.send_keys(temp)

Submit = driver.find_element_by_id('loginbutton').click()
time.sleep(1)

## Page  after  login - FILL IN TRAVEL DETAILS
source = driver.find_element_by_id('jpform:fromStation').send_keys(SOURCE)
destination = driver.find_element_by_id('jpform:toStation').send_keys(DESTINATION)
dateOfTravel = driver.find_element_by_id('jpform:journeyDateInputDate').send_keys(DATE)
findTrainSubmit = driver.find_element_by_id('jpform:jpsubmit').click()
#Hardcoded for class
## Can be changed to auto class , just by string concatination
classSelect = driver.find_element_by_id('cllink-14660-2S-4').click()

time.sleep(3)
driver.find_element_by_link_text("Book Now").click()
time.sleep(5)

elem = driver.find_element_by_xpath("//*")
source_code = elem.get_attribute("outerHTML")

f = open('/home/prakhar/Desktop/html_source_code.html', 'w')
f.write(source_code.encode('utf-8'))
f.close()



## Fill travel details for passengers
regex = 'addPassengerForm:psdetail:0:(p[0-9]+)?\"'

data = ''
with open('/home/prakhar/Desktop/html_source_code.html','r') as myfile:
    data=myfile.read().replace('\n', '')

data = re.findall(regex,data)[0]
print data

# re.findall(file_sourcecode, regex)

passengerName = driver.find_element_by_id('addPassengerForm:psdetail:0:'+str(data))
passengerName.send_keys(YOUR_NAME)

time.sleep(1)

passengerAge = driver.find_element_by_id('addPassengerForm:psdetail:0:psgnAge')
passengerAge.send_keys(AGE)

time.sleep(1)

passengerGender = Select(driver.find_element_by_id('addPassengerForm:psdetail:0:psgnGender'))
passengerGender.select_by_visible_text(GENDER)

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

time.sleep(2)

checkAutoUpgradation = driver.find_element_by_id('addPassengerForm:autoUpgrade').click()

mobileDetails = driver.find_element_by_id('addPassengerForm:mobileNo')
mobileDetails.clear()
mobileDetails.send_keys(MOBILE_NO)


e = driver.find_element_by_id('bkg_captcha')
location = e.location
size = e.size

time.sleep(2) 

driver.save_screenshot('captchaPassengerDetails.png')
im = Image.open('captchaPassengerDetails.png')

left = location['x']
top = location['y']
right = location['x'] + size['width']
bottom = location['y'] + size['height']

im = im.crop((left, top, right, bottom))
im.save('captchaPassengerDetails.png')
temp1 = pytesseract.image_to_string(Image.open('captchaPassengerDetails.png'))
temp1 = temp1.replace(' ','')
Captcha = driver.find_element_by_name('j_captcha')
Captcha.send_keys(temp1)

time.sleep(2)

## Proceed to payment gateway

submitPassengerDetails = driver.find_element_by_id('validate').click()

time.sleep(1)

clickDebitCard = driver.find_element_by_id('DEBIT_CARD').click()


icici_debit_radio = driver.find_element_by_xpath(".//*[@type='radio'][@value='41']")
icici_debit_radio.click()

finalSubmit = driver.find_element_by_id('validate').click()




## Checkout Details - card payment
TYPE_OF_CARD = 'Visa-Debit/Credit'  # also Mastercard
cardType = Select(driver.find_element_by_name('CardTypeSelectBox'))
cardType.select_by_visible_text(TYPE_OF_CARD)

time.sleep(3)
CARD_NO1 = '4693'
CARD_NO2 = '7510'
CARD_NO3 = '5205'
CARD_NO4 = '5227'
cardNumber = driver.find_element_by_name('CardNum1').send_keys(CARD_NO1)
time.sleep(1)
cardNumber = driver.find_element_by_name('CardNum2').send_keys(CARD_NO2)
time.sleep(1)
cardNumber = driver.find_element_by_name('CardNum3').send_keys(CARD_NO3)
time.sleep(1)
cardNumber = driver.find_element_by_name('CardNum4').send_keys(CARD_NO4)

time.sleep(3)

EXP_MONTH = '10'
EXP_YEAR = '2024'
expiryDate = Select(driver.find_element_by_name('ExpDtMon'))
expiryDate.select_by_value(EXP_MONTH)
expiryDate = Select(driver.find_element_by_name('ExpDtYr'))
expiryDate.select_by_value(EXP_YEAR)

time.sleep(3)

CVV = '127'
cvvDetails = driver.find_element_by_name('CVVNum')
cvvDetails.send_keys(CVV)

time.sleep(3)

NAME_CARDHOLDER = 'Prakhar Mishra'
nameOfCardHolder = driver.find_element_by_name('NameOnCard')
nameOfCardHolder.send_keys(NAME_CARDHOLDER)

time.sleep(3)

ATM = '1963'
atmPinDetails = driver.find_element_by_name("ATMPIN")
atmPinDetails.send_keys(ATM)

time.sleep(3)

payMoneyButton = driver.find_element_by_name('btnPay')
payMoneyButton.click()
