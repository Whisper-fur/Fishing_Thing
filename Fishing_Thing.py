import csv
from datetime import datetime
from collections import Counter, defaultdict



def stats():
   with open("fishing_log.csv", mode="r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        rows = list(reader)

        trips = len(rows)

        fish = 0
        for row in rows: #[5]
            fish = fish + int(row[5])

        fish_species_caught = [
            row[4] for row in rows 
            if len(row) > 4 and row[4].strip().lower() not in ["", "none"]]
        fish_species_counts = Counter(fish_species_caught)
        most_caught_fish_species = fish_species_counts.most_common(1)[0]    

        bait_used = [row[6] for row in rows if len(row) > 6 and row[6].strip() != ""]
        bait_counts = Counter(bait_used)
        most_used_bait = bait_counts.most_common(1)[0]

   print('Total number of trips logged: ' + str(trips)) 
   print('Total number of fish caught: ' + str(fish))
   print('Most common fish species: ' + str(most_caught_fish_species))
   print('Most used bait: ' + str(most_used_bait))
   print('Average fish per trip: ' + str(fish/trips))

   print('These stats will be coming soon! with visuals')
   print('Best location: ')
   print('Best time of day: ')
   print('Best Water Temp: ')

def catch_rate():
    with open("fishing_log.csv", mode="r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        rows = list(reader)

    trips_by_location = defaultdict(int)
    fish_by_location = defaultdict(int)

    for row in rows:
        if len(row) > 5:
            location = row[2].strip()
            trips_by_location[location] += 1

            if row[4].strip().lower() != "none":
                try:
                    fish_by_location[location] += int(row[5])
                except ValueError:
                    pass

    print("\n🎣 Catch Rate by Lake:")
    for location in sorted(trips_by_location.keys()):
        trips = trips_by_location[location]
        fish = fish_by_location.get(location, 0)
        avg = round(fish / trips, 2) if trips else 0
        print(f"{location}: {fish} fish / {trips} trips → {avg} per trip")

def log_trip():
    date = input("Date (YYYY-MM-DD): ") or datetime.today().strftime('%Y-%m-%d')
    time = input('Time?')
    location = input('Where did you fish?')
    weather = input('What was the weather like?')
    fish_caught = input('What fish did you catch?')
    amount = input('How many fish did you catch?')
    bait = input('What bait did you use?')
    temp = input('What was the temperature?')
    wind = input('What was the wind speed?')

    with open("fishing_log.csv", mode="a", newline="") as file:
      writer = csv.writer(file)
      writer.writerow([date, time, location, weather, fish_caught, amount, bait, temp, wind])

def load_log_data():
    with open("fishing_log.csv", mode="r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        return list(reader)
    

def view_logs():
    print("\nFishing Trip Log:\n")

    try:
        with open("fishing_log.csv", mode="r") as file:
            reader = csv.reader(file)
            header = next(reader)  # Read the header row
            print(" | ".join(header))  # Print header titles
            print("-" * 80)

            for row in reader:
                print(" | ".join(row))

    except FileNotFoundError:
        print("No log file found yet. Go catch some fish first!")      

def delete_log():
    with open("fishing_log.csv", mode="r") as file:
            reader = csv.reader(file)
            header = next(reader) 
            
    #Add in the feature to remove the row here.

    with open("fishing_log.csv", mode="r") as file:
        reader = csv.reader(file)
        rows = list(reader)
    print('You made it here so it seems like the reader is working')



def menu():
    while True:
        print("\n=== Fishing Tracker Menu ===")
        print("1. Log new trip")
        print("2. View past logs")
        print("3. Exit")
        print("4. Delete a log")
        print("5. Stat overview")
        print("6. Catch Rate by Lake")
        choice = input("Choose an option (1-6): ")

        if choice == "1":
            log_trip()
        elif choice == "2":
            view_logs()
        elif choice == "3":
            print("Tight lines! Goodbye.")
        elif choice == "4":
            delete_log()
        elif choice == "5":
            stats()
        elif choice == "6":
            catch_rate()
            break
        else:
            print("Invalid option.")
menu()
def view_logs():
    print("I'll be adding this in soon. Keep catching fish until then, the data helps")

menu()