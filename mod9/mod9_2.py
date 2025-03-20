class Auto:
    def __init__(self, rekisteritunnus, huippunopeus,):
        self.rekisteritunnus = rekisteritunnus
        self.huippunopeus = 142
        self.tämänhetkinen_nopeus = 0
        self.kuljettu_matka= 0

    def kiihdyta(self, nopeuden_muutos):
        uusi_nopeus = self.tämänhetkinen_nopeus + nopeuden_muutos

        if uusi_nopeus >self.huippunopeus:
            self.tämänhetkinen_nopeus = self.huippunopeus

        elif uusi_nopeus < 0:
            self.tämänhetkinen_nopeus = 0

        else:
            self.tämänhetkinen_nopeus = uusi_nopeus

        return self.tämänhetkinen_nopeus






auto1= Auto("ABC-123",142)

nopeuden_muutos_list = [30,70,50]

for muutos in nopeuden_muutos_list:
    uusi_nopeus= auto1.kiihdyta(muutos)
    print(f"uusi_nopeus:{uusi_nopeus}km/h")

uusi_nopeus=auto1.kiihdyta(-200)
print(f"uusi nopeus hätäjarrutuksen jälkeen: {uusi_nopeus} km/h")






