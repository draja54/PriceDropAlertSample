import requests
from bs4 import BeautifulSoup
from decimal import Decimal
from re import sub
import smtplib
import time

# URL indicates the webpage we want to scrape

URL = 'https://www.amazon.in/gp/product/B01N6OLO8U/ref=s9_acss_bw_cg_INPCWe_6a1_w?pf_rd_m=A1K21FY43GMZF8&pf_rd_s=merchandised-search-3&pf_rd_r=F0FSVQPGQG3WB2B25E31&pf_rd_t=101&pf_rd_p=5d82acaa-b7d5-4845-bcab-37a465bc023c&pf_rd_i=11599648031'

# Type myuseragent in the browser to get the value

headers = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}

def check_price():
    # We pass url and the header to get all the data from the page
    page = requests.get(URL,headers = headers)

    # retrive the content of the page with html parser
    soup = BeautifulSoup(page.content,'html.parser')

    # Use find metod to search based on the id from the UI page
    # We can see the id by pressing f12 on the browser page or right click on the browser page and viwe source
    
    # Getting the title of the item from Amazon website 
    title = soup.find(id = "productTitle").get_text().strip()

    # Getting the price of the product (It will come in the form of $ 2500.33 which is a string)
    currency_price = soup.find(id = "priceblock_ourprice").get_text()
    
    # convert the currency to float variable
    float_price = Decimal(sub(r'[^\d.]', '', currency_price))

    # if the price value is lessthan a set amount/threshold amount(20000 here) send an email alert

    if(float_price < 20000.00):
        send_email_alert()

    print(title)
    print(currency_price)
    print(float_price)

def send_email_alert():

    # we are using SMTP - Simple Mail Transfer Protocol fror sending Email
    # we are using google mail services for sending the email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    # Providing the credentials for google
    # First parameter is login name and the second parameter is app password.
    
    login_name = "abc@gmail.com"
    password = "XXXxxxXXX"
    to_address = 'abc@hotmail.com'

    """
    For the second parameter few steps have to be taken
    1. Enable two step auhenticcation in google account
    2. regiser for Less secure app access as Allow less secure apps: ON
    3. Generate app password for Mail in Select App and select the device you are running the on(I choose  Windows Computer).
    4. It will generate the App password
    5. pass this generated password as password in the second parameter.
    """
    server.login(login_name,password)

    # Create the subject and body objects to be passed in the email
    subject = 'Price fell down!'
    body =  "Check the  amazon link https://www.amazon.in/gp/product/B01N6OLO8U/ref=s9_acss_bw_cg_INPCWe_6a1_w?pf_rd_m=A1K21FY43GMZF8&pf_rd_s=merchandised-search-3&pf_rd_r=F0FSVQPGQG3WB2B25E31&pf_rd_t=101&pf_rd_p=5d82acaa-b7d5-4845-bcab-37a465bc023c&pf_rd_i=11599648031"

    # Create the msg object with subject and body
    msg = f"Subject: {subject}\n\n{body}"
    
    server.sendmail(
        login_name,
        to_address,
        msg
        )
    print("HEY EMAIL HAS BEEN SENT!")
    server.quit()

check_price()

# we can run the check_price method periodically by passing in a while loop

"""
while(true):
    check_price()
    time_to_wait = 60*30
    # after checking the price wait for specified time (here 30 minutes) to check again
    time.sleep(time_to_wait)
"""

"""
References:
    https://www.youtube.com/watch?v=Bg9r_yLk7VY
    https://www.youtube.com/channel/UClb90NQQcskPUGDIXsQEz5Q
    
"""