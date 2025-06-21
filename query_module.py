# query_module.py
# Handles querying of the stroke dataset for analysis, supporting clinician insights

import math

# Helper function to calculate the average of numeric values, skipping None
def calculate_mean(values):
    """
    Computes the average of a list of numbers, ignoring None values.

    Args:
        values (list): List of numbers (e.g., ages, glucose levels).

    Returns:
        float: Mean value, or None if no valid numbers.
    """
    valid_values = [x for x in values if x is not None]
    if not valid_values:
        return None  # Return None to indicate no valid data
    return sum(valid_values) / len(valid_values)

# Helper function to find the middle value of a sorted list, skipping None
def calculate_median(values):
    """
    Computes the median of a list of numbers, ignoring None values.

    Args:
        values (list): List of numbers.

    Returns:
        float: Median value, or None if no valid numbers.
    """
    valid_values = [x for x in values if x is not None]
    if not valid_values:
        return None
    sorted_values = sorted(valid_values)
    n = len(sorted_values)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_values[mid - 1] + sorted_values[mid]) / 2
    return sorted_values[mid]

# Helper function to find the most frequent value(s), skipping None
def calculate_mode(values):
    """
    Computes the mode(s) of a list, handling multimodal cases and ignoring None.

    Args:
        values (list): List of values (e.g., ages).

    Returns:
        list: List of mode(s), empty if no valid values.
    """
    valid_values = [x for x in values if x is not None]
    if not valid_values:
        return []
    frequency = {}
    for value in valid_values:
        frequency[value] = frequency.get(value, 0) + 1
    max_freq = max(frequency.values())
    return [value for value, freq in frequency.items() if freq == max_freq]

# Helper function to calculate standard deviation, skipping None
def calculate_std_dev(values, mean=None):
    """
    Computes standard deviation to measure data spread, ignoring None values.

    Args:
        values (list): List of numbers.
        mean (float, optional): Precomputed mean for efficiency.

    Returns:
        float: Standard deviation, or None if fewer than 2 valid values.
    """
    valid_values = [x for x in values if x is not None]
    if len(valid_values) < 2:
        return None
    if mean is None:
        mean = calculate_mean(valid_values)
    if mean is None:
        return None
    squared_diff_sum = sum((x - mean) ** 2 for x in valid_values)
    return math.sqrt(squared_diff_sum / len(valid_values))

# Helper function to compute percentiles, skipping None
def calculate_percentiles(values, percentiles=[25, 50, 75]):
    """
    Computes percentiles (e.g., 25th, 50th, 75th) for data distribution.

    Args:
        values (list): List of numbers.
        percentiles (list): Percentiles to compute (default: [25, 50, 75]).

    Returns:
        dict: Maps percentiles to values, or None if no valid numbers.
    """
    valid_values = [x for x in values if x is not None]
    if not valid_values:
        return {p: None for p in percentiles}
    sorted_values = sorted(valid_values)
    n = len(sorted_values)
    results = {}
    for p in percentiles:
        k = (n - 1) * (p / 100)
        f, i = math.modf(k)
        i = int(i)
        if i + 1 < n:
            results[p] = sorted_values[i] + f * (sorted_values[i + 1] - sorted_values[i])
        else:
            results[p] = sorted_values[i]
    return results

# --- Query Functions for Stroke Data Analysis ---

# Query 1: Analyze ages of smokers with hypertension and stroke
def query_smokers_hypertension_stroke(dataset):
    """
    Finds average, modal, and median age for smokers with hypertension and stroke.

    Args:
        dataset (dict): Nested dictionary from dataset_module.

    Returns:
        dict: Contains mean_age, modal_age, median_age; None or [] for empty results.
    """
    # Filter for smokers (not "Never smoked"), with hypertension and stroke
    ages = [
        record["Age"]
        for record in dataset.values()
        if record["Smoking Status"] not in ["Never smoked", "Unknown"]
        and record["Hypertension"] == 1
        and record["Stroke Occurrence"] == 1
    ]
    return {
        "mean_age": calculate_mean(ages),
        "modal_age": calculate_mode(ages),
        "median_age": calculate_median(ages)
    }

# Query 2: Analyze age and glucose levels for heart disease and stroke patients
def query_heart_disease_stroke(dataset):
    """
    Computes age statistics and average glucose level for heart disease and stroke patients.

    Args:
        dataset (dict): Nested dictionary from dataset_module.

    Returns:
        dict: Includes mean_age, modal_age, median_age, mean_glucose; None or [] for empty results.
    """
    ages = []
    glucose_levels = []
    for record in dataset.values():
        if record["Heart Disease"] == 1 and record["Stroke Occurrence"] == 1:
            ages.append(record["Age"])
            glucose_levels.append(record["Average Glucose Level"])
    return {
        "mean_age": calculate_mean(ages),
        "modal_age": calculate_mode(ages),
        "median_age": calculate_median(ages),
        "mean_glucose": calculate_mean(glucose_levels)
    }

