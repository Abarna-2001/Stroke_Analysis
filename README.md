# STROKE DATA Prediction [Without Using High Level libraries]
This notebook is the main entry point for the Stroke Data Analytics project. It launches a user-friendly Tkinter GUI that lets clinicians explore a stroke dataset through 12 predefined queries.

- Compute the average, modal age, and median age of smokers with hypertension and stroke.
- Calculate age and glucose statistics for patients with heart disease and stroke.
- Compute age statistics by gender for patients with hypertension.
- Compare age statistics for smokers with and without stroke.
- Compare age statistics for urban versus rural stroke patients.
- Analyze dietary habits for patients with and without stroke.
- List patients with hypertension and stroke.
- List patients with hypertension, split by stroke status.
- List patients with heart disease and stroke.
- Compute descriptive statistics (mean, median, mode) for a user-specified
feature.
- Calculate the average sleep hours for patients with and without stroke.
- Save the query results to a CSV in a table format.

## 1. Overview
The project consists of four files:

- *dataset_module.py*: Loads the stroke dataset (data.csv) into a nested dictionary.
- *query_module.py*: Defines 12 queries to analyze the dataset (e.g., average age of smokers with stroke) and saves results to CSV.
- *ui_module.py*: Creates a Tkinter GUI with a dropdown for selecting queries, a text area for results, and buttons for saving to CSV or exiting.
- *main.ipynb*: Runs the GUI by calling ui_module.run_user_interface.
  
- The dataset (data.csv) contains patient data with 22 features, like Age, Hypertension, and Stroke Occurrence. The GUI makes it easy for clinicians to run queries and save results.

## Setup Instructions

Before running this notebook, make sure the environment is properly set up:

- **Python**  
  - Ensure Python 3.11 or higher is installed  
  - Check version using: `python3 --version`

- **Tkinter**  
  - Usually included with Python on Windows/macOS  
  - On Linux, install with: `sudo apt-get install python3-tk`

- **Dataset File**  
  - Place `data.csv` in the **same folder** as the notebook  
  - If placed elsewhere, update the `data_file` path in the code

- **Required Python Files**  
  Ensure the following files are in the same folder as the notebook:
  - `dataset_module.py`
  - `query_module.py`
  - `ui_module.py`

- **Write Permissions**  
  - For saving CSVs, ensure the current directory has write access  
  - On Linux: run `chmod u+w .` if you encounter permission errors

- **Jupyter Support**  
  - Use a Jupyter environment like **VS Code** or **Jupyter Notebook**  
  - These support GUI popups created with `Tkinter`


## 3. How to Run
Follow these steps to run and use the GUI application:

- Open the notebook in a Jupyter environment that supports GUI popups (e.g., **VS Code**, **Jupyter Notebook**)
- Run the code cell that launches the GUI
- In the GUI:
  - Select a query from the dropdown (e.g., `"1. Average, modal, and median age..."`)
  - For **Query 10**, enter a feature name (e.g., `"Age"`)
  - Click **"Run Query"** to display the results
  - Click **"Save to CSV"** to save the results to a file
  - Click **"Exit"** to close the GUI
- If you encounter errors (e.g., "file not found"), double-check:
  - File paths
  - Read/write permissions in the current directory
