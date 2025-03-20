import random

class Auto:
    def __init__(self, rekisteritunnus, huippunopeus):
        self.rekisteritunnus = rekisteritunnus
        self.huippunopeus = huippunopeus
        self.tämänhetkinen_nopeus = 0
        self.kuljettu_matka = 0

    def kiihdytä(self, muutos):
        self.tämänhetkinen_nopeus += muutos
        if self.tämänhetkinen_nopeus > self.huippunopeus:
            self.tämänhetkinen_nopeus = self.huippunopeus
        if self.tämänhetkinen_nopeus < 0:
            self.tämänhetkinen_nopeus = 0

    def kulje(self, tunnit):
        self.kuljettu_matka += self.tämänhetkinen_nopeus * tunnit


class Kilpailu:
    def __init__(self, nimi, pituus_km, autot):
        self.nimi = nimi
        self.pituus_km = pituus_km
        self.autot = autot


    def tunti_kuluu(self):
        for auto in self.autot:
            nopeuden_muutos = random.randint(-10, 15)
            auto.kiihdytä(nopeuden_muutos)
            auto.kulje(1)



    def tulosta_tilanne(self):
        print("\nkilpailun tilanne:")
        print("{:<10} {:<15} {:<15} {:<15}".format("rekisteri", "huippunopeus", "nopeus", "matka"))
        print("-" * 55)
        for auto in self.autot:
            print("{:<10} {:<15} {:<15} {:<15}".format(
                auto.rekisteritunnus,
                f"{auto.huippunopeus} km/h",
                f"{auto.tämänhetkinen_nopeus} km/h",
                f"{auto.kuljettu_matka} km"
            ))



    def kilpailu_ohi(self):
        for auto in self.autot:
            if auto.kuljettu_matka >= self.pituus_km:
                return True
        return False



def main():
    autot = []
    for i in range(1, 11):
        rekisteritunnus = f"ABC-{i}"
        huippunopeus = random.randint(100, 200)
        autot.append(Auto(rekisteritunnus, huippunopeus))

    kilpailu = Kilpailu("Suuri romuralli", 8000, autot)


    tunti = 0
    while not kilpailu.kilpailu_ohi():
        tunti += 1
        kilpailu.tunti_kuluu()
        if tunti % 10 == 0:
            kilpailu.tulosta_tilanne()


    print("\nKilpailu on päättynyt! Lopullinen tilanne:")
    kilpailu.tulosta_tilanne()


if __name__ == "__main__":
    main()