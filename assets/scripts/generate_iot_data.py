#!/usr/bin/env python3
"""
IoT Sensor Data Generator für Column Store Demos

Generiert synthetische Smart-Home-Sensordaten mit konfigurierbarem Zeitraum.
Die Daten eignen sich perfekt für Column Store vs. Row Store Vergleiche.

Usage:
    python generate_iot_data.py --start "2023-01-01" --end "2023-12-31" --interval 1h
    python generate_iot_data.py --days 30 --interval 10min
    python generate_iot_data.py --help
"""

import argparse
import csv
import math
from datetime import datetime, timedelta
import random


def generate_temperature(hour, day_of_year, room_type="living"):
    """
    Generiert realistische Temperatur mit täglichem und saisonalem Zyklus.
    
    Args:
        hour: Stunde des Tages (0-23)
        day_of_year: Tag im Jahr (1-365)
        room_type: Art des Raums (living, bedroom, kitchen, bathroom, outside)
    
    Returns:
        Temperatur in Celsius
    """
    # Saisonaler Zyklus (Jahreszeit)
    seasonal = 15 + 8 * math.sin(2 * math.pi * (day_of_year - 80) / 365)
    
    # Täglicher Zyklus (Tag/Nacht)
    daily = 3 * math.sin(2 * math.pi * (hour - 6) / 24)
    
    # Raum-spezifische Anpassungen
    room_offsets = {
        "living": 0,
        "bedroom": -1.5,
        "kitchen": 1.0,
        "bathroom": 2.0,
        "outside": 0
    }
    
    base_temp = seasonal + daily + room_offsets.get(room_type, 0)
    noise = random.gauss(0, 0.5)  # Leichtes Rauschen
    
    # Außentemperatur schwankt stärker
    if room_type == "outside":
        base_temp += random.gauss(0, 2)
    
    return round(base_temp, 2)


def generate_humidity(temperature, room_type="living"):
    """
    Generiert realistische Luftfeuchtigkeit basierend auf Temperatur.
    
    Args:
        temperature: Temperatur in Celsius
        room_type: Art des Raums
    
    Returns:
        Relative Luftfeuchtigkeit in %
    """
    # Basis-Luftfeuchtigkeit (inverse Korrelation mit Temperatur)
    base_humidity = 70 - (temperature - 15) * 1.5
    
    # Raum-spezifische Anpassungen
    room_offsets = {
        "living": 0,
        "bedroom": -5,
        "kitchen": 10,
        "bathroom": 20,
        "outside": 5
    }
    
    humidity = base_humidity + room_offsets.get(room_type, 0)
    humidity += random.gauss(0, 3)  # Rauschen
    
    # Begrenzen auf 20-95%
    humidity = max(20, min(95, humidity))
    
    return round(humidity, 1)


def generate_light(hour, room_type="living"):
    """
    Generiert Licht-Level basierend auf Tageszeit.
    
    Args:
        hour: Stunde des Tages (0-23)
        room_type: Art des Raums
    
    Returns:
        Lux-Wert (0-1000)
    """
    # Tageslicht (6-20 Uhr)
    if 6 <= hour <= 20:
        daylight = 300 + 400 * math.sin(math.pi * (hour - 6) / 14)
    else:
        daylight = 0
    
    # Künstliches Licht (18-23 Uhr und 6-8 Uhr)
    if 18 <= hour <= 23 or 6 <= hour <= 8:
        artificial = random.choice([0, 150, 300, 450])  # An/Aus/Dimmer
    else:
        artificial = 0
    
    # Raum-spezifisch
    if room_type == "outside":
        return round(daylight * 1.5, 0)  # Heller draußen
    
    return round(daylight + artificial + random.gauss(0, 20), 0)


def generate_co2(hour, occupancy=1):
    """
    Generiert CO2-Level basierend auf Tageszeit und Belegung.
    
    Args:
        hour: Stunde des Tages (0-23)
        occupancy: Anzahl Personen im Raum (0-4)
    
    Returns:
        CO2 in ppm (parts per million)
    """
    base_co2 = 400  # Außenluft
    
    # Erhöhung durch Personen
    co2_per_person = 150
    co2 = base_co2 + occupancy * co2_per_person
    
    # Nachts weniger Lüftung → höherer CO2
    if 22 <= hour or hour <= 6:
        co2 += random.randint(50, 150)
    
    co2 += random.gauss(0, 30)
    
    return max(400, round(co2, 0))


def generate_motion(hour):
    """
    Generiert Bewegungssensor-Status (binär).
    
    Args:
        hour: Stunde des Tages (0-23)
    
    Returns:
        0 (keine Bewegung) oder 1 (Bewegung)
    """
    # Höhere Wahrscheinlichkeit tagsüber (7-23 Uhr)
    if 7 <= hour <= 23:
        return 1 if random.random() < 0.4 else 0
    else:
        return 1 if random.random() < 0.05 else 0


def generate_power(hour, appliances_on=1):
    """
    Generiert Stromverbrauch in Watt.
    
    Args:
        hour: Stunde des Tages (0-23)
        appliances_on: Anzahl aktiver Geräte
    
    Returns:
        Leistung in Watt
    """
    # Basis-Verbrauch (Standby)
    base_power = 50
    
    # Geräte-Verbrauch
    power = base_power + appliances_on * random.randint(50, 300)
    
    # Kochen (11-13, 18-20 Uhr)
    if 11 <= hour <= 13 or 18 <= hour <= 20:
        power += random.randint(0, 1500)  # Herd/Ofen
    
    return round(power, 0)