# Query 3: Break down age statistics by gender for hypertension patients
def query_hypertension_by_gender(dataset):
    """
    Computes age statistics by gender for hypertension patients, split by stroke.

    Args:
        dataset (dict): Nested dictionary from dataset_module.

    Returns:
        dict: Nested results for each gender, with stroke/no_stroke stats.
    """
    # Get unique genders dynamically from dataset
    genders = set(record["Gender"] for record in dataset.values() if record["Gender"] is not None)
    results = {gender: {"stroke": {}, "no_stroke": {}} for gender in genders}
    
    for gender in genders:
        stroke_ages = [
            record["Age"]
            for record in dataset.values()
            if record["Gender"] == gender
            and record["Hypertension"] == 1
            and record["Stroke Occurrence"] == 1
        ]
        no_stroke_ages = [
            record["Age"]
            for record in dataset.values()
            if record["Gender"] == gender
            and record["Hypertension"] == 1
            and record["Stroke Occurrence"] == 0
        ]
        results[gender]["stroke"] = {
            "mean_age": calculate_mean(stroke_ages),
            "modal_age": calculate_mode(stroke_ages),
            "median_age": calculate_median(stroke_ages)
        }
        results[gender]["no_stroke"] = {
            "mean_age": calculate_mean(no_stroke_ages),
            "modal_age": calculate_mode(no_stroke_ages),
            "median_age": calculate_median(no_stroke_ages)
        }
    return results

# Query 4: Compare age statistics for smokers with and without stroke
def query_smoking_stroke_comparison(dataset):
    """
    Computes age statistics for smokers, comparing those with vs. without stroke.

    Args:
        dataset (dict): Nested dictionary from dataset_module.

    Returns:
        dict: Contains stroke and no_stroke groups with age statistics.
    """
    # Filter for smokers (not "Never smoked" or "Unknown")
    stroke_ages = [
        record["Age"]
        for record in dataset.values()
        if record["Smoking Status"] not in ["Never smoked", "Unknown"]
        and record["Stroke Occurrence"] == 1
    ]
    no_stroke_ages = [
        record["Age"]
        for record in dataset.values()
        if record["Smoking Status"] not in ["Never smoked", "Unknown"]
        and record["Stroke Occurrence"] == 0
    ]
    return {
        "stroke": {
            "mean_age": calculate_mean(stroke_ages),
            "modal_age": calculate_mode(stroke_ages),
            "median_age": calculate_median(stroke_ages)
        },
        "no_stroke": {
            "mean_age": calculate_mean(no_stroke_ages),
            "modal_age": calculate_mode(no_stroke_ages),
            "median_age": calculate_median(no_stroke_ages)  
        }
    }

# Query 5: Analyze age statistics for stroke patients in urban vs. rural areas
def query_residence_stroke(dataset):
    """
    Computes age statistics for stroke patients, comparing urban vs. rural residence.

    Args:
        dataset (dict): Nested dictionary from dataset_module.

    Returns:
        dict: Contains urban and rural groups with age statistics.
    """
    # Get unique residence types dynamically
    residence_types = set(record["Residence Type"] for record in dataset.values() if record["Residence Type"] is not None)
    results = {res: {"mean_age": None, "modal_age": [], "median_age": None} for res in residence_types}
    
    for res in residence_types:
        ages = [
            record["Age"]
            for record in dataset.values()
            if record["Residence Type"] == res
            and record["Stroke Occurrence"] == 1
        ]
        results[res] = {
            "mean_age": calculate_mean(ages),
            "modal_age": calculate_mode(ages),
            "median_age": calculate_median(ages)
        }
    return results

# Query 6: List unique dietary habits for patients with and without stroke
def query_dietary_habits(dataset):
    """
    Retrieves unique dietary habits, split by stroke occurrence.

    Args:
        dataset (dict): Nested dictionary from dataset_module.

    Returns:
        dict: Contains stroke and no_stroke lists of unique dietary habits.
    """
    stroke_diets = [
        record["Dietary Habits"]
        for record in dataset.values()
        if record["Stroke Occurrence"] == 1 and record["Dietary Habits"] is not None
    ]
    no_stroke_diets = [
        record["Dietary Habits"]
        for record in dataset.values()
        if record["Stroke Occurrence"] == 0 and record["Dietary Habits"] is not None
    ]
    return {
        "stroke": list(set(stroke_diets)),
        "no_stroke": list(set(no_stroke_diets))
    }

# Query 7: Identify patients with hypertension and stroke
def query_hypertension_stroke(dataset):
    """
    Retrieves IDs of patients with hypertension and stroke.

    Args:
        dataset (dict): Nested dictionary from dataset_module.

    Returns:
        list: List of patient IDs (strings).
    """
    return [
        record["ID"]
        for record in dataset.values()
        if record["Hypertension"] == 1
        and record["Stroke Occurrence"] == 1
        and isinstance(record["ID"], str)
    ]

