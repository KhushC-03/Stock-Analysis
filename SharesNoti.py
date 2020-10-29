import clicksend_client
from pathlib import Path
from datetime import datetime
import requests, time, os, json, glob, sys, logging
from bs4 import BeautifulSoup
from clicksend_client import SmsMessage
from clicksend_client.rest import ApiException
from currency_converter import CurrencyConverter
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from yahoo_fin import stock_info as si
from proxyscrape import create_collector, get_collector, Proxy

c = CurrencyConverter()
apiusrnme = bytes.fromhex('4368617568616e323030336b6340676d61696c2e636f6d').decode('utf-8')
apikey = bytes.fromhex('45333746323041452d444545442d334238462d444636462d374531333637304132423732').decode('utf-8')
os.system('cls')
v = requests.session()
def get_stock_price():
    I1A = input('Enter the names of the stock(s), if theres multiple split them with a comma ')
    if ',' in I1A:
        stock_comma = (I1A.split(','))
        for stocks in stock_comma:
            base_url = ('https://uk.finance.yahoo.com/quote/{}?p={}'.format(stocks,stocks))
            stock_price = v.get(base_url, timeout=5, allow_redirects=False)
            soup = BeautifulSoup(stock_price.content, 'html.parser')
            webdata = soup.find_all('span')[20]
            stockcap = stocks.capitalize()
            print('{} price per share is: ${}'.format(stockcap,webdata.text))
    else:
        base_url = ('https://uk.finance.yahoo.com/quote/{}?p={}'.format(I1A,I1A))
        stock_price = v.get(base_url, timeout=5, allow_redirects=False)
        soup = BeautifulSoup(stock_price.content, 'html.parser')
        webdata = soup.find_all('span')[20]
        IA1cap = I1A.capitalize()
        print('{} price per share is: ${}'.format(IA1cap,webdata.text))
def get_file_names():
    filepath = 'SharePortfolios'
    i = 0
    filesi = os.listdir(filepath)
    for files in filesi:
        i = i + 1
        print('File Number {}: {}'.format(i,files))

def calculate_share_price():
    filepath = 'SharePortfolios'
    #b = os.path.getsize('Shares Notifyer\\SharePortfolios')
    files = os.listdir(filepath)
    if not files:
        print('There Are No Stock Portfolio Files Please Make One')
        time.sleep(0.5)
        input('Click Enter To Make A Stock Portfolio')
        make_stock_portfolio()
    else:
        get_file_names()
        i = input('Enter The Number Of The File You Would Like To Open ')
        ii = int(i) - 1
        filesi = os.listdir(filepath)[int(ii)]
        filepath1 = 'SharePortfolios\\{}'.format(filesi)
        print(filesi)
        o = open(filepath1)
        data = json.load(o)
        stock_name = data['Stock Name']
        amount_of_stocks = data['Amount Of Stocks']
        stock_price = si.get_live_price(str(stock_name))
        share_price_2dm = round(stock_price,2)
        price = int(share_price_2dm)
        aprice = (int(amount_of_stocks) * price)
        c = CurrencyConverter()
        currency_type = input('What Is The Currency You Would Like To See Your Shares In? e.g GBP USD EUR ')
        if currency_type.islower():
            print('Please Re-write The Currency In All CAPS ')
            time.sleep(0.2)
            currency_type = input('What Is The Currency You Would Like To See Your Shares In? e.g GBP USD EUR ')
            m = c.convert(aprice, 'USD', currency_type)
            main_price_2dm = round(m,2)
            print(' {} {}'.format(main_price_2dm,currency_type))
        else:
            m = c.convert(aprice, 'USD', currency_type)
            main_price_2dm = round(m,2)
            print('{} {}'.format(main_price_2dm,currency_type))

