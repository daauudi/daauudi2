

import mysql.connector
import random
import geopy.distance
from rich import print
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress
from rich.prompt import Prompt
from rich.text import Text
from rich.columns import Columns
from time import sleep
from datetime import datetime
from rich import box

# Tietokantayhteys
yhteys = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='flight_game',
    user='root',
    password='daauudi',
    collation="utf8mb4_general_ci",
    autocommit=True
)
tavara_emojit = {
    "matkalaukku": "🧳",
    "passi": "📘",
    "kartta": "🗺️",
    "kamera": "📷",
    "lompakko": "👛",
    "aurinkolasit": "😎",
    "reppu": "🎒",
    "tabletti": "📱",
    "avainnippu": "🔑",
    "lääkepakkaus": "💊",
    "sateenvarjo": "☂️",
    "kaupunkikirja": "📖",
    "lentolippu": "🎫",
    "kännykkälaturi": "🔌",
    "koruarkku": "💎",
    "viinipullo": "🍷",
    "mokkakannu": "☕",
    "dronen": "🚁"
}


def hae_lentokentat():
    try:
        kursori = yhteys.cursor()
        sql = """SELECT ident, name, latitude_deg, longitude_deg FROM airport WHERE iso_country = 'FI' AND ident LIKE 'EF%'"""
        kursori.execute(sql)
        return kursori.fetchall()
    except mysql.connector.Error as err:
        print(Panel.fit(f"Tietokantavirhe: {err}", style=STYLE_DANGER))
        exit()


def valitse_tavarat_ja_pelaaja(lentokentat):
    efhk = next(k for k in lentokentat if k[0] == "EFHK")
    efhk_coord = (efhk[2], efhk[3])

    # vain 100 km säteellä olevat kentät
    lahimmat = [
        k for k in lentokentat
        if k[0] != "EFHK"  # Estetään tavaroiden sijoittuminen aloituskentälle
           and laske_etaisyys(efhk_coord, (k[2], k[3])) <= MAX_ETÄISYYS
    ]

    if len(lahimmat) < 4:
        raise ValueError("Liian vähän kenttiä 100 km säteellä EFHK:sta (vähintään 4 vaaditaan)")

    random.shuffle(lahimmat)
    tavarat = []
    for tavara in random.sample(list(tavara_emojit.keys()), 3):
        kentta = lahimmat.pop()
        tavarat.append((kentta, tavara))

    vakooja = lahimmat.pop()
    return tavarat, vakooja


def laske_etaisyys(koord1, koord2):
    return geopy.distance.distance(koord1, koord2).km

STYLE_HEADER = "bold #FF6B6B on #2D3436"
STYLE_SUCCESS = "bold #00FF00 on #2D3436"
STYLE_WARNING = "bold #FFD700 on #2D3436"
STYLE_DANGER = "bold #FF0000 on #2D3436"
STYLE_INFO = "bold #00BFFF on #2D3436"
STYLE_TABLE = "bold #74B9FF"
MAP_SYMBOLS = ["🛫", "🛩️", "🚁", "🌍"]
BORDER_STYLES = {
    "header": "bold #FF6B6B",
    "table": "bold #74B9FF",
    "success": "bold #00FF00",
    "warning": "bold #FFD700"
}

# Pelin asetukset
MAX_ETÄISYYS = 100  # km
ALOITUSBUDJETTI = 5000  # €
CO2_KERROIN = 0.133  # kg/km

# Pelimekaniikka lisäykset
SATUNNAISET_TAPAHTUMAT = [
    ("Säähäiriö", "⛈️", "Lento viivästyy! Menetät yhden vuoron", 0.15),
    ("Löysit rahaa", "💰", "+€500 budjettiin!", 0.10),
    ("Moottorivika", "🔧", "Korjaus maksaa €300", 0.12),
    ("Turbulenssia", "🌪️", "Matka-aika tuplaantuu!", 0.08)
]


class PeliTilanne:
    def __init__(self):
        self.aloitus_aika = datetime.now()
        self.viimeisin_siirto = None
        self.saavutukset = set()
        self.käytetyt_tehot = []


def lataa_animaatio():
    with Progress(transient=True) as progress:
        task = progress.add_task("[cyan]Ladataan...", total=100)
        for _ in range(100):
            progress.update(task, advance=1)
            sleep(0.02)


def piirra_kartta(sijainti, kentat):
    kartta = Table.grid(padding=1, pad_edge=True)
    kartta.add_column(style="dim", justify="center")

    # Lisätään karttasymboleja
    rivi = Text(" " * 50)
    for i, kentta in enumerate(kentat[:4]):
        rivi.append(f"{MAP_SYMBOLS[i]} {kentta[0]}", style="bold yellow")
    kartta.add_row(Panel.fit(rivi, title="Karttanäkymä"))

    return kartta


def satunnainen_tapahtuma():
    if random.random() < 0.3:  # 30% mahdollisuus tapahtumalle
        tapahtuma = random.choice(SATUNNAISET_TAPAHTUMAT)
        return tapahtuma
    return None


