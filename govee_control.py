import requests
import os
import json

os.system("color 70")

# Konfigurationsdatei laden oder erstellen
config_datei = "config.json"

if not os.path.exists(config_datei):
    config = {
        "api_key": input("Bitte gib deinen API-Key ein: "),
        "device_id": input("Bitte gib deine Device ID ein: "),
        "modell": input("Bitte gib das Modell ein: ")
    }
    with open(config_datei, "w") as f:
        json.dump(config, f, indent=4)
    print("✅ Konfigurationsdatei erstellt.")
else:
    with open(config_datei, "r") as f:
        config = json.load(f)
    print("✅ Konfiguration geladen.")

API_KEY = config["api_key"]
DEVICE_ID = config["device_id"]
MODEL = config["modell"]

BASE_URL = "https://developer-api.govee.com/v1"
HEADERS = {
    "Govee-API-Key": API_KEY,
    "Content-Type": "application/json"
}

COLOR_MAP = {
    "rot": (255, 0, 0),
    "grün": (0, 255, 0),
    "blau": (0, 0, 255),
    "gelb": (255, 255, 0),
    "cyan": (0, 255, 255),
    "magenta": (255, 0, 255),
    "weiß": (255, 255, 255),
    "orange": (255, 165, 0),
    "lila": (128, 0, 128),
    "pink": (255, 105, 180),
    "warmweiß": (127, 60, 60)
}

def send_command(name, value):
    url = f"{BASE_URL}/devices/control"
    payload = {
        "device": DEVICE_ID,
        "model": MODEL,
        "cmd": {
            "name": name,
            "value": value
        }
    }
    response = requests.put(url, headers=HEADERS, json=payload)
    return response.status_code == 200

def turn_on():
    return send_command("turn", "on")

def turn_off():
    return send_command("turn", "off")

def set_color(r, g, b):
    return send_command("color", {"r": r, "g": g, "b": b})

def set_brightness(level):
    return send_command("brightness", level)

if __name__ == "__main__":
    device_state = None  # Startzustand unbekannt

    print("🟢 Govee Steuerung gestartet")
    print("Drücke Enter zum Ein-/Ausschalten")
    print("Schreibe eine Farbe wie 'rot', 'weiß', 'lila'")
    print("Gib eine Zahl von 1–100 ein für die Helligkeit")
    print("Schreibe 'stop' zum Beenden\n")

    while True:
        user_input = input("> ").strip().lower()

        if user_input == "stop":
            print("🛑 Beende das Skript.")
            break

        elif user_input == "":
            if device_state != "on":
                if turn_on():
                    device_state = "on"
                    print("💡 Lampe ist jetzt AN")
            else:
                if turn_off():
                    device_state = "off"
                    print("💤 Lampe ist jetzt AUS")

        elif user_input in COLOR_MAP:
            r, g, b = COLOR_MAP[user_input]
            if set_color(r, g, b):
                print(f"🎨 Farbe geändert zu: {user_input}")
            else:
                print("❌ Farbe konnte nicht geändert werden.")

        elif user_input.isdigit():
            brightness = int(user_input)
            if 1 <= brightness <= 100:
                if set_brightness(brightness):
                    print(f"🔆 Helligkeit auf {brightness}% gesetzt")
                else:
                    print("❌ Helligkeit konnte nicht geändert werden.")
            else:
                print("⚠️ Bitte gib eine Zahl von 1 bis 100 ein.")

        else:
            print("❓ Unbekannter Befehl. Drücke Enter, schreibe Farbe, Zahl oder 'stop'.")
