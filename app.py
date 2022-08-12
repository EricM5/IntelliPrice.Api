from flask import Flask
from flask import render_template
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from bs4 import BeautifulSoup
import time  
from flask_swagger_ui import get_swaggerui_blueprint  
import os

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.route("/getall/<string:searchterm>")
def getallproducts(searchterm):
    soup = GetSoup(searchterm)
    sortedlist = GetSortedList(soup)
    
    return sortedlist

@app.route("/getlowest/<string:searchterm>")
def getlowestproduct(searchterm):
    soup = GetSoup(searchterm)
    lowestproduct = GetSortedList(soup)[0]

    return lowestproduct

@app.route("/gethighest/<string:searchterm>")
def gethighestproduct(searchterm):
    soup = GetSoup(searchterm)
    highestproduct = GetSortedList(soup)[-1]

    return highestproduct

@app.route("/getlowest/<string:searchterm>/<int:size>")
def getlowestnum(searchterm, size):
    if size <= 0:
        return []
    
    soup = GetSoup(searchterm)
    lowestproductlist = GetSortedList(soup)

    if (size > len(lowestproductlist)):
        size = len(lowestproductlist)
    
    lowestproducts = lowestproductlist[0:size]
    return lowestproducts

@app.route("/gethighest/<string:searchterm>/<int:size>")
def gethighestnum(searchterm, size):
    if size <= 0:
        return []
    
    soup = GetSoup(searchterm)
    highestproductlist = GetSortedList(soup)

    if (size > len(highestproductlist)):
        size = len(highestproductlist)
        
    highestproducts = highestproductlist[-size:]
    return highestproducts

def GetSortedList(soup):
    list = soup.find_all('div', class_="sh-dgr__content")

    productlist = []
    for i in list:
        title = i.find_all('h4', class_="Xjkr3b")
        if len(title) == 0:
            title = "Not found"
        else:
            title = i.find_all('h4', class_="Xjkr3b")[0].text
        
        pricebeforeship = i.find_all('span', {"class":["a8Pemb OFFNJ", "a8Pemb OFFNJ Jz5Gae"]})[0].text
        pricefloat = float(pricebeforeship[1:].replace(',',""))
        shipping = i.find_all('div', class_="vEjMR")

        if (len(shipping) == 0):
            shipping = "Shipping Hidden"
        else:
            shipping = i.find_all('div', class_="vEjMR")[0].text
            if '. ' in shipping or 'Free delivery' in shipping or '.' not in shipping:
                shippingfloat = 0.0
            else:
                shippingfloat = shipping.replace(",", '')
                shippingfloat = float(shipping[1:shipping.find(' ')])

        TotalFloat = pricefloat + shippingfloat
        seller = i.find_all('div', class_="aULzUe")[0].text
        
        url = i.find_all('a', class_="shntl")[1].get('href').replace("/url?url=", "").split("%",1)[0].split("&",1)[0]
        if url[0] == '/':
            url = "https://google.com" + url

        tempdict = {"Title":title, "Price":pricebeforeship, "Shipping":shipping, "TotalPrice":TotalFloat, "Seller":seller, "url":url}
        productlist.append(tempdict)

    sortedproductlist = sort(productlist)
    for product in sortedproductlist:
        product["TotalPrice"] = "${:.2f}".format(product["TotalPrice"])
        
    return sortedproductlist

def GetSoup(searchterm):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    driver.get("https://www.google.com/search?" + "q=" + searchterm + "&tbm=shop")

    soup = BeautifulSoup(driver.page_source)
    driver.close()
    return soup

def sort(array):
        less = []
        equal = []
        greater = []

        if len(array) > 1:
            pivot = array[0]["TotalPrice"]
            for x in array:
                if x["TotalPrice"] < pivot:
                    less.append(x)
                elif x["TotalPrice"] == pivot:
                    equal.append(x)
                elif x["TotalPrice"] > pivot:
                    greater.append(x)
            return sort(less)+equal+sort(greater) 
        else:  
            return array

if __name__ == "__main__": 
    app.run(host="0.0.0.0")