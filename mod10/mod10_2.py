
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
        print(f"hissi on nyt kerroksessa {self.nykyinen_kerros}.")


    def kerros_ylös(self):
        if self.nykyinen_kerros < self.ylin_kerros:
            self.nykyinen_kerros += 1
            print(f"hissi nousi kerrokseen {self.nykyinen_kerros}.")
        else:
            print(f"hissi on jo ylimmässä kerroksessa ({self.ylin_kerros}).")


    def kerros_alas(self):
        if self.nykyinen_kerros > self.alin_kerros:
            self.nykyinen_kerros -= 1
            print(f"hissi laski kerrokseen {self.nykyinen_kerros}.")
        else:
            print(f"hissi on jo alimmassa kerroksessa ({self.alin_kerros}).")


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
            print(f"hissiä {hissin_numero + 1} ei oo talossa.")



def main():

    talo = Talo(1, 10, 3)

    print("testataan talon hissejä:")
    talo.aja_hissia(0, 5)
    talo.aja_hissia(1, 3)
    talo.aja_hissia(2, 9)
    talo.aja_hissia(0, 1)


if __name__ == "__main__":
    main()