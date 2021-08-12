import bs4 as bs
import requests
import csv
from datetime import date
import os

def getprecios():
    if (not os.path.exists("../precios.csv")) or os.path.getsize("../precios.csv") == 0:
        createCSV()
    baseurl = 'https://www.mercadolibre.com.ar/ofertas?page='
    pagina = 1
    while pagina < 200:
        url=baseurl+str(pagina)
        f = csv.writer(open("precios.csv","a+",newline=''))
        resp = requests.get(url)
        soup = bs.BeautifulSoup(resp.text, "lxml")
        productos = soup.find_all('p', {'class':'promotion-item__title'})
        dirtyprecios = soup.find_all('span', {'class':'promotion-item__price'})
        links = soup.find_all('a', {'class':'promotion-item__link-container'})
        precios = []
        for precio in dirtyprecios:
            ps = precio.find_all('span')
            for p in ps:
                precios.append(p.text.strip())
        for i in range(len(productos)):
            linea = []
            linea.append(productos[i].text.strip())
            precio = precios[i]
            precio = precio.replace("$","")
            precio = precio.replace(".","")
            linea.append(precio)
            linea.append(date.today())
            linea.append(links[i]['href'])
            f.writerow(linea)
        print("pagina " + str(pagina))
        pagina+=1
            
def createCSV():
    f = csv.writer(open("precios.csv","w",newline=''))
    f.writerow(["producto","precio","fecha","link"])
            
    
getprecios()