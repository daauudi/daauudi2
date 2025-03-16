import mysql.connector


yhteys = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='flight_game',
    user='root',
    password='daauudi',
    collation="utf8mb4_general_ci",
    autocommit=True
)


maakoodi = input("Anna maakoodi: ")


kursori = yhteys.cursor()
kursori.execute(f"SELECT type, COUNT(*) FROM airport WHERE iso_country = '{maakoodi}' GROUP BY type")
tulokset = kursori.fetchall()


for rivi in tulokset:
    print(f"{rivi[0]}: {rivi[1]} kpl")

yhteys.close()
