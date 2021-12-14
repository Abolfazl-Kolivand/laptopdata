import requests
from bs4 import BeautifulSoup
import re
import mysql.connector
#اسکریپتی برای یافتن مشخصات و قیمت  5 صفحه ی اول پر بازدید ترین
#لپ تاپ های سایت دیجی کالا و ذخیره آن ها بر روی یک دیتابیس
cnx = mysql.connector.connect(user='*****', password='*****',
                              host='localhost',
                              database='laptops')
cursor = cnx.cursor()
query = '''CREATE TABLE laptops_table (
                brand VARCHAR ( 255 ),
                model VARCHAR ( 255 ) NOT NULL,
                size VARCHAR ( 255 ) NOT NULL,
                cpu VARCHAR ( 255 ),
                ram VARCHAR ( 255 ),
                gpu VARCHAR ( 255 ),
            price INT ( 255 ) NOT NULL,
            PRIMARY KEY ( model, size, price ))'''
cursor.execute(query)
#fuction for create table

def f_brand(l_b): #l_b means laptop brand
    l_brand = re.findall(r'<span class=\"c-product__title-en\">(\w.+?) .+\n*.+<\/span>', str(l_b))
    return l_brand
    #a regex to find a laptop brand from the html texts of the digikala site
    
def f_model(l_m): #l_m means laptop model
    l_model = re.findall(r'<span class=\"c-product__title-en\">\w+? (\w* *-*\w*-*\w*-*\w*).*?<\/.+?>', str(l_m))
    return l_model
    #a regex to find a laptop model from the html texts of the digikala site

def f_size(l_s): #l_b means laptop brand
    l_size = re.findall(r'<span.+>.*(.\d\.*. inch).*<\/.+?>', str(l_s))
    return l_size
    #a regex to find a laptop size from the html texts of the digikala site

def f_cpu(l_c):
    l_cpu = re.findall(r'<span>سری پردازنده: <\/.+?><.+?>\s +(.+?)\s +<\/.+?>', str(l_c))
    return l_cpu
    #a regex to find a laptop cpu from the html texts of the digikala site

def f_ram(l_r):
    l_ram = re.findall(r'<span>ظرفیت حافظه RAM: <\/.+?><.+?>\s +(.+?)\s +<\/.+?>', str(l_r))
    return l_ram
    #همچون بلاک بالایی

def f_gpu(l_g):
    l_gpu = re.findall(r'<span>سازنده پردازنده گرافیکی: <\/.+?><.+?>\s +(.+?)\s +<\/.+?>', str(l_g))
    return l_gpu
    #همچون بلاک بالایی

def f_price(l_p):
    l_price = re.findall(r'<.+>\s*(.+)\n\s*<.+>', str(l_p))
    return l_price
    #همچون بلاک بالایی

def f_db(b, m, s, c, r ,g ,p): #fuction for insert data to db
    cursor.execute("INSERT IGNORE INTO laptops_table VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s');"% (b, m, s, c, r ,g ,p))

href_list = list() #لیستی برای ذخیره آدرس سایت لپ تاپ ها
for number in range(1,6):
    site = "https://www.digikala.com/search/category-notebook-netbook-ultrabook/?pageno=%s"%number
    ltps_dgkala = requests.get(site)
    print(ltps_dgkala, number) #for show response
    soup_ltps = BeautifulSoup(ltps_dgkala.text, 'html.parser')
    ltp_values = soup_ltps.find_all('div', attrs={'class':'c-product-box__title'})
    for href in ltp_values:
        href_ltps = re.findall(r'href=\"/(.+?)\" .+?\">', str(href))
        if href_ltps != []:
            href_list.append(href_ltps[0])
count = 1 #for show response
for case in href_list:
    ltp_site = 'https://www.digikala.com/'+str(case)
    laptop = requests.get(ltp_site)
    print('_________________________________________________________________________')
    print(laptop, count)
    count+=1
    soup_laptop = BeautifulSoup(laptop.text, 'html.parser')
    ltp_values = soup_laptop.find_all('div', attrs={'class':'c-product__config'})
    #get the specs of laptops from html text 
    ltp_feature = soup_laptop.find_all('ul', attrs={'data-title':'ویژگی‌های کالا'})
    #get the features of laptops from html text
    ltp_prices = soup_laptop.find_all('div', attrs={'class':'c-product__seller-price-pure js-price-value'})
    #get the prices of laptops from html text
    brand = f_brand(ltp_values)
    if brand!=[]: #هر مراحل وابسته به مرحله ی قبل است یعنی اگر شرط دلخواه برقرار نباشد به سراغ کیس بعدی می رود 
        brand = str(brand[0]).upper()
        model = f_model(ltp_values)
        if model!=[]:
            model = str(model[0]).upper()
            size = f_size(ltp_values)
            if size!=[]:
                size = str(size[0]).strip().upper()
                cpu = f_cpu(ltp_feature)
                if cpu!=[]:
                    cpu = str(cpu[0]).upper()
                    ram = f_ram(ltp_feature) 
                    ram = re.sub('گیگابایت','GB',str(ram[0]))
                    ram = re.sub('چهار','4',ram)
                    ram = re.sub('هشت','8',ram)
                    ram = re.sub(' ' ,'' ,ram)
                    if ram!=[]:
                        gpu = f_gpu(ltp_feature)
                        if gpu!=[]:
                            gpu = str(gpu[0]).upper()
                            price = f_price(ltp_prices)
                            if price!=[]:
                                price = int(re.sub(',','',price[0]))
                                f_db(brand, model, size, cpu, ram, gpu, price)
                                #print(brand, model, size, cpu, ram, gpu, price)

cnx.commit()   
cnx.close()