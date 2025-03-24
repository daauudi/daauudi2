
class julkaisu:
    def __init__(self,nimi,):
        self.nimi=nimi


    def tulosta_tiedot(self):
        print(f"nimi: {self.nimi}")


class kirja(julkaisu):
    def __init__(self, nimi, kirjoittaja, sivumäärä):
        super().__init__(nimi)
        self.kirjoittaja = kirjoittaja
        self.sivumäärä = sivumäärä

    def tulosta_tiedot(self):
        print(f"kirjoittaja: {self.kirjoittaja}")
        print(f"sivumäärä: {self.sivumäärä}")
        super().tulosta_tiedot()




class lehti(julkaisu):
    def __init__(self,nimi, päätoimittaja):
        self.päätoimittaja= päätoimittaja
        super().__init__(nimi)


    def tulosta_tiedot(self):
        print(f"nimi: {self.päätoimittaja}")
        super().tulosta_tiedot()



aku= lehti("aku ankka","aki hyyppä")
kirja= kirja("hytti n:o6","rosa liksom",200)

print("lehden tiedot: ")
aku.tulosta_tiedot()
print("\nkirjan tiedot: ")
kirja.tulosta_tiedot()
