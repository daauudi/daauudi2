
class Hissi:
    def __init__(self, alin_kerros, ylin_kerros):
        self.alin_kerros = alin_kerros
        self.ylin_kerros = ylin_kerros
        self.nykyinen_kerros = alin_kerros  # issi aloittaa alimmasta kerroksesta



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



def main():
    hissi = Hissi(1, 10)


    print("Testataan hissiä:")
    hissi.siirry_kerrokseen(5)
    hissi.siirry_kerrokseen(1)


if __name__ == "__main__":
    main()