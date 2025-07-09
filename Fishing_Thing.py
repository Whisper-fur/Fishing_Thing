import csv
from datetime import datetime



def stats():
   print('Total number of trips logged: ') 
   print('Total number of fish caught: ')
   print('Most common fish species: ')
   print('Most used bait: ')
   print('Average fish per trip: ')

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
        choice = input("Choose an option (1-3): ")

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
            break
        else:
            print("Invalid option. Please choose 1, 2, or 3.")
menu()
def view_logs():
    print("I'll be adding this in soon. Keep catching fish until then, the data helps")

menu()