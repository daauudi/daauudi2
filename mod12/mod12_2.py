import requests


API_AVAIN = "5500116c1716fb305b8e99d505d6b072"


paikkakunta = input("Anna paikkakunnan nimi: ")


try:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={paikkakunta}&appid={API_AVAIN}&units=metric&lang=fi"
    vastaus = requests.get(url)
    sää = vastaus.json()


    if sää["cod"] == 200:
        print("\nSäätiedot:")
        print(f"Paikkakunta: {sää['name']}")
        print(f"Sää: {sää['weather'][0]['description']}")
        print(f"Lämpötila: {sää['main']['temp']}°C")
    else:
        print("Virhe:", sää["message"])

except Exception as e:
    print("Jokin meni pieleen:", e)