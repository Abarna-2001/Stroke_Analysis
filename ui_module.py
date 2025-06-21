# ui_module.py
# A friendly Tkinter GUI that lets clinicians explore the stroke dataset with ease

import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import os
from dataset_module import load_dataset
from query_module import (
    query_smokers_hypertension_stroke,
    query_heart_disease_stroke,
    query_hypertension_by_gender,
    query_smoking_stroke_comparison,
    query_residence_stroke,
    query_dietary_habits,
    query_hypertension_stroke,
    query_hypertension_stroke_split,
    query_heart_disease_stroke_patients,
    query_descriptive_stats,
    query_sleep_hours,
    persist_to_csv
)

def format_result(result, indent=0):
    """
    Turns query results into a clean, readable string for the GUI’s text display.
    Handles None values nicely to avoid confusion for users.

    Args:
        result: The result from a query (could be a dict, list, or something else).
        indent (int): How many spaces to indent for nested results.

    Returns:
        str: A neatly formatted string, with None shown as 'No data'.
    """
    output = []  # Collect lines to display
    if isinstance(result, dict):
        # Loop through dictionary items to format them
        for key, value in result.items():
            if isinstance(value, dict):
                # Handle nested dictionaries with indentation
                output.append("  " * indent + f"{key}:")
                output.append(format_result(value, indent + 1))
            elif isinstance(value, list):
                # Turn lists into a comma-separated string
                output.append("  " * indent + f"{key}: {', '.join(map(str, value))}")
            else:
                # Show None as 'No data' 
                display_value = "No data" if value is None else value
                output.append("  " * indent + f"{key}: {display_value}")
    elif isinstance(result, list):
        # Handle lists, like patient IDs
        if not result:
            output.append("  " * indent + "No results found.")
        for i, item in enumerate(result, 1):
            output.append("  " * indent + f"{i}. {item}")
    else:
        # Handle all by converting to string
        output.append("  " * indent + str(result))
    return "\n".join(output)

