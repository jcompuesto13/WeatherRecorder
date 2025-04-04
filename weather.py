# (c) 2025 Jovan Compuesto, Eurica Abella
# A program to parse and manage a JSON file.

import os
import re
import json
from datetime import datetime


pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")

def write_to_file(filepath, data={}):
    """ Save a dictionary (empty or not) into a file. """
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def read_file(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)

def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def validate_date(date):
    if not pattern.match(date):
        return False

    year, month, day = map(int, date.split("-"))
    if not (1 <= month <= 12) or not (1 <= day <= 31):
        return False

    if month in [4, 6, 9, 11] and day > 30:
        return False
    if month == 2:
        if is_leap_year(year) and day > 29:
            return False
        elif day > 28:
            return False

    return True

def format_date(date):
    value = datetime.strptime(date, "%Y-%m-%d")
    return value.strftime("%b %d, %Y (%a)")

def main():
    datapath = "data"
    os.makedirs(datapath, exist_ok=True)

    filepath = f"{datapath}/weather.json"
    if not os.path.exists(filepath):
        write_to_file(filepath)

    records = read_file(filepath)
    count = len(records)

    print("[Weather Station]")
    print(f" \nNOTE: Type 'stop' to end the program.")

    # get the current date
    today = datetime.today().strftime("%Y-%m-%d")
    placeholder = today

    while True:
        if placeholder in records:
            placeholder = "yyyy-mm-dd"

        date = input(f"\nEnter date ({placeholder}): ").strip()
        if date == "stop":
            break

        if date == "" and placeholder != "yyyy-mm-dd":
            date = placeholder
        elif not validate_date(date):
            print("Oops, please use 'yyyy-mm-dd' format...")
            continue
        elif date > today:
            print("Oops, date is in the future...")
            continue

        temperature = float(input(" Enter temperature (°C): "))
        humidity = float(input(" Enter Rel. Humidity (%): "))
        if not (0 <= humidity <= 100):
            print("Oops, RH (%) must be between 0-100 only...")
            continue
        # add 3 more weather phenomenon here, such as UV index, etc.

        records[date] = {
            "temperature": temperature,
            "humidity": humidity,
            # add the key-value pairs here...
        }

    print("\nSaving to file...")
    records = dict(sorted(records.items()))
    write_to_file(filepath, records)

    print("\n[Weather Information]")
    for date, data in records.items():
        formatted_date = format_date(date)
        temperature = data["temperature"]
        humidity = data["humidity"]
        # phenomenon3 = data["phenomenon3"]
        # phenomenon4 = data["phenomenon4"]
        # phenomenon5 = data["phenomenon5"]

        print(f"{formatted_date}\t| {temperature:.1f}°C\t| {humidity:.1f}%")
        # print(f" * {phenomenon3:,.1f} symbol | ...")

if __name__ == "__main__":
    main()