from bs4 import BeautifulSoup
import requests
import re
import mysql.connector

city = input('Please enter the city:(Dear Corrector,Please enter "tehran")  ')
kind = input('Please enter the kind of property'
             '(for Example:apartment):  ')

## Web Scraping
res = requests.get('https://ihome.ir/sell-residential-'+kind+'/th-'+city+'/')
soup = BeautifulSoup(res.text, 'html.parser')
result = soup.find_all('div', attrs={'class':'col-12 col-m-6 col-lg-4 mt-4'})
home_list = []
for home in result:
    sample_home = []
    price = home.find('span', attrs={'itemprop':'price'}).text
    detail = home.find_all('span', attrs={'class':'property-detail__icons-item__value'})
    sample_home.append(price)
    for value in detail:
        sample_home.append(re.sub(r'\s+', ' ', value.text))
    home_list.append(sample_home)

for age in home_list:
    if (age[2]) == ' نوساز ' :
        age.remove(age[2])
        age.insert(2, '0')

db = mysql.connector.connect(host='localhost',
                             user='root',
                             password='',
                             database='ihome')
my_cursor = db.cursor()
drop_table = 'DROP TABLE IF EXISTS home'
my_cursor.execute(drop_table)
my_cursor.execute('CREATE TABLE home (bedroom VARCHAR(1), age VARCHAR(2), area VARCHAR(5), price VARCHAR(15))')

sql = ('INSERT INTO home(bedroom, age, area, price) VALUES (%s, %s, %s, %s)')
for i in range(0,24):
    val = (home_list[i][3], home_list[i][2], home_list[i][1], home_list[i][0])
    my_cursor.execute(sql, val)

## Take Input From User
area = input('What is the area of your property?\n')
age = input('What is the age of your property?\n')
bedroom = input('How many bedrooms does your property have?\n')

## Machine Learning
from sklearn import tree
my_cursor.execute('SELECT * FROM home')
rows = my_cursor.fetchall()
x = []
y = []
for row in rows:
    x.append(row[0:3])
    y.append(row[3:])
clf = tree.DecisionTreeClassifier()
clf = clf.fit(x, y)

new_data = [[bedroom, age, area]]
answer = clf.predict(new_data)
print('The price of the property you are looking for is:','ریال',int(answer),'in',city)