class StrokeDataAnalyticsGUI:
    """
    The main Tkinter GUI class for exploring stroke data.
    Offers a dropdown to pick queries, a text area for results, and buttons to save or exit.
    """
    def __init__(self, root, dataset):
        """
        Sets up the GUI with the dataset and configures the window.

        Args:
            root (tk.Tk): The main Tkinter window.
            dataset (dict): The stroke dataset loaded from dataset_module.
        """
        self.root = root  # Store the main window
        self.dataset = dataset  # Store the dataset for queries
        self.current_result = None  # Keep track of the latest query result
        
        # Set up the window’s title and size
        self.root.title("Stroke Data Analytics")
        self.root.geometry("800x600")  # Wide enough for results
        
        # List all 11 queries
        # Each entry has a number, description, and the query function
        self.queries = [
            (1, "Average, modal, and median age of smokers with hypertension and stroke", query_smokers_hypertension_stroke),
            (2, "Age and glucose stats for heart disease and stroke patients", query_heart_disease_stroke),
            (3, "Age stats by gender for hypertension patients", query_hypertension_by_gender),
            (4, "Age stats for smokers with vs. without stroke", query_smoking_stroke_comparison),
            (5, "Age stats for urban vs. rural stroke patients", query_residence_stroke),
            (6, "Dietary habits with and without stroke", query_dietary_habits),
            (7, "Patients with hypertension and stroke", query_hypertension_stroke),
            (8, "Patients with hypertension, split by stroke", query_hypertension_stroke_split),
            (9, "Patients with heart disease and stroke", query_heart_disease_stroke_patients),
            (10, "Descriptive statistics for a specified feature", query_descriptive_stats),
            (11, "Average sleep hours with and without stroke", query_sleep_hours)
        ]
        
        # Build the GUI components
        self.create_widgets()
        
    def create_widgets(self):
        """
        Creates all the GUI elements: dropdown, text entry, buttons, and result display.
        Arranges them neatly for a clean user experience.
        """
        # Add a label to guide users
        tk.Label(self.root, text="Select Query:", font=("Arial", 12)).pack(pady=10)
        
        # Set up the dropdown menu for picking queries
        self.query_var = tk.StringVar(self.root)
        self.query_var.set("1")  # Start with the first query
        query_options = [f"{num}. {desc}" for num, desc, _ in self.queries]
        self.query_menu = tk.OptionMenu(self.root, self.query_var, *query_options, command=self.toggle_feature_entry)
        self.query_menu.pack(pady=5)
        
        # Create a frame for the feature input field (used for Query 10)
        self.feature_frame = tk.Frame(self.root)
        tk.Label(self.feature_frame, text="Feature Name:", font=("Arial", 12)).pack(side=tk.LEFT)
        self.feature_entry = tk.Entry(self.feature_frame, width=30)
        self.feature_entry.pack(side=tk.LEFT, padx=5)
        self.feature_entry.config(state="disabled")  # Disabled until Query 10 is selected
        self.feature_frame.pack(pady=5)
        
        # Add a button to run the selected query
        tk.Button(self.root, text="Run Query", command=self.run_query, font=("Arial", 12)).pack(pady=10)
        
        # Add a label and text area for showing query results
        tk.Label(self.root, text="Results:", font=("Arial", 12)).pack()
        self.result_text = tk.Text(self.root, height=15, width=80, font=("Arial", 10))
        self.result_text.pack(pady=5)
        # Include a scrollbar for scrolling through long results
        scrollbar = tk.Scrollbar(self.root, command=self.result_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.config(yscrollcommand=scrollbar.set)
        
        # Create a frame for the Save and Exit buttons
        button_frame = tk.Frame(self.root)
        tk.Button(button_frame, text="Save to CSV", command=self.save_result, font=("Arial", 12)).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Exit", command=self.root.quit, font=("Arial", 12)).pack(side=tk.LEFT, padx=10)
        button_frame.pack(pady=10)
        
        # Add a status label to show feedback, like “Saved!” or errors
        self.status_var = tk.StringVar()
        tk.Label(self.root, textvariable=self.status_var, font=("Arial", 11)).pack(pady=5)
        
    def toggle_feature_entry(self, *args):
        """
        Turns on the feature entry field for Query 10, turns it off and clears it for others.
        """
        selected = self.query_var.get().split(".")[0]
        self.feature_entry.config(state="normal" if selected == "10" else "disabled")
        if selected != "10":
            self.feature_entry.delete(0, tk.END)  # Clear old input
        
    def run_query(self):
        """
        Runs the chosen query and shows the results in the text area.
        Catches errors and handles None values for a smooth experience.
        """
        # Clear the text area and status message
        self.result_text.delete(1.0, tk.END)
        self.status_var.set("")
        
        # Get the query number from the dropdown
        selected = self.query_var.get().split(".")[0]
        try:
            query_num = int(selected)
        except ValueError:
            self.status_var.set("Oops! Pick a valid query number.")
            return
        
        # Find and run the selected query
        for num, _, func in self.queries:
            if num == query_num:
                try:
                    if func == query_descriptive_stats:
                        # Check if a feature name was entered for Query 10
                        feature = self.feature_entry.get().strip()
                        if not feature:
                            self.status_var.set("Please enter a feature name, like 'Age'.")
                            return
                        # Make sure the feature exists in the dataset
                        if feature not in self.dataset[list(self.dataset.keys())[0]]:
                            self.status_var.set(f"Sorry, '{feature}' isn’t in the dataset.")
                            return
                        result = func(self.dataset, feature)
                    else:
                        # Run the query with the dataset
                        result = func(self.dataset)
                    
                    # Save the result for CSV export
                    self.current_result = result
                    # Format and display the result
                    formatted_result = format_result(result)
                    self.result_text.insert(tk.END, formatted_result)
                    self.status_var.set("Query ran successfully! Check the results above.")
                except Exception as e:
                    self.status_var.set(f"Uh-oh, something went wrong: {str(e)}")
                return
        
        # If the query number doesn’t match
        self.status_var.set("Couldn’t find that query. Try again!")
        
    def save_result(self):
        """
        Saves the latest query result to a CSV file chosen by the user.
        """
        if self.current_result is None:
            self.status_var.set("Run a query first so there’s something to save!")
            return
        
        # Let the user pick a save location with a file dialog
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Save Query Results",
            initialdir=os.getcwd()
        )
        if filename:
            try:
                # Save the result using the query module’s function
                if persist_to_csv(self.current_result, filename):
                    self.status_var.set(f"Saved to {os.path.basename(filename)}!")
                else:
                    self.status_var.set("Couldn’t save the CSV. Check permissions or try a different name.")
            except Exception as e:
                self.status_var.set(f"Save failed: {str(e)}")
        else:
            self.status_var.set("No filename chosen, so nothing was saved.")

def run_user_interface(file_path):
    """
    Starts the GUI after loading the dataset and checking if we can save files.

    Args:
        file_path (str): Path to the data.csv file.

    Returns:
        None: Keeps running until the user clicks Exit.
    """
    # Try to load the dataset
    try:
        print(f"Trying to load dataset from {file_path}...")
        dataset = load_dataset(file_path)
        if not dataset:
            raise ValueError("The dataset is empty or not valid.")
        print(f"Successfully loaded {len(dataset)} patient records!")
    except Exception as e:
        # Show an error popup if loading fails
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Error", f"Couldn’t load the dataset: {str(e)}")
        root.destroy()
        return
    
    # Check if we have permission to save files in the current folder
    if not os.access(os.getcwd(), os.W_OK):
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Error", f"Can’t save files in {os.getcwd()}. Try running 'chmod u+w .' in your terminal.")
        root.destroy()
        return
    
    # Launch the GUI
    root = tk.Tk()
    app = StrokeDataAnalyticsGUI(root, dataset)
    root.mainloop()