# Query 8: Identify hypertension patients, split by stroke occurrence
def query_hypertension_stroke_split(dataset):
    """
    Retrieves IDs of hypertension patients, separated by stroke occurrence.

    Args:
        dataset (dict): Nested dictionary from dataset_module.

    Returns:
        dict: Contains stroke and no_stroke lists of patient IDs.
    """
    stroke_ids = [
        record["ID"]
        for record in dataset.values()
        if record["Hypertension"] == 1
        and record["Stroke Occurrence"] == 1
        and isinstance(record["ID"], str)
    ]
    no_stroke_ids = [
        record["ID"]
        for record in dataset.values()
        if record["Hypertension"] == 1
        and record["Stroke Occurrence"] == 0
        and isinstance(record["ID"], str)
    ]
    return {
        "stroke": stroke_ids,
        "no_stroke": no_stroke_ids
    }

# Query 9: Identify patients with heart disease and stroke
def query_heart_disease_stroke_patients(dataset):
    """
    Retrieves IDs of patients with heart disease and stroke.

    Args:
        dataset (dict): Nested dictionary from dataset_module.

    Returns:
        list: List of patient IDs (strings).
    """
    return [
        record["ID"]
        for record in dataset.values()
        if record["Heart Disease"] == 1
        and record["Stroke Occurrence"] == 1
        and isinstance(record["ID"], str)
    ]

# Query 10: Provide detailed statistics for a user-specified feature
def query_descriptive_stats(dataset, feature):
    """
    Computes statistics (mean, std dev, min, max, percentiles) for a feature.

    Args:
        dataset (dict): Nested dictionary from dataset_module.
        feature (str): Feature name (e.g., "Age").

    Returns:
        dict: Contains statistics or error message if feature is invalid.
    """
    if not dataset or feature not in dataset[list(dataset.keys())[0]]:
        return {"error": f"Feature '{feature}' not found or dataset is empty."}
    
    values = [
        record[feature]
        for record in dataset.values()
        if record[feature] is not None and isinstance(record[feature], (int, float))
    ]
    if not values:
        return {"error": "No valid numerical values found for the feature."}
    
    mean = calculate_mean(values)
    return {
        "mean": mean,
        "std_dev": calculate_std_dev(values, mean),
        "min": min(values),
        "max": max(values),
        **calculate_percentiles(values, [25, 50, 75])
    }

# Query 11: Compare average sleep hours for patients with and without stroke
def query_sleep_hours(dataset):
    """
    Computes average sleep hours, split by stroke occurrence.

    Args:
        dataset (dict): Nested dictionary from dataset_module.

    Returns:
        dict: Contains stroke and no_stroke average sleep hours.
    """
    stroke_sleep = [
        record["Sleep Hours"]
        for record in dataset.values()
        if record["Stroke Occurrence"] == 1 and record["Sleep Hours"] is not None
    ]
    no_stroke_sleep = [
        record["Sleep Hours"]
        for record in dataset.values()
        if record["Stroke Occurrence"] == 0 and record["Sleep Hours"] is not None
    ]
    return {
        "stroke": calculate_mean(stroke_sleep),
        "no_stroke": calculate_mean(no_stroke_sleep)
    }

# Query 12: Save query results to a CSV file
def persist_to_csv(data, output_file):
    """
    Saves query results to a CSV file in a tabular format for clinician use.

    Args:
        data: Query result (dict or list).
        output_file (str): Path to the output CSV file.

    Returns:
        bool: True if saved successfully, False otherwise.
    """
    try:
        with open(output_file, "w") as file:
            if isinstance(data, dict):
                # Write header based on data structure
                if "stroke" in data and isinstance(data["stroke"], dict):
                    # For queries with stroke/no_stroke groups (e.g., Query 4, 5, 11)
                    file.write("Group,Mean,Mode,Median\n")
                    for group, stats in data.items():
                        modes = ",".join(map(str, stats.get("modal_age", stats.get("mode", []))))
                        median = stats.get("median_age", stats.get("median", "N/A"))
                        mean = stats.get("mean_age", stats.get("mean", "N/A"))
                        file.write(f"{group},{mean},{modes},{median}\n")
                elif all(isinstance(v, dict) for v in data.values()):
                    # For nested results (e.g., Query 3)
                    file.write("Gender,Group,Mean,Mode,Median\n")
                    for gender, groups in data.items():
                        for group, stats in groups.items():
                            modes = ",".join(map(str, stats["modal_age"]))
                            file.write(f"{gender},{group},{stats['mean_age']},{modes},{stats['median_age']}\n")
                else:
                    # For simple key-value results (e.g., Query 10)
                    file.write("Statistic,Value\n")
                    for key, value in data.items():
                        file.write(f"{key},{value}\n")
            
            elif isinstance(data, list):
                # Write list of IDs (e.g., Query 7, 9)
                file.write("Patient_ID\n")
                for item in data:
                    file.write(f"{item}\n")
            
            else:
                return False
        return True
    except Exception as e:
        print(f"Failed to save CSV: {e}")
        return False