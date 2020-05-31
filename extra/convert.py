import os,sys
import csv
# from itertools import izip_longest #for python 2
from itertools import zip_longest #for python 3

rawFile = './raw_data/dataWed May 27 2020 23_57_52 GMT+0530 (India Standard Time).csv'
newfilePath = './raw_data/dataWed May 27 2020 23_57_52 GMT+0530 (India Standard Time)_training_dataset.csv'

def removeSpace(data):
    try:
        data.remove('')
    except Exception as e:
        print(e)
    return data

with open(rawFile) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    allData = list(readCSV)
    xColumn = []
    yColumn = []
    zColumn = []
    for x,y,z in zip(allData[0::3],allData[1::3],allData[2::3]):
        try:
            print(x)
            x.pop(0)
            y.pop(0)
            z.pop(0)
            xColumn.extend(x)
            yColumn.extend(y)
            zColumn.extend(z)
        except Exception as error:
            print(error)
    print(xColumn)
    xColumn = removeSpace(xColumn)
    yColumn = removeSpace(yColumn)
    zColumn = removeSpace(zColumn)
    clmn = [xColumn, yColumn, zColumn]
    data = zip_longest(*clmn, fillvalue = '')
    with open(newfilePath, 'w', encoding="ISO-8859-1", newline='') as trainCsv:
        write = csv.writer(trainCsv)
        write.writerow(("Gx", "Gy","Gz"))
        write.writerows(data)
    trainCsv.close()