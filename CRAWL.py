from bs4 import BeautifulSoup
import requests
import json

def CRAWL():
    a =[]
    url = 'https://nhathuoclongchau.com.vn'   
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    products = soup.findAll("div", class_="h-full relative flex rounded-xl border border-solid border-white bg-white transition-all duration-300 ease-out hover:border-blue-5 flex-col")
    for i in products:
        tenSanPham = i.find("h3", class_ = "overflow-hidden text-gray-10 text-body2 font-semibold line-clamp-2 md:line-clamp-3 mb-1 md:mb-2")
        tenSanPham = tenSanPham.getText(strip = True)
        sp = {"tenSanPham":tenSanPham}
        a.append(sp)
    return a

    

    