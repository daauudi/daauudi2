import mysql.connector
import random
import geopy.distance

yhteys = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='flight_game',
    user='root',
    password='daauudi',
    collation="utf8mb4_general_ci",
    autocommit=True
)


icao_koodi = input("Anna lentoaseman ICAO-koodi: ")


kursori = yhteys.cursor()
kursori.execute(f"SELECT name, municipality FROM airport WHERE ident = '{icao_koodi}'")
tulos = kursori.fetchone()

if tulos:
    print("Lentokentän nimi:", tulos[0])
    print("Sijaintikunta:", tulos[1])
else:
    print("ICAO-koodilla ei löytynyt lentokenttää.")


yhteys.close()
