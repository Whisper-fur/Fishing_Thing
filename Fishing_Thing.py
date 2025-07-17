# Imports
import csv
import matplotlib.pyplot as plt
from datetime import datetime
from collections import Counter, defaultdict
import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

# Logging Section
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

# Function for viewing logs
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


# Stats Section (First method) Keeping for memories
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

# GUI Section
class FishingLogApp:
    def __init__(self, root):
        root.title("Fishing Logbook")
        # root.attributes("-fullscreen", True)  # Removed fullscreen attribute

        # Set default window size
        root.geometry("800x600")

        # Create a frame for buttons
        button_frame = tk.Frame(root)
        button_frame.pack(side=tk.TOP, fill=tk.X)

        # Add buttons for menu options in two columns
        left_buttons = [
            ("View Logs", self.view_logs),
            ("Edit Logs", self.edit_logs),
            ("Delete Log", self.delete_log),
        ]

        right_buttons = [
            ("Bait Efficiency", self.bait_efficiency),
            ("Bait Performance Over Time", self.plot_bait_over_time),
            ("Seasonal Trend Breakdown", self.seasonal_trend_breakdown),
            ("Catch Rate Over Time", self.catch_rate_over_time),
            ("Outlier Detection", self.outlier_detection)
        ]

    

        # Add left column buttons
        left_frame = tk.Frame(button_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        # Add header above left column buttons
        tk.Label(left_frame, text="Log Options", font=("Arial", 12, "bold")).pack(pady=5)

        for text, command in left_buttons:
            tk.Button(left_frame, text=text, command=command).pack(fill=tk.X, pady=2)

        # Add a thin gray line between columns
        separator = tk.Frame(button_frame, width=2, bg="gray")
        separator.pack(side=tk.LEFT, fill=tk.Y, padx=5)

        # Add right column buttons
        right_frame = tk.Frame(button_frame)
        right_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        # Add header above right column buttons
        tk.Label(right_frame, text="Statistics", font=("Arial", 12, "bold")).pack(pady=5)

        for text, command in right_buttons[:-1]:  # Exclude "Outlier Detection"
            tk.Button(right_frame, text=text, command=command).pack(fill=tk.X, pady=2)

        # Add another separator for "Outlier Detection"
        separator_outlier = tk.Frame(button_frame, width=2, bg="gray")
        separator_outlier.pack(side=tk.LEFT, fill=tk.Y, padx=5)

        # Add "Outlier Detection" button separately
        outlier_frame = tk.Frame(button_frame)
        outlier_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        # Add header above "Outlier Detection" button
        tk.Label(outlier_frame, text="Data Cleaning", font=("Arial", 12, "bold")).pack(pady=5)

        tk.Button(outlier_frame, text="Outlier Detection", command=self.outlier_detection).pack(fill=tk.X, pady=2)

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

# Utilities Section
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

    def new_trip(self): #TODO: Implement new trip functionality
        return

    # Logging Section
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

                # Calculate column widths based on the longest value in each column
                column_widths = [max(len(str(value)) for value in col) for col in zip(header, *rows)]

                # Format and insert header
                header_line = "Index | " + " | ".join(f"{h:<{column_widths[i]}}" for i, h in enumerate(header))
                text_widget.insert(tk.END, header_line + "\n")
                text_widget.insert(tk.END, "-" * len(header_line) + "\n")

                # Format and insert rows with index numbers
                for i, row in enumerate(rows):
                    row_line = f"{i + 1:<5} | " + " | ".join(f"{value:<{column_widths[j]}}" for j, value in enumerate(row))
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

#Check if this is still needed
    def show_stats(self):
        # Hide the input frame as it's not needed for showing stats
        self.input_frame.pack_forget()

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


#Visualization Section
    def bait_efficiency(self):
        # Hide the input frame as it's not needed for bait efficiency
        self.input_frame.pack_forget()

        # Clear the result frame
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        try:
            with open("fishing_log.csv", mode="r") as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                rows = list(reader)

            bait_usage = defaultdict(int)
            fish_by_bait = defaultdict(int)

            for row in rows:
                if len(row) > 6 and row[6].strip() != "":
                    bait = row[6].strip()
                    bait_usage[bait] += 1
                    if len(row) > 5 and row[5].strip().isdigit():
                        fish_by_bait[bait] += int(row[5])

            # Prepare data for the bar chart
            bait_efficiency_data = sorted(
                ((bait, fish_by_bait[bait] / bait_usage[bait]) for bait in bait_usage),
                key=lambda x: x[1],
                reverse=True
            )
            baits = [item[0] for item in bait_efficiency_data]
            efficiency = [item[1] for item in bait_efficiency_data]

            # Create the bar chart
            fig, ax = plt.subplots()
            ax.bar(baits, efficiency, color='skyblue')
            ax.set_xlabel('Bait')
            ax.set_ylabel('Efficiency (Fish per Use)')
            ax.set_title('Bait Efficiency Ranking')
            ax.set_xticklabels(baits, rotation=45)

            # Adjust layout to prevent label cutoff
            plt.tight_layout()

            # Display the plot dynamically sized with the window
            canvas = FigureCanvasTkAgg(fig, master=self.result_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

            # Close the figure to prevent memory leaks
            plt.close(fig)

        except FileNotFoundError:
            label = tk.Label(self.result_frame, text="No logs found. Please add a new trip.", anchor="w")
            label.pack(fill=tk.X)

    def plot_bait_over_time(self):
        # Hide the input frame as it's not needed for plotting bait performance over time
        self.input_frame.pack_forget()

        with open("fishing_log.csv", mode="r") as file:
            reader = csv.reader(file)
            header = next(reader)
            rows = list(reader)

        # Group data by quarters and bait types
        quarterly_catch_by_bait = defaultdict(lambda: defaultdict(int))
        quarterly_trips_by_bait = defaultdict(lambda: defaultdict(int))

        for row in rows:
            if len(row) > 6 and row[6].strip() != "":
                try:
                    date = datetime.strptime(row[0], "%Y-%m-%d")
                    quarter = f"Q{(date.month - 1) // 3 + 1} {date.year}"  # Format as Quarter-Year
                    bait = row[6].strip()
                    fish_caught = int(row[5]) if row[5].strip().isdigit() else 0
                    quarterly_catch_by_bait[bait][quarter] += fish_caught
                    quarterly_trips_by_bait[bait][quarter] += 1
                except ValueError:
                    pass

        # Prepare data for plotting
        fig, ax = plt.subplots()
        for bait, quarterly_catch in quarterly_catch_by_bait.items():
            quarters = sorted(quarterly_catch.keys())
            catch_rates = [
                round(quarterly_catch[quarter] / quarterly_trips_by_bait[bait][quarter], 2) if quarterly_trips_by_bait[bait][quarter] > 0 else 0
                for quarter in quarters
            ]
            ax.plot(quarters, catch_rates, label=bait)

        ax.set_xlabel("Quarter")
        ax.set_ylabel("Catch Rate (Fish per Trip)")
        ax.set_title("Bait Performance Over Time (Grouped by Quarter)")
        ax.tick_params(axis="x", rotation=45)
        ax.grid(True, linestyle='--', alpha=0.5)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()

        # Display the plot dynamically sized with the window
        self.display_plot(fig)

        # Close the figure to prevent memory leaks
        plt.close(fig)

    def seasonal_trend_breakdown(self):
        # Hide the input frame as it's not needed for seasonal trend breakdown
        self.input_frame.pack_forget()

        with open("fishing_log.csv", mode="r") as file:
            reader = csv.reader(file)
            header = next(reader)
            rows = list(reader)

        # Group data by seasons
        seasonal_catch = defaultdict(int)
        seasonal_trips = defaultdict(int)

        for row in rows:
            if len(row) > 5 and row[5].strip().isdigit():
                try:
                    date = datetime.strptime(row[0], "%Y-%m-%d")
                    month = date.month
                    fish_caught = int(row[5])

                    # Determine season based on month
                    if month in [12, 1, 2]:
                        season = "Winter"
                    elif month in [3, 4, 5]:
                        season = "Spring"
                    elif month in [6, 7, 8]:
                        season = "Summer"
                    else:
                        season = "Fall"

                    seasonal_catch[season] += fish_caught
                    seasonal_trips[season] += 1
                except ValueError:
                    pass

        # Prepare data for plotting
        seasons = ["Winter", "Spring", "Summer", "Fall"]
        catch_rates = [
            round(seasonal_catch[season] / seasonal_trips[season], 2) if seasonal_trips[season] > 0 else 0
            for season in seasons
        ]

        # Create the bar chart
        fig, ax = plt.subplots()
        ax.bar(seasons, catch_rates, color='lightgreen')
        ax.set_xlabel("Season")
        ax.set_ylabel("Catch Rate (Fish per Trip)")
        ax.set_title("Seasonal Trend Breakdown")
        ax.grid(True, linestyle='--', alpha=0.5)

        # Display the plot dynamically sized with the window
        self.display_plot(fig)

        # Close the figure to prevent memory leaks
        plt.close(fig)

    def catch_rate_over_time(self):
        # Hide the input frame as it's not needed for plotting catch rate over time
        self.input_frame.pack_forget()

        with open("fishing_log.csv", mode="r") as file:
            reader = csv.reader(file)
            header = next(reader)
            rows = list(reader)

        # Group data by quarters
        quarterly_catch = defaultdict(int)
        quarterly_trips = defaultdict(int)

        for row in rows:
            if len(row) > 5 and row[5].strip().isdigit():
                try:
                    date = datetime.strptime(row[0], "%Y-%m-%d")
                    quarter = f"Q{(date.month - 1) // 3 + 1} {date.year}"  # Format as Quarter-Year
                    fish_caught = int(row[5])
                    quarterly_catch[quarter] += fish_caught
                    quarterly_trips[quarter] += 1
                except ValueError:
                    pass

        quarters = sorted(quarterly_catch.keys())
        catch_rates = [
            round(quarterly_catch[quarter] / quarterly_trips[quarter], 2) if quarterly_trips[quarter] > 0 else 0
            for quarter in quarters
        ]

        # Ensure pandas DataFrame is created correctly
        df = pd.DataFrame({'quarter': quarters, 'rate': catch_rates})
        df['moving_avg'] = df['rate'].rolling(window=2, center=True).mean()

        # Create the line graph
        fig, ax = plt.subplots()
        ax.plot(df['quarter'], df['rate'], color='steelblue', linewidth=2.5, marker='o', markersize=6, label='Catch Rate')
        ax.plot(df['quarter'], df['moving_avg'], color='orange', linestyle='--', linewidth=2, label='2-quarter Moving Avg')

        ax.set_xlabel("Quarter")
        ax.set_ylabel("Catch Rate (Fish per Trip)")
        ax.set_title("Catch Rate Over Time (Grouped by Quarter)")
        ax.tick_params(axis="x", rotation=45)
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.legend()

        # Adjust layout to prevent label cutoff
        plt.tight_layout()

        # Display the plot dynamically sized with the window
        self.display_plot(fig)

        # Close the figure to prevent memory leaks
        plt.close(fig)

    
# Data Cleaning Section
    def outlier_detection(self):
        return

# Main Function
def main():
    root = tk.Tk()
    app = FishingLogApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()