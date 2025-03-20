

class auto:
    def __init__(self, rekisteritunnus, huippunopeus,):
        self.rekisteritunnus = "ABC-123"
        self.huippunopeus = 142
        self.tämänhetkinen_nopeus = 0
        self.kuljettu_matka= 0

auto1= auto("ABC-123",142)

print(f"rekisteritunnus:{auto1.rekisteritunnus}")
print(f"huippunopeus:{auto1.huippunopeus}km/h")
print(f"tämänhetkinen nopeus:{0}km/h")
print(f"kuljettu matka:{0}km")

