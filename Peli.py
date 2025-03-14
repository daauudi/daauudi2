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

tavarat_lista = ["Matkalaukku", "Passi", "Reppu", "Tietokone", "Puhelin", "Aurinkolasit"]


def hae_lentokentat():
    sql = "SELECT ident, name, latitude_deg, longitude_deg FROM airport WHERE iso_country = 'FI'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    return kursori.fetchall()


def hae_lähimmät_lentokentat(nykyinen_koord, max_etäisyys):
    kaikki_kentät = hae_lentokentat()
    return [kenttä for kenttä in kaikki_kentät if
            laske_etaisyys(nykyinen_koord, (kenttä[2], kenttä[3])) <= max_etäisyys]


def valitse_satunnaiset_tavarat(lentokentat):
    lähimmät_kentät = hae_lähimmät_lentokentat((60.3172, 24.9633), 100)  # Helsinki-Vantaa referenssipisteenä
    satunnaiset_kentat = random.sample(lähimmät_kentät, min(3, len(lähimmät_kentät)))
    return [(kenttä, tavarat_lista[i]) for i, kenttä in enumerate(satunnaiset_kentat)]


def laske_etaisyys(koord1, koord2):
    return geopy.distance.distance(koord1, koord2).km


def tulosta_tavaratiedot(tavarat):
    print("Tervetuloa ETSI TAVARAT -peliin! Etsi seuraavat tavarat lentokentiltä:")
    for i, (kenttä, tavara) in enumerate(tavarat, 1):
        print(f"Tavara {i}: {tavara} sijaitsee lentokentällä {kenttä[1]} (lat: {kenttä[2]}, lon: {kenttä[3]})")


def peli():
    lentokentat = hae_lentokentat()
    tavarat = valitse_satunnaiset_tavarat(lentokentat)
    tulosta_tavaratiedot(tavarat)
    sijainti = next(k for k in lentokentat if k[0].strip().upper() == "EFHK")
    loydetyt = []
    vuorot = 0
    kokonaismatka = 0

    while len(loydetyt) < len(tavarat):
        print(f"\nOlet lentokentällä: {sijainti[1]} ({sijainti[0]})")
        lähimmät = hae_lähimmät_lentokentat((sijainti[2], sijainti[3]), 100)
        print("Lähimmät lentoasemat (100 km säteellä):")
        for kenttä in lähimmät:
            print(
                f"{kenttä[0]} - {kenttä[1]} ({laske_etaisyys((sijainti[2], sijainti[3]), (kenttä[2], kenttä[3])):.2f} km)")

        valinta = input("Valitse seuraava lentokenttä (ICAO-koodi, tai 'exit' poistuaksesi): ").strip().upper()

        if valinta == "EXIT":
            print("Peli päättyi. Kiitos pelaamisesta!")
            return

        seuraava = next((k for k in lentokentat if k[0].strip().upper() == valinta), None)

        if seuraava and seuraava in lähimmät:
            etaisyys = laske_etaisyys((sijainti[2], sijainti[3]), (seuraava[2], seuraava[3]))
            kokonaismatka += etaisyys
            vuorot += 1
            sijainti = seuraava

            for i, (kenttä, tavara) in enumerate(tavarat):
                if seuraava[0] == kenttä[0] and kenttä not in loydetyt:
                    loydetyt.append(kenttä)
                    print(f"Löysit tavaran {tavara} lentokentältä {kenttä[1]}!")
                    break
        else:
            print("Virheellinen ICAO-koodi tai kenttä ei ole 100 km säteellä. Yritä uudelleen.")

    co2_päästöt = kokonaismatka * 0.133  # Keskimääräinen CO2-päästö per km lentämällä
    print("\nOnneksi olkoon! Löysit kaikki tavarat!")
    print(f"Vuoroja käytetty: {vuorot}")
    print(f"Kokonaismatka: {kokonaismatka:.2f} km")
    print(f"Hiilijalanjälki: {co2_päästöt:.2f} kg CO2")


peli()
