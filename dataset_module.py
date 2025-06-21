# dataset_module.py
# Loads stroke dataset from a CSV file into a nested dictionary for querying

def load_dataset(file_path):
    """
    Loads the stroke dataset from a CSV file into a nested dictionary for easy querying.
    
    Args:
        file_path (str): Path to the data.csv file containing stroke data.
        
    Returns:
        dict: Nested dictionary where each key is a unique record ID (e.g., "1") and
              the value is a dictionary of feature names (e.g., "Age", "Hypertension")
              mapped to their values. Example:
              {
                  "1": {
                      "Age": 78,
                      "Gender": "Female",
                      "Hypertension": 0,
                      "Stroke Occurrence": 0,
                      # ... other features
                  },
                  # ... other records
              }
              
    Raises:
        FileNotFoundError: If the CSV file doesn't exist at the specified path.
        ValueError: If the CSV is empty, malformed, or has no valid records.
    """
    dataset = {}  # Initialize dictionary to store patient records
    
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            
            if not lines:
                raise ValueError("CSV file is empty. Please check the file contents.")
            
            # Extract headers from the first row
            headers = lines[0].strip().split(",")
            
            # Expected number of columns based on dataset features (ID + 21 features)
            expected_columns = len(headers)
            if expected_columns < 2:
                raise ValueError(
                    f"Invalid header: found {expected_columns} columns. "
                    "Expected at least 2 (ID and one feature)."
                )
            
            # Process each data row to build patient records
            for line_num, line in enumerate(lines[1:], start=2):
                values = line.strip().split(",")
                
                # Skip rows with incorrect column counts
                if len(values) != expected_columns:
                    print(
                        f"Warning at row {line_num}: Expected {expected_columns} columns, "
                        f"found {len(values)}. Skipping this row."
                    )
                    continue
                
                record = {}  # Dictionary for this patient's data
                
                # Map headers to values, converting data types as needed
                for header, value in zip(headers, values):
                    # Numeric features stored as integers
                    if header == "Age":
                        try:
                            record[header] = int(value)
                        except ValueError:
                            print(
                                f"Warning at row {line_num}: Invalid age '{value}'. "
                                "Setting to None to avoid skewing queries."
                            )
                            record[header] = None
                    
                    # Numeric features stored as floats
                    elif header in ["Average Glucose Level", "BMI", "Sleep Hours", "Stroke Risk Score"]:
                        try:
                            record[header] = float(value)
                        except ValueError:
                            print(
                                f"Warning at row {line_num}: Invalid value '{value}' for {header}. "
                                "Setting to None to preserve data accuracy."
                            )
                            record[header] = None
                    
                    # Binary features (0 or 1) stored as integers
                    elif header in [
                        "Hypertension", "Heart Disease", "Ever Married",
                        "Alcohol Consumption", "Chronic Stress",
                        "Family History of Stroke", "Stroke Occurrence"
                    ]:
                        try:
                            if value not in ["0", "1"]:
                                raise ValueError("Expected 0 or 1")
                            record[header] = int(value)
                        except ValueError:
                            print(
                                f"Warning at row {line_num}: Invalid binary value '{value}' for {header}. "
                                "Setting to None to avoid errors."
                            )
                            record[header] = None
                    
                    # Categorical features stored as strings
                    else:
                        # Validate categorical values (example for Gender)
                        if header == "Gender" and value not in ["Male", "Female", "Other"]:
                            print(
                                f"Warning at row {line_num}: Invalid Gender '{value}'. "
                                "Keeping as it is but consider checking data."
                            )
                        record[header] = value
                
                # Store record using ID as key
                dataset[values[0]] = record
                
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{file_path}' not found. Please verify the path.")
    except Exception as e:
        raise ValueError(f"Error loading dataset: {str(e)}")
    
    # Check if any records were loaded
    if not dataset:
        raise ValueError("No valid records loaded. Check the CSV file for issues.")
    
    return dataset