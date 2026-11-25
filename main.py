# Lisää tarvittavat kirjastot ja hae tiedostot
import network
from machine import Pin
from dht import DHT22
from umqtt.simple import MQTTClient
import time

# Määritä funktio Wifille
def liityWifiin():
    import network
    import time

    SSID = "LHS25"
    PASSWORD = "14021994"

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    #Lisää teksti toiminnan varmistamiseksi
    print("Yhdistetään verkkoon...")
    while not wlan.isconnected():
        time.sleep(1)

    ip = wlan.ifconfig()[0]
    print("IP-osoite:", ip)

# Liity Wifiin ja ilmoita yhteyden olevan ok
liityWifiin()
print("Wifi yhdistyi.")

# Yhdistä MQTT brokeriin
client = MQTTClient(
    b"picow",
    "iot.research.hamk.fi",
    keepalive=60
)

client.connect()

# Anturin määritys
anturi = DHT22(Pin(21))
# Alkuarvojen määritys    
vanha_lampo = None
vanha_kosteus = None

# Luo silmukka lämmön ja kosteuden mittaamiseksi
while True:
    # Mittaa ja tulosta mittaustekstit toiminnan varmistamiseksi
    print("Mitataan... ")
    anturi.measure()
    print("Mittaus onnistui.")

    # Määrittele tarvittavat muuttujat
    lampotila = anturi.temperature()
    kosteus = anturi.humidity()

    # Luo muuttuja viestin lähetykselle
    lahetysOk = False

    # Mittaa ja lähetä lämpötila, jos muutos
    if lampotila != vanha_lampo:
        client.publish(
                b"HAMK/Fo/DHT22/amk1021056/lampotila",
                str(lampotila)
        )

        vanha_lampo = lampotila
        lahetysOk = True

    # Mittaa ja lähetä kosteus, jos muutos
    if kosteus != vanha_kosteus:
        client.publish(
                b"HAMK/Fo/DHT22/amk1021056/kosteus",
                str(kosteus)
        )

        vanha_kosteus = kosteus
        lahetysOk = True

    # Tulosta lämpötila, kosteus ja tieto tulostuksesta
    print("Lampotila: ", lampotila)
    print("Kosteus: ", kosteus)
    if lahetysOk:
        print("MQTT viesti lähetetty: Kyllä.")
    else:
        print("MQTT viesti lahetetty: Ei.")
    print("")


    # Mittaa 10s välein
    time.sleep(10)

# Katkaise yhteys
client.disconnect()
