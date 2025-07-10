import csv
from datetime import datetime
from collections import Counter, defaultdict


#Logging Section 
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

def edit_logs():
    filename = "fishing_log.csv"
    with open(filename, mode="r") as file:
        reader = csv.reader(file)
        header = next(reader)
        rows = list(reader)

    if not rows:
        print("No logs to edit.")
        return

    print("\nSelect a log to edit:")
    for i, row in enumerate(rows, start=1):
        print(f"{i}. {' | '.join(row)}")  

    try:
        index = int(input("Enter the number of the log to edit: ")) - 1
        if index < 0 or index >= len(rows):
            print("Invalid selection.")
            return
    except ValueError:
        print("Invalid input.")
        return
        
    selected_row = rows[index]
    print("\nEditing this entry:")
    for i, value in enumerate(selected_row):
        new_value = input(f"{header[i]} (leave blank to keep '{value}'): ").strip()
        if new_value:
            selected_row[i] = new_value

    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(rows)

    print("Log updated successfully.")    


def delete_log():
    filename = "fishing_log.csv"
    with open(filename, mode="r") as file:
        reader = csv.reader(file)
        header = next(reader)
        rows = list(reader)

    if not rows:
        print("No logs to delete.")
        return

    print("\n Select a log to delete:")
    for i, row in enumerate(rows, start=1):
        print(f"{i}. {' | '.join(row)}")

    try:
        index = int(input("Enter the number of the log to delete: ")) - 1
        if index < 0 or index >= len(rows):
            print("Invalid selection.")
            return
    except ValueError:
        print("Invalid input.")
        return

    print("\nYou selected:")
    print(" | ".join(rows[index]))
    confirm = input("Are you sure you want to delete this? (y/n): ").strip().lower()
    if confirm != "y":
        print("Deletion canceled.")
        return

    del rows[index]

    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(rows)

    print("Log deleted successfully.")
 
## Stats Section
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



def menu():
    while True:
        print("\n=== Fishing Tracker Menu ===")
        print("1. Log new trip")
        print("2. View past logs") 
        print("3. Edit a log")
        print("4. Delete a log")
        print("5. Basic Stat overview")
        print("6. Catch Rate by Lake")
        print("7. Visual Analysis (Coming Soon)")
        choice = input("Choose an option (1-6 or type 'exit' to leave.): ")

        if choice == "1":
            log_trip()
        elif choice == "2":
            view_logs()
        elif choice == "3":
            edit_logs()
        elif choice == "4":
            delete_log()
        elif choice == "5":
            stats()
        elif choice == "6":
            catch_rate()
        elif choice == "exit":
            print("Tight lines! Goodbye.")
            break
        else:
            print("Invalid option.")

menu()