def make_stock_portfolio():
    I1 = input('Which stock(s) do you own, split them with a comma ')
    if ',' in I1:
        stock_comma = (I1.split(','))        
        for stocks in stock_comma:
            stockscap = stocks.capitalize()
            filename = 'SharePortfolios\\{}portfolio.json'.format(stocks)
            a = open(filename,'a')
            b = os.path.getsize(filename)   
            a.close() 
            if int(b) == 0:    
                I1A = input('How many stocks do you have for {} '.format(stockscap))
                stock_ammount = (I1A.split(','))            
                f = open(filename,'w') 
                Stock_Portfolio = {
                    "Stock Name":stockscap,
                    "Amount Of Stocks":I1A
                }
                json.dump(Stock_Portfolio,f)
                time.sleep(1)
                print('Portfolio Successfully Made For {}'.format(stockscap))
                f.close()
            elif int(b) >0 or int(b) >1:
                I2 = input('Portfolio Already Exists For {}, If You Would Like To Change It Press < C > If Not Click ENTER '.format(stockscap))
                os.remove(filename)
                letterc = I2.capitalize()
                a = open(filename,'a')
                b = os.path.getsize(filename)   
                a.close() 
                if letterc == 'C':
                    stockscap = stocks.capitalize()
                    I1A = input('How many stocks do you now have for {} '.format(stockscap))
                    stock_ammount = (I1A.split(','))
                    filename = 'SharePortfolios\\{}portfolio.json'.format(stocks)
                    a = open(filename,'a')
                    b = os.path.getsize(filename)   
                    a.close() 
                    if int(b) >0:                
                        f = open(filename,'w') 
                        Stock_Portfolio = {
                            "Stock Name":stockscap,
                            "Amount Of Stocks":I1A
                        }
                        json.dump(Stock_Portfolio,f)
                        time.sleep(1)
                        print('Portfolio Successfully Made For {}'.format(stockscap))
                        f.close()
                    else:
                        print('ERROR PLEASE TRY AGAIN')
            else:    
                os.system('cls')   
                menu()
    else:
        stockscap = I1.capitalize()
        filename = 'SharePortfolios\\{}portfolio.json'.format(stockscap)
        a = open(filename,'a')
        b = os.path.getsize(filename)   
        a.close() 
        if int(b) == 0:   
            I1A = input('How many stocks do you have for {} '.format(stockscap))
            stock_ammount = I1A             
            f = open(filename,'w') 
            Stock_Portfolio = {
                "Stock Name":stockscap,
                "Amount Of Stocks":I1A
            }
            json.dump(Stock_Portfolio,f)
            time.sleep(1)
            print('Portfolio Successfully Made For {}'.format(stockscap))
            f.close()
        elif int(b) >0 or int(b) >1:
            I2 = input('Portfolio Already Exists For {}, If You Would Like To Change It Press < C > If Not Click ENTER '.format(stockscap))
            letterc = I2.capitalize()
            if letterc == 'C':
                stockscap = I1.capitalize()
                I1A = input('How many stocks do you now have for {} '.format(stockscap))
                stock_ammount = (I1A.split(','))
                filename = 'SharePortfolios\\{}portfolio.json'.format(I1)
                a = open(filename,'a')
                b = os.path.getsize(filename)   
                a.close() 
                if int(b) >0:                
                    f = open(filename,'w') 
                    Stock_Portfolio = {
                        "Stock Name":stockscap,
                        "Amount Of Stocks":I1A
                    }
                    json.dump(Stock_Portfolio,f)
                    time.sleep(1)
                    print('Portfolio Successfully Made For {}'.format(stockscap))
                    f.close()
                else:
                    print('ERROR PLEASE TRY AGAIN')
            else:
                os.system('cls')
                menu()

def get_stock_news():
    baseurl = 'https://www.marketwatch.com/investing/stock/cat'.format()
    html_page = v.get(baseurl).text
    soup = BeautifulSoup(html_page, "lxml")
    for href in soup.findAll('a'):
        print(href.get('href'))[196]
