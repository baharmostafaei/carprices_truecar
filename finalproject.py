from bs4 import BeautifulSoup
import requests
import mysql.connector
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn import tree
from sklearn.preprocessing import LabelEncoder
links = []
cnt = 1
while cnt <= 30:
    urls = f'https://www.truecar.com/used-cars-for-sale/listings/?page={cnt}'
    links.append(urls)
    cnt = cnt + 1
names_list  = []
price_list = []
miles_list = []
for link in links:
    req = requests.get(link)
    soup = BeautifulSoup(req.text, 'html.parser')
    for a in soup.find_all('div', attrs= {'class':'card-content order-3 vehicle-card-body'}):
        name = a.find('span', attrs= {'class':'truncate'})
        names_list.append(name.text)
        price = a.find('div', attrs= {'class':'heading-3 my-1 font-bold'})
        price = str(price.text)
        price = price[1:]
        price = price.replace(',', '')
        price_list.append((price))        
    for ba in soup.find_all('div', attrs= {'class': 'mt-2-5 w-full border-t pt-2-5'}):
        mile = ba.find('div', attrs= {'class': 'truncate text-xs'})
        mile = str(mile.text).split()
        miles_list.append((mile[0]).replace(',', ''))
values = list(zip(names_list, price_list, miles_list))
mydb = mysql.connector.connect(user = 'root',
                               host = 'localhost',
                               password= 'bahare1383cs',
                               database = 'truecar')
mycursor = mydb.cursor()
sql = "INSERT IGNORE INTO cars_info (carsname, carsprice, carsmile) VALUES (%s, %s, %s)"
mycursor.executemany(sql, values)
mydb.commit()
# print(mycursor.rowcount, "rows inserted.")
clf = tree.DecisionTreeClassifier()
x , y = [] , [] 
with mydb.cursor() as cursor : 
    cursor.execute('SELECT * FROM cars_info ')
    all_data = cursor.fetchall()
    for thing in all_data :
        x.append((thing[2], thing[3]))
        y.append(thing[1])
le = LabelEncoder()
my_list = []
for thing in x :  
    my_list.extend(thing)
user_price = input('insert the price for your desired car (JUST DIGITS WITH NO "$" "," "." ) : ')
user_mile = input('insert the mile(JUST DIGITS WITH NO "," "." ): ')
my_list.extend((user_price, user_mile))
my_list = list(le.fit_transform(my_list))
x = list()
for thing in my_list[:] :
    x.append((my_list.pop(0), my_list.pop(0)))
    if len(my_list) == 2 :
        my_list.append((my_list.pop(0), my_list.pop(0)))
        break 
clf.fit(x, y)
print(clf.predict(my_list))

