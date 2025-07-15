import csv
import matplotlib.pyplot as plt
from datetime import datetime
from collections import Counter, defaultdict
import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


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

def edit_logs(user_input):
    filename = "fishing_log.csv"
    with open(filename, mode="r") as file:
        reader = csv.reader(file)
        header = next(reader)
        rows = list(reader)

    if not rows:
        return "No logs to edit."

    try:
        index = int(user_input) - 1
        if index < 0 or index >= len(rows):
            return "Invalid selection."
    except ValueError:
        return "Invalid input."

    selected_row = rows[index]
    result = "Editing this entry:\n"
    for i, value in enumerate(selected_row):
        result += f"{header[i]}: {value}\n"

    return result


def delete_log(user_input):
    filename = "fishing_log.csv"
    with open(filename, mode="r") as file:
        reader = csv.reader(file)
        header = next(reader)
        rows = list(reader)

    if not rows:
        return "No logs to delete."

    try:
        index = int(user_input) - 1
        if index < 0 or index >= len(rows):
            return "Invalid selection."
    except ValueError:
        return "Invalid input."

    selected_row = rows[index]
    result = "You selected:\n" + " | ".join(selected_row) + "\n"
    rows.pop(index)

    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(rows)

    return "Log deleted successfully."


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

## Visual Stats with matplotlib

def plot_fish_by_lake():
    with open("fishing_log.csv", mode="r") as file:
        reader = csv.reader(file)
        header = next(reader)
        rows = list(reader)

    fish_by_location = defaultdict(int)

    for row in rows:
        if len(row) > 5 and row[4].strip().lower() != "none":
            try:
                location = row[2].strip()
                fish = int(row[5])
                fish_by_location[location] += fish
            except ValueError:
                pass

    locations = list(fish_by_location.keys())
    fish_counts = list(fish_by_location.values())

    fig, ax = plt.subplots()
    ax.bar(locations, fish_counts, color='skyblue')
    ax.set_xlabel('Location')
    ax.set_ylabel('Number of Fish Caught')
    ax.set_title('Fish Caught by Location')
    ax.set_xticklabels(locations, rotation=45)

    return fig

def plot_bait_usage():
    with open("fishing_log.csv", mode="r") as file:
        reader = csv.reader(file)
        header = next(reader)
        rows = list(reader)

    bait_counts = Counter(row[6].strip().lower() for row in rows if len(row) > 6 and row[6].strip() != "")

    baits = list(bait_counts.keys())
    counts = list(bait_counts.values())

    fig, ax = plt.subplots()
    ax.pie(counts, labels=baits, autopct="%1.1f%%", startangle=140)
    ax.set_title("Bait Usage Distribution")

    return fig

def plot_fish_over_time():
    with open("fishing_log.csv", mode="r") as file:
        reader = csv.reader(file)
        header = next(reader)
        rows = list(reader)

    dates = [datetime.strptime(row[0], "%Y-%m-%d") for row in rows if len(row) > 0 and row[0].strip() != ""]
    fish_counts = [int(row[5]) for row in rows if len(row) > 5 and row[5].strip().isdigit()]

    fig, ax = plt.subplots()
    ax.plot(dates, fish_counts, marker="o", linestyle="-", color="green")
    ax.set_xlabel("Date")
    ax.set_ylabel("Number of Fish Caught")
    ax.set_title("Fish Caught Over Time")
    ax.tick_params(axis='x', rotation=45)

    return fig