def nayta_alkuruutu(tavarat):
    # Päivitetty header tyylillä ja väreillä
    header = Panel.fit(
        Text("✈️ LENTOKENTTÄ-SEIKKAILU 3000 ✈️",
             justify="center",
             style="bold #FFE66D on #2D3436"),
        style=STYLE_HEADER,
        border_style=BORDER_STYLES["header"]
    )
    print(header)

    tavarataulu = Table(
        title="[bold #FF6B6B]📦 Etsittävät tavarat[/]",
        box=box.DOUBLE_EDGE,
        style=STYLE_TABLE,
        header_style="bold #FFE66D",
        border_style=BORDER_STYLES["table"],
        title_style="bold #FF6B6B"
    )
    tavarataulu.add_column("[#FF6B6B]Nro[/]", justify="center", width=8)
    tavarataulu.add_column("[#00BFFF]Tavara[/]", style="#74B9FF", min_width=20)
    tavarataulu.add_column("[#74B9FF]Sijainti[/]", style="#00BFFF", min_width=30)

    for i, (kentta, tavara) in enumerate(tavarat, 1):
        emoji = tavara_emojit.get(tavara, "❓")
        tavarataulu.add_row(
            f"[#FF6B6B]{i}.[/]",
            f"{emoji} [bold #00BFFF]{tavara.capitalize()}[/]",
            f"[#74B9FF]{kentta[1]}[/]\n[dim #A9A9A9]({kentta[0]})[/]"
        )

    # Moderni ohjepaneeli
    ohjeet = Table(
        title="[bold #FF6B6B]📜 Pelin ohjeet[/]",
        box=box.ROUNDED,
        style=STYLE_TABLE,
        border_style=BORDER_STYLES["warning"],
        show_header=False
    )
    ohjeet.add_row("[bold #00BFFF]1.[/] Liiku ICAO-koodeja käyttäen")
    ohjeet.add_row("[bold #00BFFF]2.[/] Löydä kaikki 3 tavaraa")
    ohjeet.add_row("[bold #00BFFF]3.[/] Vältä yli 100 km lentoja")
    ohjeet.add_row("[bold #00BFFF]4.[/] Löydä vakooja voittaaksesi")

    # Resurssipaneeli
    resurssit = Panel(
        "[bold #FFE66D]💰 Budjetti:[/] €5000\n"
        "[bold #00FF00]🌱 CO2-budjetti:[/] 500 kg\n"
        "[bold #FFA500]🚫 Max lentomatka:[/] 100 km",
        title="📊 Resurssit",
        border_style=BORDER_STYLES["success"]
    )

    # Layout uudelleenjärjestely
    layout = Columns(
        [
            Panel(tavarataulu, border_style=BORDER_STYLES["table"]),
            Columns([ohjeet, resurssit], equal=True)
        ],
        expand=True,
        align="center"
    )

    print(Panel(layout, border_style=BORDER_STYLES["success"], title="🚀 Aloita seikkailusi!"))


def nayta_tilanne(peli, sijainti, budjetti, loydetyt, kokonaismatka):
    co2_päästöt = kokonaismatka * CO2_KERROIN
    peliaika = datetime.now() - peli.aloitus_aika
    peliaika_muoto = str(peliaika).split(".")[0]  # Poistetaan mikrosekunnit

    # taulukkorakenne
    tilanne = Table.grid(expand=True, padding=(0, 2))
    tilanne.add_column(justify="left", width=40)
    tilanne.add_column(justify="right", width=30)

    # Vasen paneeli (Sijaintitiedot)
    sijainti_paneeli = Table(
        box=box.ROUNDED,
        show_header=False,
        style="#74B9FF",
        border_style="bright_blue",
        title="📍 Sijaintitiedot"
    )
    sijainti_paneeli.add_row(
        "[bold #FFD700]Lentokenttä:[/]",
        f"[bold]{sijainti[1]}[/]"
    )
    sijainti_paneeli.add_row(
        "[bold #FFD700]ICAO-koodi:[/]",
        f"[bold #00BFFF]{sijainti[0]}[/]"
    )
    sijainti_paneeli.add_row(
        "[bold #FFD700]Koordinaatit:[/]",
        f"{sijainti[2]:.4f}, {sijainti[3]:.4f}"
    )
    sijainti_paneeli.add_row(
        "[bold #FFD700]Peliaika:[/]",
        f"[#00FF00]{peliaika_muoto}[/]"
    )

    # Oikea paneeli (Tilastot)
    tilastot_paneeli = Table(
        box=box.DOUBLE,
        show_header=False,
        style="#00BFFF",
        border_style="bright_green",
        title="📊 Tilastot"
    )
    tilastot_paneeli.add_row(
        "[bold #FF6B6B]Budjetti:[/]",
        f"[#00FF00]€{budjetti:,.2f}[/]"
    )
    tilastot_paneeli.add_row(
        "[bold #FF6B6B]CO2-päästöt:[/]",
        f"[#FFA500]{co2_päästöt:.1f} kg[/]"
    )
    tilastot_paneeli.add_row(
        "[bold #FF6B6B]Tehdyt vuorot:[/]",
        f"[#74B9FF]{len(peli.käytetyt_tehot)}[/]"
    )
    tilastot_paneeli.add_row(
        "[bold #FF6B6B]Löydetyt tavarat:[/]",
        f"[blink #00FF00]{len(loydetyt)}/3[/]"
    )

    # Yhdistetään paneelit
    tilanne.add_row(
        Panel(sijainti_paneeli, border_style="bright_blue"),
        Panel(tilastot_paneeli, border_style="bright_green")
    )

    print(tilanne)