def change_number():
    os.remove("settings.json")
    a = open('settings.json','a')
    b = os.path.getsize("settings.json")   
    a.close() 
    f = open('settings.json','w') 
    I1 = input('Please enter your new phone number including prefix and [+] ')
    phone_number = [
            {
                "phone_number":I1
                },
            {
                "retry_delay":"125"
                }
    ]
    json.dump(phone_number,f)
    print('Phone Number is added! {}'.format(I1))
    f.close()

def setup_number():
    a = open('settings.json','a')
    b = os.path.getsize("settings.json")   
    a.close() 
    if int(b) == 0:
        f = open('settings.json','w') 
        I1 = input('Please enter your phone number including prefix and [+] ')
        phone_number = [
            {
                "phone_number":I1
                },
            {
                "retry_delay":"125"}
        ]

        json.dump(phone_number,f)
        print('Phone Number is added! {}'.format(I1))
        f.close()
    elif int(b) >0 or int(b) >1:
        with open('settings.json') as (j):
            data = json.load(j) 
            number = data[0]['phone_number']
            print('Number is setup',number)
            j.close()

def monitor_loop():
    for x in range (0,25):  
        b = "Monitoring" + "." * x
        print (b, end="\r")
        time.sleep(1)
    print(end='\r')

def loop_monitor_loop():
    for i in range(4):
        monitor_loop()
        print(end='\r')

def share_price_notifications():
    #b = os.path.getsize("settings.json")  
    settings = os.path.exists('settings.json')
    if settings == False:
        print('There Is No Phone Number On File, Please Set One Up ')
        time.sleep(0.4)
        setup_number()
        share_price_notifications()
    else:
        f = open('settings.json')
        data = json.load(f)
        number = data[0]['phone_number']
        delay = data[1]['retry_delay']
        I1 = input("What is the stock you'd like to monitor? ")
        I2 = input('What is the stock price you want to be notified at? ')
        note = ('{} stock has hit ${}'.format(I1,I2))
        date = time.strftime('%a %H:%M:%S')
        print('************')
        print(date)
        i = 0
        print("********************************************************")
        log = open('LOG.txt','a')
        t = datetime.utcnow()
        datestamp = t.strftime('%d/%m/%y')
        timestamp = time.strftime('%H:%M:%S')
        logheader = '\n----------- MONITOR START DATE '+datestamp+' ----- MONITOR START TIME '+timestamp+' -----------\n'
        log.write(str(logheader))
        timestamp = time.strftime('%H:%M:%S')
        log0 = ('[{}] [MONITOR LOOP {}] [SUCCESS] [200] [STARTED MONITOR]  [STOCK PRICE GOAL {}]\n').format(timestamp,i,I2)
        log.write(log0)
        while True:
            i = i + 1
            proxies = {
            'http': '',
            'https': ''
                }
            base_url = ('https://uk.finance.yahoo.com/quote/{}?p={}'.format(I1,I1))
            stock_price = v.get(base_url, timeout=5, allow_redirects=False, verify=False,proxies=proxies,)
            soup = BeautifulSoup(stock_price.content, 'html.parser')
            webdata = soup.find_all('span')[20]
            webdata_price = webdata.text
            print('Monitor loop at '+str(i)+' try(s)','Current share price at $'+str(webdata_price),end='\r')
            time.sleep(int(delay))
            base_url = ('https://uk.finance.yahoo.com/quote/{}?p={}'.format(I1,I1))
            stock_price = v.get(base_url, timeout=5, allow_redirects=False, verify=False,proxies=proxies)
            if 201 <= stock_price.status_code <= 1000:                                    
                timestamp2 = time.strftime('%H:%M:%S')
                log1 = ('[{}] [MONITOR LOOP {}] [ERROR] [{}] [RETRY MONITOR FAILED RESTART TASK] [STOCK PRICE AT {}]\n').format(timestamp2,i,stock_price.status_code,webdata_price)
                log.write(log1)
                input('An Error Occured, Press ENTER To Continue')
                os.system('cls')
                menu()
            elif stock_price.status_code == 200:
                timestamp3 = time.strftime('%H:%M:%S')
                log2 = ('[{}] [MONITOR LOOP {}] [SUCCESS] [{}] [<<<MONITORING>>>] [STOCK PRICE AT {}]\n').format(timestamp3,i,stock_price.status_code,webdata_price)
                log.write(log2)
                soup = BeautifulSoup(stock_price.content, 'html.parser')
                webdata = soup.find_all('span')[20]   
                webdata_price = webdata.text
                if webdata_price >= I2:
                    configuration = clicksend_client.Configuration()
                    configuration.username = str(apiusrnme)
                    configuration.password = str(apikey)
                    api_instance = clicksend_client.SMSApi(clicksend_client.ApiClient(configuration))
                    sms_message = SmsMessage(source="python",body=note,to=number)
                    sms_messages = clicksend_client.SmsMessageCollection(messages=[sms_message])
                    try:
                        api_response = api_instance.sms_send_post(sms_messages)
                        #print(api_response)
                        print('SMS SENT')
                        timestamp4 = time.strftime('%H:%M:%S')
                        log3 = ('[{}] [MONITOR LOOP {}] [SUCCESS] [{}] [<<<SMS SENT>>>] [STOCK PRICE AT {}]\n').format(timestamp4,i,stock_price.status_code,webdata_price)
                        log.write(log3)  
                        log.close()
                        menu()
                    except ApiException as e:
                        print("ERROR SENDING SMS: %s\n" % e)
                        timestamp5 = time.strftime('%H:%M:%S')
                        log4 = ('[{}] [MONITOR LOOP {}] [ERROR] [404] [<<<ERROR SENDING SMS>>>] [STOCK PRICE AT {}]\n').format(timestamp5,i,webdata_price)
                        log.write(log4)  
                        log.close()
                elif webdata_price < I2:
                    a = 1+1

