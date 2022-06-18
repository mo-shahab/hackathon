import lxml.html as lh
from time import sleep
import pandas as pd
import numpy as np
import requests
import bs4
from bs4 import BeautifulSoup

def stock_data():
    r = requests.get("https://www.moneycontrol.com/stocks/marketstats/indexcomp.php?optex=NSE&opttopic=indexcomp&index=9")
    soup = BeautifulSoup(r.text, 'html.parser')
    
    doc = lh.fromstring(r.content)
    tr_elements = doc.xpath('//tr')
    
    col=[]
    i=0
    for t in tr_elements[1]:
        i+=1
        name=t.text_content()
        #print('%d:"%s"'%(i,name))
        col.append((name,[]))
    
    col[0] = ('Company Name', [])

    #Since out first row is the header, data is stored on the second row onwards
    for j in range(1,len(tr_elements)):
        #T is our j'th row
        T=tr_elements[j]

        #If row is not of size 6, the //tr data is not from our table 
        if len(T)!=6:
            break

        #i is the index of our column
        i=0
        
        #Iterate through each element of the row
        for t in T.iterchildren():
            data=t.text_content() 

            #Check if row is empty
            if i>0:
            #Convert any numerical value to integers
                try:
                    data=int(data)
                except:
                    pass
            
            #Append the data to the empty list of the i'th column
            col[i][1].append(data)
            #Increment i for the next column
            i+=1
            
    Dict={title:column for (title,column) in col}
    df=pd.DataFrame(Dict)
    df = df.drop(df.index[[0]])
    return df

data = stock_data()
#print(data.head(10))


#function to print the data scraped from the website every 30 seconds for the next 'x' minutes
def print_stock_data(x):

    flag = True
    counter = 0
    refreshRate = 30
    
    while flag:
        print("===========================================================\n")
        print(stock_data())
        sleep(refreshRate)
        counter +=1
        if (counter == (x*2)):
            flag = False
            
            
print_stock_data(1)

#function that alerts if a % change is over a given threshold in a 2 minute period
def change_alert(threshold):
    data1 = stock_data()
    a1 = [float(s) for s in data1[["%Chg"]].values]
    a1 = np.asarray(a1)
    
    sleep(120)
    
    data2 = stock_data()
    a2 = [float(s) for s in data2[["%Chg"]].values]
    a2 = np.asarray(a2)
    
    i=0
    for i in range(len(a2)):
        diff = a2[i] - a1[i]
        count = 0
        if abs(diff)>=threshold:
            count +=1
            if diff>0:
                print("\nAlert: Company %s has gone down!", data2["Company Name"][index[i]])
            else:
                print("\nAlert: Company %s has gone up!", data2["Company Name"][index[i]])
    if count == 0:
        print("Everything is fine. No market fluctuation.")
