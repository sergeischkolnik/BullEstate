import argparse
import math
import sys

from lxml import html
import requests
import csvWrite as ew
import datetime
import time
from xlrd import open_workbook
import pandas
from matplotlib import pyplot as plt
plt.rcParams['figure.figsize'] = (16, 9)
plt.style.use('ggplot')
import numpy as np
from copy import deepcopy
import models

def normalize(v):
    norm = np.linalg.norm(v, ord=1)
    if norm == 0:
        norm = np.finfo(v.dtype).eps
    return v / norm

def getInfo(subsites,master):

    for j in range(0, len(subsites)):
        subMaster = []
        print(str(time.time()-startTime)+":" + str(subsites[j])+ " page nr:" + str(j+1))
        try:
            #print(str(time.time() - startTime) + ": getting subsite")
            page2 = requests.get(subsites[j], allow_redirects=True)
            #print(str(time.time() - startTime) + ": getting tree")
            tree2 = html.fromstring(page2.content)
        except:
            print("Many requests error.")
        lastRange = 25
        for i in range(1,lastRange+3):
           # print(str(time.time() - startTime) + ": parsing basic data")
            codeSite =  '//*[@id="wrapper"]/section[2]/div/div/div[1]/article/div[3]/div[' + str(i) + ']/div[2]/div/div[1]/p[2]'
            nameSite =  '//*[@id="wrapper"]/section[2]/div/div/div[1]/article/div[3]/div[' + str(i) + ']/div[2]/div/div[1]/h4/a'
            priceSite = '//*[@id="wrapper"]/section[2]/div/div/div[1]/article/div[3]/div[' + str(i) + ']/div[2]/div/div[2]/p/span'
            meterSite = '//*[@id="wrapper"]/section[2]/div/div/div[1]/article/div[3]/div[' + str(i) + ']/div[2]/div/div[3]/p/span'
            typeSite =  '//*[@id="wrapper"]/section[2]/div/div/div[1]/article/div[3]/div[' + str(i) + ']/div[2]/div/div[1]/p[1]/span'
            code = tree2.xpath(codeSite)
            if len(code) == 0:
                codeSite = '//*[@id="wrapper"]/section[2]/div/div/div[1]/article/div[3]/div[' + str(
                    i) + ']/div[2]/div/div[1]/p[3]'
                '//*[@id="wrapper"]/section[2]/div/div/div[1]/article/div[3]/div[1]/div[2]/div/div[1]/p[3]'
                code = tree2.xpath(codeSite)
            name = tree2.xpath(nameSite)
            price = tree2.xpath(priceSite)
            meters = tree2.xpath(meterSite)
            clase = tree2.xpath(typeSite)
            if len(code) > 0:
                aux = []
                code = (code[0]).text
                if "Código" not in code:
                    codeSite = '//*[@id="wrapper"]/section[2]/div/div/div[1]/article/div[3]/div[' + str(
                        i) + ']/div[2]/div/div[1]/p[3]'
                    code = tree2.xpath(codeSite)
                    code = (code[0]).text
                code = int(code[8:])
                aux.append(code)
                newLink = str((name[0]).attrib)
                operacion = newLink.split('/')[1]
                newLink = newLink[17:]
                newLink = newLink[:-4]
                newLink = 'http://www.portalinmobiliario.com/'+operacion+'/'+newLink
                name = (name[0]).text
                try:
                    price = (price[0]).text
                except:
                    continue
                price = str(price)
                price = price[2:]

                try:
                    price = float(price.replace('.', ''))
                except:
                    continue
                if len(meters) > 0:
                    meters = meters[0].text
                else:
                    meters = 'missing'
                if '-' in meters:
                    try:
                        meters = meters.split('-')
                        minMeters = (meters[0])[:-1]
                        maxMeters = (meters[1])[:-3]
                        maxMeters = maxMeters[1:]
                        minMeters = float(minMeters.replace(',','.'))
                        maxMeters = float(maxMeters.replace(',','.'))
                    except:
                        continue

                elif 'missing' in meters:
                    minMeters = -1
                    maxMeters = -1
                else:
                    meters = meters[:-3]
                    try:
                        meters = float(meters.replace(',','.'))
                    except:
                        continue
                    minMeters = meters
                    maxMeters = meters
                meanMeters = (minMeters+maxMeters)/2.0

                clase = clase[0].text
                clase=clase[:-2]

                try:
                   # print(str(time.time() - startTime) + ": Getting microsite")
                    page3 = requests.get(newLink, allow_redirects=True)
                   # print(str(time.time() - startTime) + ": Getting tree")
                    tree3 = html.fromstring(page3.content)
                except:
                    print("Request error")
                print(str(subsites[j]) + " " + str(j+1) + "." + str(i))
              #  print(str(time.time() - startTime) + ": Parsing microsite")
                addresSite = '//*[@id="wrapper"]/section/div/div/div[1]/article/div/div[2]/div[1]/div[2]/div[1]/div/div/p[3]/span[1]'
                address = tree3.xpath(addresSite)
                if len(address) == 0:
                    addresSite = '//*[@id="wrapper"]/section/div/div/div[1]/article/div/div[2]/div[2]/div[2]/div[1]/p/span[1]'
                    address = tree3.xpath(addresSite)
                if len(address) == 0:
                    addresSite = '//*[@id="project-location"]/div/div/div[1]/div/div[1]/p/span[1]'
                    address = tree3.xpath(addresSite)
                if len(address) > 0:
                    try:
                        address = address[0].text
                    except AttributeError:
                        address = '-'
                else:
                    address = '-'

                latSite = '/html/head/meta[18]'
                lat = tree3.xpath(latSite)
                if len(lat) > 0:
                    lat = str((lat[0]).attrib).split(':')
                    lat = lat[3]
                    lat = (lat[2:])[:-2]

                    try:
                        lat = float(lat)
                    except:
                        continue

                else:
                    lat = -1

                lonSite = '/html/head/meta[19]'
                lon = tree3.xpath(lonSite)
                if len(lon) > 0:
                    lon = (((str((lon[0]).attrib).split(':'))[3])[2:])[:-2]
                    try:
                        lon= float(lon)
                    except:
                        continue
                else:
                    lon = -1

                dormSite = '//*[@id="wrapper"]/section/div/div/div[1]/article/div/div[2]/div[2]/div[2]/div[2]/p/text()[1]'
                dorms = tree3.xpath(dormSite)

                try:
                    if len(dorms) > 0:

                        dorms=str(dorms)
                        dorms=dorms[2]
                        dorms=float(dorms)
                    else:
                        dormSite = '//*[@id="project-features"]/div/div/div[2]/span[2]/em'
                        dorms = tree3.xpath(dormSite)
                        if len(dorms) > 0:
                            dorms = dorms[0].text
                            dorms =dorms[0]
                            dorms = float(dorms)
                        else:
                            dorms = '-'
                except AttributeError:
                    dorms = '-'

                bathSite = '//*[@id="wrapper"]/section/div/div/div[1]/article/div/div[2]/div[2]/div[2]/div[2]/p/text()[2]'
                baths = tree3.xpath(bathSite)

                try:
                    if len(baths) > 0:
                        baths = str(baths)
                        baths = baths[2]
                        baths = float(baths)
                    else:
                        bathSite = '//*[@id="project-features"]/div/div/div[3]/span[2]/em'
                        baths = tree3.xpath(bathSite)
                        if len(baths) > 0:
                            baths = baths[0].text
                            baths = baths [0]
                            baths = float(baths)
                        else:
                            baths = '-'
                except AttributeError:
                    baths = '-'

                dateSite = '//*[@id="wrapper"]/section/div/div/div[1]/article/div/div[2]/div[1]/div[1]/div[2]/p[2]/strong'
                date = tree3.xpath(dateSite)
                if len(date) > 0:
                    date = date[0].text
                    date=date[11:]
                else:
                    date = '-'

                pxm=float(price/minMeters)

                #obtencion de tipo y comuna:

                comuna = (newLink.split('/')[5]).split('?')[0]

                tipo = newLink.split('/')[4]
                if tipo=="do" or tipo=="do-de-temporada":
                    comuna = (newLink.split('/')[6]).split('?')[0]
                    tipo = newLink.split('/')[5]

                #print(str(time.time() - startTime) + ": Creating tuple")
                aux.append(name)
                aux.append(price)
                aux.append(minMeters)
                aux.append(maxMeters)
                aux.append(meanMeters)
                aux.append(pxm)
                aux.append(address)
                aux.append(clase)
                aux.append(lat)
                aux.append(lon)
                aux.append(dorms)
                aux.append(baths)
                aux.append(date)
                aux.append(newLink)
                aux.append(operacion)
                aux.append(comuna)
                aux.append(tipo)

                master.append(aux)
                subMaster.append(aux)
            else:
                print("ERROR")
            #print(str(time.time() - startTime) + ": Done")
        models.save(subMaster)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Single scraper')
    parser.add_argument('-l', '--lugar', help='lugar:(0) todo, (1) metropolitana, (2) resto', type=int, default=0)
    parser.add_argument('-o', '--operacion', help='Operacion:(0) todo (1) venta, (2) arriendo', type=int, default=0)
    parser.add_argument('-t', '--tipo', help='tipo: (0) todo, (1) depto, (2) casa, (3) resto', type=int, default=0)

    args = parser.parse_args()

    #lista de operaciones segun parametros
    opList = []
    if args.operacion == 0:
        opList = ['venta','arriendo']
    elif args.operacion == 1:
        opList = ['venta']
    elif args.operacion == 2:
        opList = ['arriendo']
    else:
        print("ERROR DE PARAMETRO DE OPERACION: DEBE SER 0, 1 o 2.")
        sys.exit(0)

    #lista de lugares segun parametros
    placeList = []
    if args.lugar == 0:
        placeList = ['arica-y-parinacota','tarapaca','antofagasta','atacama','coquimbo',
                       'bernardo-ohiggins','maule','biobio','la-araucania','de-los-rios','los-lagos','aysen',
                       'magallanes-y-antartica-chilena','valparaiso','metropolitana']
    elif args.lugar == 1:
        placeList = ['metropolitana']
    elif args.lugar == 2:
        placeList = ['arica-y-parinacota','tarapaca','antofagasta','atacama','coquimbo',
                       'bernardo-ohiggins','maule','biobio','la-araucania','de-los-rios','los-lagos','aysen',
                       'magallanes-y-antartica-chilena','valparaiso']
    else:
        print("ERROR DE PARAMETRO DE LUGAR: DEBE SER 0, 1 o 2.")
        sys.exit(0)

    #lista de tipo
    tipoList = []
    if args.tipo == 0:
        tipoList = ['casa','departamento','oficina','sitio','comercial','agricola','loteo','bodega','parcela',
                    'estacionamiento','terreno-en-construcción']
    elif args.tipo == 1:
        tipoList = ['departamento']
    elif args.tipo == 2:
        tipoList = ['casa']
    elif args.tipo == 3:
        tipoList = ['oficina','sitio','comercial','agricola','loteo','bodega','parcela',
                    'estacionamiento','terreno-en-construcción']
    else:
        print("ERROR DE PARAMETRO DE TIPO: DEBE SER 0, 1 , 2 o 3.")
        sys.exit(0)

    print(str(datetime.datetime.now()))
    step = 1
    startTime = time.time()

    collection = []
    for n1 in opList:
        for n2 in tipoList:
            for n3 in placeList:
                collection.append("http://www.portalinmobiliario.com/"+n1+"/"+n2+"/"+n3+"?tp=6&op=2&ca=3&ts=1&dd=0&dh=6&bd=0&bh=6&or=&mn=1&sf=0&sp=0&pg=1")

    cycle = 0
    while True:

        for collectElement in collection:

            # TESTING
            oneTesting = False
            if oneTesting:
                collectElement = 'http://www.portalinmobiliario.com/venta/departamento/metropolitana?tp=6&op=2&ca=3&ts=1&dd=0&dh=6&bd=0&bh=6&or=&mn=1&sf=0&sp=0&pg=1'
            # ENDTESTING

            print("SITE:" + collectElement)
            try:
                page2 = requests.get(collectElement, allow_redirects=True)
                tree2 = html.fromstring(page2.content)
            except:
                print("Request error")
            paginas = tree2.xpath('//*[@id="wrapper"]/section[2]/div/div/div[1]/article/div[1]/div[1]/div/div/text()[1]')
            if len(paginas) == 0:
                continue

            pagsplit = (str(paginas[0]).split())[2]
            nrOfPubs = int(pagsplit.replace(".", ""))

            nrOfPbsPerPage = 25

            nrPages = math.ceil(nrOfPubs/nrOfPbsPerPage)

            subsites = []
            subsiteBasicUrl = (collectElement)[:-1]
            for i in range(1,nrPages+1):
                subsites.append(subsiteBasicUrl + str(i))

            last = nrOfPubs % 25
            if last == 0:
                last = 25


            fileName = collectElement.split('?')
            fileName = fileName[0].split('/')
            fileName = fileName[3]+'_'+fileName[4]+'_'+fileName[5]

            master = []
            #titles = ["id", "Nombre", "Precio", "minMet", "maxMet", "promM","Precio/m2", "direc" ,"tipo", "lat", "lon", "dorms", "banios", "fecha", "link"]
            #master.append(titles)

            getInfo(subsites, master)
            ctime = time.strftime("%H_%M")
            cdate = time.strftime("%Y_%m_%d")
            fileName += '_' + cdate + '_' + ctime

            #models.save(master)
            #ew.write(master, fileName)

            # df = pandas.read_excel(fileName+".xlsx", sheet_name='Sheet1')
            # print (df.columns)
            # values=df['id'].values
            # df=pandas.DataFrame(df,df.index)
            # df.drop(df.columns[[0, 1, 3,4,6,7,8,11,12,13,14]], axis=1, inplace=True)
            #
            # print(df)
            #
            # Preciol = df['Precio'].values
            # promMl = df['promM'].values
            # latl = df['lat'].values
            # lonl = df['lon'].values
            #
            # Precion=normalize(Preciol)
            # promMn=normalize(promMl)
            # latn=normalize(latl)
            # lonn=normalize(lonl)
            # print(Precion,promMn,latn,lonn)

        cycle += 1