def best_fishing_conditions():
    with open("fishing_log.csv", mode="r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        rows = list(reader)

    weather_counts = Counter(row[3].strip().lower() for row in rows if len(row) > 3 and row[3].strip() != "")
    temp_values = [float(row[7]) for row in rows if len(row) > 7 and row[7].strip().replace('.', '', 1).isdigit()]
    wind_values = [float(row[8]) for row in rows if len(row) > 8 and row[8].strip().replace('.', '', 1).isdigit()]

    most_common_weather = weather_counts.most_common(1)[0][0] if weather_counts else "Unknown"
    avg_temp = round(sum(temp_values) / len(temp_values), 2) if temp_values else "Unknown"
    avg_wind = round(sum(wind_values) / len(wind_values), 2) if wind_values else "Unknown"

    print("\nBest Fishing Conditions:")
    print(f"Most common weather: {most_common_weather}")
    print(f"Average temperature: {avg_temp}°C")
    print(f"Average wind speed: {avg_wind} km/h")

def trip_recommendations():
    with open("fishing_log.csv", mode="r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        rows = list(reader)

    location_counts = Counter(row[2].strip().lower() for row in rows if len(row) > 2 and row[2].strip() != "")
    bait_counts = Counter(row[6].strip().lower() for row in rows if len(row) > 6 and row[6].strip() != "")

    # Recommend locations with the most trips
    print("\nTop Locations to Fish Again:")
    for location, count in location_counts.most_common(3):
        print(f"{location.title()} - {count} trips")

    # Recommend bait that was most effective
    print("\nBait Recommendations Based on Past Success:")
    for bait, count in bait_counts.most_common(3):
        print(f"{bait.title()} - Used in {count} trips")

## GUI Section 
class FishingLogApp:
    def __init__(self, root):
        self.root = root
        root.title("Fishing Logbook")

        # Set default window size
        root.geometry("800x600")

        # Create a frame for buttons
        button_frame = tk.Frame(root)
        button_frame.pack(side=tk.TOP, fill=tk.X)

        # Add buttons for menu options in a grid format
        buttons = [
            ("New Trip", self.new_trip),
            ("View Logs", self.view_logs),
            ("Edit Logs", self.edit_logs),
            ("Delete Log", self.delete_log),
            ("Show Stats", self.show_stats),
            ("Visualize Fish by Lake", self.plot_fish_by_lake),
        
        ]

        for i, (text, command) in enumerate(buttons):
            tk.Button(button_frame, text=text, command=command).grid(row=i // 2, column=i % 2, padx=5, pady=5, sticky="ew")

        # Add a frame for displaying results
        self.result_frame = tk.Frame(root)
        self.result_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # Add an input frame for user input
        self.input_frame = tk.Frame(root)
        self.input_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.input_label = tk.Label(self.input_frame, text="Input:")
        self.input_label.pack(side=tk.LEFT, padx=5)

        self.input_entry = tk.Entry(self.input_frame)
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.input_button = tk.Button(self.input_frame, text="Submit", command=self.handle_input)
        self.input_button.pack(side=tk.LEFT, padx=5)

        # Load and display log data
        self.load_logs()

    def handle_input(self):
        user_input = self.input_entry.get()
        self.input_entry.delete(0, tk.END)

        try:
            index = int(user_input) - 1
            filename = "fishing_log.csv"

            with open(filename, mode="r") as file:
                reader = csv.reader(file)
                header = next(reader)
                rows = list(reader)

            if index < 0 or index >= len(rows):
                messagebox.showerror("Error", "Invalid selection.")
                return

            rows.pop(index)

            with open(filename, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(header)
                writer.writerows(rows)

            messagebox.showinfo("Success", "Log deleted successfully!")

            # Refresh the log view
            self.view_logs()

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")
        except FileNotFoundError:
            messagebox.showerror("Error", "No log file found.")

    def display_result(self, text):
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        text_widget = tk.Text(self.result_frame, wrap=tk.WORD)
        text_widget.insert(tk.END, text)
        text_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def display_plot(self, fig):
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.result_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Close the figure to prevent memory leaks
        plt.close(fig)

    def new_trip(self):
        user_input = self.input_entry.get()
        self.input_entry.delete(0, tk.END)
        log_trip()  # Modify log_trip to accept user_input if needed
        self.display_result("Trip logged successfully!")
        self.load_logs()

    def view_logs(self):
        # Hide the input frame as it's not needed for viewing logs
        self.input_frame.pack_forget()

        # Clear the result frame
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        try:
            with open("fishing_log.csv", mode="r") as file:
                reader = csv.reader(file)
                header = next(reader)
                rows = list(reader)

                # Create a Text widget for better alignment
                text_widget = tk.Text(self.result_frame, wrap=tk.NONE, font=("Courier", 10))
                text_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

                # Format and insert header
                header_line = "Index | " + " | ".join(f"{h:<15}" for h in header)
                text_widget.insert(tk.END, header_line + "\n")
                text_widget.insert(tk.END, "-" * len(header_line) + "\n")

                # Format and insert rows with index numbers
                for i, row in enumerate(rows):
                    row_line = f"{i + 1:<5} | " + " | ".join(f"{value:<15}" for value in row)
                    text_widget.insert(tk.END, row_line + "\n")

                # Disable editing
                text_widget.config(state=tk.DISABLED)

        except FileNotFoundError:
            label = tk.Label(self.result_frame, text="No logs found. Please add a new trip.", anchor="w")
            label.pack(fill=tk.X)

    def edit_logs(self):
        # Show the input frame for entering the log number to edit
        self.input_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Clear the result frame
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        try:
            with open("fishing_log.csv", mode="r") as file:
                reader = csv.reader(file)
                header = next(reader)
                rows = list(reader)

                # Create a Text widget for displaying logs
                text_widget = tk.Text(self.result_frame, wrap=tk.NONE, font=("Courier", 10))
                text_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

                # Format and insert header
                header_line = "Index | " + " | ".join(f"{h:<15}" for h in header)
                text_widget.insert(tk.END, header_line + "\n")
                text_widget.insert(tk.END, "-" * len(header_line) + "\n")

                # Format and insert rows with index numbers
                for i, row in enumerate(rows):
                    row_line = f"{i + 1:<5} | " + " | ".join(f"{value:<15}" for value in row)
                    text_widget.insert(tk.END, row_line + "\n")

                # Disable editing
                text_widget.config(state=tk.DISABLED)

        except FileNotFoundError:
            label = tk.Label(self.result_frame, text="No logs found. Please add a new trip.", anchor="w")
            label.pack(fill=tk.X)

    def delete_log(self):
        # Show the input frame for entering the log number to delete
        self.input_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Clear the result frame
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        try:
            with open("fishing_log.csv", mode="r") as file:
                reader = csv.reader(file)
                header = next(reader)
                rows = list(reader)

                # Create a Text widget for displaying logs
                text_widget = tk.Text(self.result_frame, wrap=tk.NONE, font=("Courier", 10))
                text_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

                # Format and insert header
                header_line = "Index | " + " | ".join(f"{h:<15}" for h in header)
                text_widget.insert(tk.END, header_line + "\n")
                text_widget.insert(tk.END, "-" * len(header_line) + "\n")

                # Format and insert rows with index numbers
                for i, row in enumerate(rows):
                    row_line = f"{i + 1:<5} | " + " | ".join(f"{value:<15}" for value in row)
                    text_widget.insert(tk.END, row_line + "\n")

                # Disable editing
                text_widget.config(state=tk.DISABLED)

        except FileNotFoundError:
            label = tk.Label(self.result_frame, text="No logs found. Please add a new trip.", anchor="w")
            label.pack(fill=tk.X)

    def handle_delete_log(self):
        user_input = self.input_entry.get()
        self.input_entry.delete(0, tk.END)

        try:
            index = int(user_input) - 1
            filename = "fishing_log.csv"

            with open(filename, mode="r") as file:
                reader = csv.reader(file)
                header = next(reader)
                rows = list(reader)

            if index < 0 or index >= len(rows):
                messagebox.showerror("Error", "Invalid selection.")
                return

            rows.pop(index)

            with open(filename, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(header)
                writer.writerows(rows)

            messagebox.showinfo("Success", "Log deleted successfully!")

            # Refresh the log view
            self.delete_log()

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")
        except FileNotFoundError:
            messagebox.showerror("Error", "No log file found.")

    def show_stats(self):
        with open("fishing_log.csv", mode="r") as file:
            reader = csv.reader(file)
            next(reader)
            rows = list(reader)

            trips = len(rows)
            fish = sum(int(row[5]) for row in rows if row[5].isdigit())
            avg_fish_per_trip = round(fish / trips, 2) if trips else 0

            trips_by_location = defaultdict(int)
            fish_by_location = defaultdict(int)

            for row in rows:
                location = row[2].strip()
                trips_by_location[location] += 1
                if row[5].isdigit():
                    fish_by_location[location] += int(row[5])

            catch_rate_result = "\nCatch Rate by Lake:\n"
            for location in sorted(trips_by_location.keys()):
                trips = trips_by_location[location]
                fish = fish_by_location.get(location, 0)
                avg = round(fish / trips, 2) if trips else 0
                catch_rate_result += f"{location}: {fish} fish / {trips} trips → {avg} per trip\n"

            result = (
                f"Total trips: {trips}\n"
                f"Total fish caught: {fish}\n"
                f"Average fish per trip: {avg_fish_per_trip}\n"
                f"{catch_rate_result}"
            )
            self.display_result(result)

    def load_logs(self):
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        try:
            with open("fishing_log.csv", mode="r") as file:
                reader = csv.reader(file)
                next(reader)
                rows = list(reader)
                for row in rows:
                    log_entry = " | ".join(row)
                    label = tk.Label(self.result_frame, text=log_entry, anchor="w")
                    label.pack(fill=tk.X)
        except FileNotFoundError:
            label = tk.Label(self.result_frame, text="No logs found. Please add a new trip.", anchor="w")
            label.pack(fill=tk.X)

    def plot_fish_by_lake(self):
        with open("fishing_log.csv", mode="r") as file:
            reader = csv.reader(file)
            header = next(reader)
            rows = list(reader)

        fish_by_location = defaultdict(int)

        for row in rows:
            if len(row) > 5 and row[4].strip().lower() != "none":
                try:
                    location = row[2].strip()
                    fish = int(row[5])
                    fish_by_location[location] += fish
                except ValueError:
                    pass

        locations = list(fish_by_location.keys())
        fish_counts = list(fish_by_location.values())

        fig, ax = plt.subplots()
        ax.bar(locations, fish_counts, color='skyblue')
        ax.set_xlabel('Location')
        ax.set_ylabel('Number of Fish Caught')
        ax.set_title('Fish Caught by Location')
        ax.set_xticklabels(locations, rotation=45)

        self.display_plot(fig)

def main():
    root = tk.Tk()
    app = FishingLogApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()