def peli():
    try:
        peli_tilanne = PeliTilanne()
        lentokentat = hae_lentokentat()
        tavarat, vakooja = valitse_tavarat_ja_pelaaja(lentokentat)
        sijainti = next(k for k in lentokentat if k[0] == "EFHK")
        loydetyt = []
        budjetti = ALOITUSBUDJETTI
        kokonaismatka = 0

        nayta_alkuruutu(tavarat)
        lataa_animaatio()

        while True:
            print("\n" * 3)
            nayta_tilanne(peli_tilanne, sijainti, budjetti, loydetyt, kokonaismatka)
            print(piirra_kartta(sijainti, lentokentat))

            # Tarkista voittoehdot
            if sijainti == vakooja:
                print(Panel.fit("[blink bold green]🎉 VOITIT! Löysit vakoojan! 🕵️[/]", style=STYLE_SUCCESS))
                break

            # Tarkista tavarat
            for kentta, tavara in tavarat:
                if sijainti == kentta and kentta not in loydetyt:
                    loydetyt.append(kentta)
                    emoji = tavara_emojit.get(tavara, "❓")
                    print(Panel.fit(f"[bold green]🎉 Löysit {emoji} {tavara.capitalize()}!", style=STYLE_SUCCESS))
                    peli_tilanne.saavutukset.add(tavara)

            if len(loydetyt) == 3 or sijainti == vakooja:
                print(Panel.fit(
                    "[blink #00FF00]"
                    "╔════════════════════════════╗\n"
                    "║ 🏆  ONNITELUT  🏆  ║\n"
                    "╚════════════════════════════╝[/]",
                    style=STYLE_SUCCESS
                ))
                lopputulos = Table(
                    title="[bold #FF6B6B]📊 LOPPUTULOS[/]",
                    box=box.DOUBLE_EDGE,
                    style=STYLE_TABLE
                )
                break

            # Käsittele syöte
            valinta = Prompt.ask(
                "\n[bold yellow]Syötä seuraava ICAO-koodi[/] "
                "[dim](tai 'exit'/'help')[/]",
                default="exit"
            ).strip().upper()

            if valinta == "EXIT":
                print(Panel.fit("[yellow]Peli keskeytetty! 👋[/]", style=STYLE_WARNING))
                break

            # Käsittele tapahtumat
            tapahtuma = satunnainen_tapahtuma()
            if tapahtuma:
                nimi, emoji, viesti, vaikutus = tapahtuma
                print(Panel.fit(f"{emoji} [bold]{nimi}[/] {viesti}", style=STYLE_WARNING))
                if "rahaa" in nimi:
                    budjetti += 500
                elif "maksaa" in nimi:
                    budjetti -= 300

            # Käsittele tapahtumat
            tapahtuma = satunnainen_tapahtuma()
            if tapahtuma:
                nimi, emoji, viesti, vaikutus = tapahtuma
                print(Panel.fit(f"{emoji} [bold]{nimi}[/] {viesti}", style=STYLE_WARNING))
                if "rahaa" in nimi:
                    budjetti += 500
                elif "maksaa" in nimi:
                    budjetti -= 300

            try:
                seuraava = next(k for k in lentokentat if k[0] == valinta)

                # Laske etäisyys ja hinta
                etaisyys = laske_etaisyys(
                    (sijainti[2], sijainti[3]),
                    (seuraava[2], seuraava[3])
                )

                if etaisyys > MAX_ETÄISYYS:
                    print(Panel.fit(
                        f"[bold red]Etäisyys {etaisyys:.1f} km yli sallitun 100 km![/]",
                        style=STYLE_DANGER
                    ))
                    continue

                hinta = etaisyys * 10
                if budjetti < hinta:
                    print(Panel.fit(
                        f"[bold red]Budjetti riittämätön! Tarvitaan €{hinta:.2f}[/]",
                        style=STYLE_DANGER
                    ))
                    continue

#Taulukko Päivittään kun pelin tilanne etenee
                budjetti -= hinta
                kokonaismatka += etaisyys
                sijainti = seuraava
                peli_tilanne.käytetyt_tehot.append(valinta)

            except StopIteration:
                print(Panel.fit(
                    f"[bold red]Virheellinen ICAO-koodi: {valinta}[/]",
                    style=STYLE_DANGER
                ))

    except Exception as e:
        print(Panel.fit(f"[bold red]VIRHE: {str(e)}[/]", style=STYLE_DANGER))
    finally:
        yhteys.close()


if __name__ == "__main__":
    try:
        peli()
    except KeyboardInterrupt:
        print(Panel.fit("[yellow]Peli keskeytetty! 👋[/]", style=STYLE_WARNING))

