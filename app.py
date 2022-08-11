from flask import Flask
from flask import render_template
from selenium import webdriver
from bs4 import BeautifulSoup
import time  
from flask_swagger_ui import get_swaggerui_blueprint  
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.route("/getallproducts/<string:searchterm>")
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
    driver = webdriver.Chrome(executable_path="C:\Program Files (x86)\chromedriver.exe")
    driver.get("https://www.google.com/search?" + "q=" + searchterm + "&tbm=shop")
    soup = BeautifulSoup(driver.page_source)
    driver.close()
    return soup

def sort(array):
        """Sorting array by quicksort:"""
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


if __name__ == "__main__": #if this file being run is the one that is being run, then this will evaluate to true since the one being run has __name__ set to __main__
    app.run(port=5000)