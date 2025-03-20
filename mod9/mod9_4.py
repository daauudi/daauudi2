import random

class Auto:
    def __init__(self, rekisteritunnus, huippunopeus, ):
        self.rekisteritunnus = rekisteritunnus
        self.huippunopeus = huippunopeus
        self.tämänhetkinen_nopeus = 0
        self.kuljettu_matka = 0

    def kiihdyta(self, nopeuden_muutos):
        uusi_nopeus = self.tämänhetkinen_nopeus + nopeuden_muutos

        if uusi_nopeus > self.huippunopeus:
            self.tämänhetkinen_nopeus = self.huippunopeus

        elif uusi_nopeus < 0:
            self.tämänhetkinen_nopeus = 0

        else:
            self.tämänhetkinen_nopeus = uusi_nopeus

        return self.tämänhetkinen_nopeus

    def kulje(self, tunnit):
        self.kuljettu_matka += tunnit * self.tämänhetkinen_nopeus




def main():

    autot = []
    for i in range(1, 11):
        rekisteritunnus = f"ABC-{i}"
        huippunopeus = random.randint(100, 200)
        autot.append(Auto(rekisteritunnus, huippunopeus))

    kilpailu_kaynnissa = True
    tunti = 0

    while kilpailu_kaynnissa:
        tunti += 1
        print(f"\ntunti {tunti}:")


        for auto in autot:
            nopeuden_muutos = random.randint(-10, 15)
            auto.kiihdyta(nopeuden_muutos)
            auto.kulje(1)


            print(f"{auto.rekisteritunnus}: {auto.kuljettu_matka} km, nopeus: {auto.tämänhetkinen_nopeus} km/h")


        for auto in autot:
            if auto.kuljettu_matka >= 10000:
                kilpailu_kaynnissa = False
                break


    print("\nkilpailu päättyi! lopputulokset:")
    print("{:<10} {:<15} {:<15} {:<15}".format("rekisteri", "huippunopeus", "Nopeus", "Matka"))
    print("-" * 55)
    for auto in autot:
        print("{:<10} {:<15} {:<15} {:<15}".format(
            auto.rekisteritunnus,
            f"{auto.huippunopeus} km/h",
            f"{auto.tämänhetkinen_nopeus} km/h",
            f"{auto.kuljettu_matka} km"
        ))


if __name__ == "__main__":
    main()