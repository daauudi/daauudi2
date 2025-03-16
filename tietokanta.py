import mysql.connector

# Pääohjelma
yhteys = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='flight_game',
         user='root',
         password='daauudi',
         collation= "utf8mb4_general_ci",
         autocommit=True
         )

sql = f"SELECT name FROM airport WHERE iso_country = 'FI'"
kursori = yhteys.cursor()
kursori.execute(sql)
tulos = kursori.fetchall()
for rivi in tulos:
    print(rivi)


