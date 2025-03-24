class Auto:
    def __init__(self,rekisteritunnus,huippunopeus):
        self.rekisteritunnus = rekisteritunnus
        self.huippunopeus = huippunopeus
        self.tämänhetkinen_nopeus = 0
        self.kuljettu_matka = 0

    def aja(self, tuntia):
        self.kuljettu_matka += self.tämänhetkinen_nopeus * tuntia


class sähköauto(Auto):
    def __init__(self,rekisteritunnus,huippunopeus,akkukapasiteetti):
        super().__init__(rekisteritunnus, huippunopeus)
        self.akkukapasiteetti = akkukapasiteetti


class polttomoottoriauto(Auto):
    def __init__(self,rekisteritunnus,huippunopeus,tankin_koko):
        super().__init__(rekisteritunnus,huippunopeus)
        self.tankin_koko = tankin_koko



sähköauto = sähköauto("ABC-15", 180, 52.5)
polttomoottoriauto = polttomoottoriauto("ACD-123", 165, 32.3)


sähköauto.tämänhetkinen_nopeus = 120
polttomoottoriauto.tämänhetkinen_nopeus = 100


sähköauto.aja(3)
polttomoottoriauto.aja(3)


print(f"sähköauton {sähköauto.rekisteritunnus} matkamittari: {sähköauto.kuljettu_matka} km")
print(f"polttomoottoriauton {polttomoottoriauto.rekisteritunnus} matkamittari: {polttomoottoriauto.kuljettu_matka} km")