def menu():
    print('\n| 1 | Get Stock Price')
    time.sleep(0.05)
    print('| 2 | Calculate Your Amount Of Share')
    time.sleep(0.05)
    print('| 3 | Setup Stock Price Notifications')
    time.sleep(0.05)
    print('| 4 | Setup Phone Number')
    time.sleep(0.05)
    print('| 5 | Change Phone Number')
    time.sleep(0.05)
    print('| 6 | Make Stock Portfolio')
    time.sleep(0.05)
    print('| 7 | Get Stock News')
    time.sleep(0.05)
    print('| 8 | Exit')
    time.sleep(0.05)
    I1 = input("Enter The Number Assigned To The Service You'd Like To Use | ")
    if I1 == '1':     
        get_stock_price()
        input('Press ENTER to continue')
        os.system('cls')
        menu()
    elif I1 == '2':    
        try:    
            calculate_share_price()
            input('Press ENTER to continue')
            os.system('cls')
            menu()
        except Exception as c:
            print(c)
            menu()
    elif I1 == '3':    
            share_price_notifications()
            input('Press ENTER to continue')
            os.system('cls')
            menu()      
    elif I1 =='4': 
        try:       
            setup_number()
            input('Press ENTER to continue')
            os.system('cls')
            menu()
        except Exception as c:
            print(c)
            menu()
    elif I1 =='5':        
        try:       
            change_number()
            input('Press ENTER to continue')
            os.system('cls')
            menu()
        except Exception as c:
            print(c)
            menu()
    elif I1 =='6':        
        try:       
            make_stock_portfolio()
            input('Press ENTER to continue')
            os.system('cls')
            menu()
        except Exception as c:
            print(c)
            menu()
    elif I1 =='7':     
        try:  
            get_stock_news() 
            input('Press ENTER to continue')
            os.system('cls')
            menu()
        except Exception as c:
            print(c)
            menu()
    elif I1 =='8':
        print('Goodbye!')
        time.sleep(1)
        sys.exit()
    else:      
        print('Invalid Selection')
        time.sleep(1)
        os.system('cls')        
        menu()
menu()