def parse_interval(interval_str):
    """
    Parst Interval-String zu timedelta.
    
    Args:
        interval_str: String wie "1h", "10min", "30s"
    
    Returns:
        timedelta Objekt
    """
    interval_str = interval_str.lower().strip()
    
    if interval_str.endswith("h"):
        hours = int(interval_str[:-1])
        return timedelta(hours=hours)
    elif interval_str.endswith("min"):
        minutes = int(interval_str[:-3])
        return timedelta(minutes=minutes)
    elif interval_str.endswith("s"):
        seconds = int(interval_str[:-1])
        return timedelta(seconds=seconds)
    elif interval_str.endswith("d"):
        days = int(interval_str[:-1])
        return timedelta(days=days)
    else:
        raise ValueError(f"Ungültiges Interval-Format: {interval_str}. Verwende '1h', '10min', '30s', oder '1d'")


def generate_data(start_date, end_date, interval):
    """
    Generiert IoT-Sensor-Daten für den angegebenen Zeitraum.
    
    Args:
        start_date: Start-Datum (datetime)
        end_date: End-Datum (datetime)
        interval: Messintervall (timedelta)
    
    Returns:
        Liste von Datenzeilen (Dicts)
    """
    data = []
    current_time = start_date
    
    rooms = ["living", "bedroom", "kitchen", "bathroom"]
    
    print(f"Generiere Daten von {start_date} bis {end_date} mit Interval {interval}...")
    
    row_count = 0
    while current_time <= end_date:
        hour = current_time.hour
        day_of_year = current_time.timetuple().tm_yday
        
        # Zufällige Belegung (mehr Personen tagsüber)
        occupancy = random.randint(0, 2) if 7 <= hour <= 23 else 0
        
        row = {
            "timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S"),
            "room_id": random.choice(rooms),
        }
        
        # Temperatur-Sensoren (4 Räume + 1 Außen)
        for room in rooms:
            row[f"temp_{room}"] = generate_temperature(hour, day_of_year, room)
        row["temp_outside"] = generate_temperature(hour, day_of_year, "outside")
        
        # Luftfeuchtigkeits-Sensoren (4 Räume + 1 Außen)
        for room in rooms:
            row[f"humidity_{room}"] = generate_humidity(row[f"temp_{room}"], room)
        row["humidity_outside"] = generate_humidity(row["temp_outside"], "outside")
        
        # Licht-Sensoren (4 Räume + 1 Außen)
        for room in rooms:
            row[f"light_{room}"] = generate_light(hour, room)
        row["light_outside"] = generate_light(hour, "outside")
        
        # CO2-Sensoren (4 Räume)
        for room in rooms:
            row[f"co2_{room}"] = generate_co2(hour, occupancy)
        
        # Bewegungssensoren (4 Räume)
        for room in rooms:
            row[f"motion_{room}"] = generate_motion(hour)
        
        # Stromverbrauch (4 Räume)
        for room in rooms:
            row[f"power_{room}"] = generate_power(hour, random.randint(0, 2))
        
        data.append(row)
        row_count += 1
        
        if row_count % 1000 == 0:
            print(f"  {row_count} Zeilen generiert...")
        
        current_time += interval
    
    print(f"✓ {row_count} Zeilen generiert")
    return data


def main():
    parser = argparse.ArgumentParser(
        description="IoT Sensor Data Generator für Column Store Demos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Beispiele:
  # 1 Jahr Daten, stündlich
  python generate_iot_data.py --start "2023-01-01" --end "2023-12-31" --interval 1h
  
  # 30 Tage Daten, 10-Minuten-Intervall
  python generate_iot_data.py --days 30 --interval 10min
  
  # 7 Tage Daten, minütlich
  python generate_iot_data.py --days 7 --interval 1min
  
  # Custom Output-Datei
  python generate_iot_data.py --days 90 --interval 1h --output sensors_90d.csv
        """
    )
    
    # Zeitraum-Optionen
    date_group = parser.add_mutually_exclusive_group(required=True)
    date_group.add_argument("--start", help="Start-Datum (YYYY-MM-DD)")
    date_group.add_argument("--days", type=int, help="Anzahl Tage ab heute")
    
    parser.add_argument("--end", help="End-Datum (YYYY-MM-DD, nur mit --start)")
    parser.add_argument("--interval", default="1h", help="Messintervall (z.B. 1h, 10min, 30s). Standard: 1h")
    parser.add_argument("--output", default="iot_sensors.csv", help="Output-Dateiname. Standard: iot_sensors.csv")
    
    args = parser.parse_args()
    
    # Zeitraum berechnen
    if args.start:
        start_date = datetime.strptime(args.start, "%Y-%m-%d")
        if args.end:
            end_date = datetime.strptime(args.end, "%Y-%m-%d")
        else:
            end_date = datetime.now()
    else:  # --days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=args.days)
    
    # Interval parsen
    try:
        interval = parse_interval(args.interval)
    except ValueError as e:
        print(f"Fehler: {e}")
        return 1
    
    # Daten generieren
    data = generate_data(start_date, end_date, interval)
    
    # CSV schreiben
    if data:
        fieldnames = data[0].keys()
        
        with open(args.output, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        
        print(f"✓ Daten gespeichert in: {args.output}")
        print(f"  Zeilen: {len(data)}")
        print(f"  Spalten: {len(fieldnames)}")
        print(f"  Zeitraum: {start_date.strftime('%Y-%m-%d')} bis {end_date.strftime('%Y-%m-%d')}")
        print(f"  Interval: {interval}")
    
    return 0


if __name__ == "__main__":
    exit(main())
