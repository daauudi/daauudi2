
class Hissi:
    def __init__(self, alin_kerros, ylin_kerros):
        self.alin_kerros = alin_kerros
        self.ylin_kerros = ylin_kerros
        self.nykyinen_kerros = alin_kerros


    def siirry_kerrokseen(self, kohdekerros):
        while self.nykyinen_kerros < kohdekerros:
            self.kerros_ylös()
        while self.nykyinen_kerros > kohdekerros:
            self.kerros_alas()
        print(f"Hissi on nyt kerroksessa {self.nykyinen_kerros}.")


    def kerros_ylös(self):
        if self.nykyinen_kerros < self.ylin_kerros:
            self.nykyinen_kerros += 1
            print(f"Hissi nousi kerrokseen {self.nykyinen_kerros}.")
        else:
            print(f"Hissi on jo ylimmässä kerroksessa ({self.ylin_kerros}).")


    def kerros_alas(self):
        if self.nykyinen_kerros > self.alin_kerros:
            self.nykyinen_kerros -= 1
            print(f"Hissi laski kerrokseen {self.nykyinen_kerros}.")
        else:
            print(f"Hissi on jo alimmassa kerroksessa ({self.alin_kerros}).")


class Talo:
    def __init__(self, alin_kerros, ylin_kerros, hissien_lukumaara):
        self.alin_kerros = alin_kerros
        self.ylin_kerros = ylin_kerros
        self.hissit = []
        for i in range(hissien_lukumaara):
            hissi = Hissi(alin_kerros, ylin_kerros)
            self.hissit.append(hissi)



    def aja_hissia(self, hissin_numero, kohdekerros):
        if 0 <= hissin_numero < len(self.hissit):
            print(f"\najetaan hissiä {hissin_numero + 1} kerrokseen {kohdekerros}:")
            self.hissit[hissin_numero].siirry_kerrokseen(kohdekerros)
        else:
            print(f"Hissiä {hissin_numero + 1} ei ole talossa.")



    def palohalytys(self):
        print("\nPALOHÄLYTYS! kaikki hissit siirtyvät pohjakerrokseen.")
        for hissi in self.hissit:
            hissi.siirry_kerrokseen(self.alin_kerros)



def main():
    talo = Talo(1, 10, 3)


    print("testataan talon hissejä:")
    talo.aja_hissia(0, 5)  # Ajetaan hissi 1 kerrokseen 5
    talo.aja_hissia(1, 3)  # Ajetaan hissi 2 kerrokseen 3
    talo.aja_hissia(2, 9)  # Ajetaan hissi 3 kerrokseen 9


    talo.palohalytys()


if __name__ == "__main__":
    main()