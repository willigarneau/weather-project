# Laboratoire 8 en Linux
# Apprentissage des API REST avec Python
# Objectif : Afficher la météo de différentes villes dans le monde

# Par William Garneau et Pascal Canuel
# 03/26/2018


import requests
import psycopg2
import datetime
from city import City
from color import Color

try:
    conn = psycopg2.connect("dbname='Weather_Project' user='General' host='10.2.0.31' password='123'")
except:
    print("I am unable to connect to the database")

cur = conn.cursor()
dt = datetime.datetime.now()

cities = {"Tokyo": "http://api.openweathermap.org/data/2.5/weather?id=1850147&APPID=f3b38c4b98d7b339fcc2175d587d5e86",
          "Berlin": "http://api.openweathermap.org/data/2.5/weather?id=2950159&APPID=f3b38c4b98d7b339fcc2175d587d5e86",
          "Toronto": "http://api.openweathermap.org/data/2.5/weather?id=6167865&APPID=f3b38c4b98d7b339fcc2175d587d5e86",
          "Paris": "http://api.openweathermap.org/data/2.5/weather?id=6455259&APPID=f3b38c4b98d7b339fcc2175d587d5e86",
          "New York": "http://api.openweathermap.org/data/2.5/weather?id=5128581&APPID=f3b38c4b98d7b339fcc2175d587d5e86",
          "Yellowknife": "http://api.openweathermap.org/data/2.5/weather?id=6185377&APPID=f3b38c4b98d7b339fcc2175d587d5e86",
          "Kuwait": "http://api.openweathermap.org/data/2.5/weather?id=285787&APPID=f3b38c4b98d7b339fcc2175d587d5e86"}

for key, value in cities.items():
    print(key + " " + value)

    resultat = requests.get(cities[key])

    resultat_json = resultat.json()

    tempC = resultat_json['main']['temp'] - 273.15

    tempC = round(tempC, 2)

    c = City(resultat_json['coord']['lon'], resultat_json['coord']['lat'])
    c.tempC = tempC
    c.name = key

    cities[key] = c

    try:
        #cur.execute("""DELETE FROM public."MoyenneTemp" """)

        cur.execute("""
             INSERT INTO public."MoyenneTemp" ("nameCity", "tempMoy", "tempsConnection")
             VALUES (%s, %s, %s);
             """, (key, tempC, dt))

        cur.execute("""SELECT "tempMoy" FROM public."MoyenneTemp" where "nameCity" = (%s)""", (key,))
        rows = cur.fetchall()

        moy = 0
        for row in rows:
            moy = moy + row[0]

        moyF = (float(moy) + c.tempC) / (len(rows) + 1)
        #print(moyF)

        cur.execute("""DELETE from public."MoyenneGenerale" where "City" = (%s)""", (key,))
        cur.execute("""
                     INSERT INTO public."MoyenneGenerale" ("Moy", "City")
                     VALUES (%s, %s);
                     """, (round(moyF, 2), key))

    except:
        print("I can't insert")

#rows = cur.fetchall()
#print(rows)

##cur.execute("""DELETE FROM public."MoyenneTemp" """)

conn.commit()

cur.close()
conn.close()

from tkinter import *

gui = Tk()

gui.title = 'Weather_Project'

canvas = Canvas(gui, width =1920, height =967)

#entry = Entry(canvas)

canvas.pack(expand=YES, fill=BOTH)
photo = PhotoImage(file ='platecarre.png')
canvas.create_image(0, 0, image = photo, anchor=NW)


col = Color()

for key, value in cities.items():
    # Nom de la ville sur la map
    lbl_temp = Label(
        text=str(value.tempC),
        width=0,
        fg='#AAA', bg='#000')
    canvas.create_window(value.x, value.y,anchor=NE,
                              window=lbl_temp)
    # Temperature de la ville sur la map
    couleur = col.tempToColor(value.tempC)
    lbl_ville = Label(
        text=value.name,
        width=0,
        fg='#000', bg=couleur)
    canvas.create_window(value.x, value.y, anchor=NW,
                              window=lbl_ville)

x = 0
y = 967
space = 30
for key, value in col.tabColor.items():
    canvas.create_rectangle(x, y, x + space, y + space, fill = value)
    canvas.create_text(x + 15, y + 40, fill ='black', font ='Times 10', text = str(key))
    x = x + space
gui.mainloop()



# liste des villes
"""
import json

with open('data') as json_data:
    d = json.load(json_data)

from tkinter import *

master = Tk()

listbox = Listbox(master)


listbox.insert(END, "a list entry")

for ville in d:
    listbox.insert(END, ville['name'])
listbox.pack()
mainloop()
"""



