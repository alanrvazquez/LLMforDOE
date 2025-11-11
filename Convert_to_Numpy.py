import pandas as pd
import numpy as np
import io
import re
from datetime import datetime

# Load the updated CSV file
df = pd.read_csv("chatgpt_results/responses_chatgpt_n16_replicate5.csv")

# Generate dated filename
filename = f"numpy_results/parsed_responses_n16_replicate5.npy"

# Parser for embedded CSV tables
def parse_embedded_csv(response_str):
    if pd.isna(response_str):
        return None

    # Step 1: Remove code block markers and strip whitespace
    cleaned = response_str.replace("```csv", "").replace("```", "").strip()

    # Step 2: Split lines, clean trailing backslashes
    lines = [re.sub(r'\\$', '', line.strip()) for line in cleaned.split('\n') if line.strip()]
    if len(lines) < 2:
        return None

    # Step 3: Normalize whitespace and remove leading commas
    lines = [','.join([col.strip() for col in line.split(',')]) for line in lines]

    # Step 4: Validate column count
    header = lines[0].split(',')
    expected_cols = len(header)
    valid_data_rows = [row for row in lines[1:] if len(row.split(',')) == expected_cols]
    if not valid_data_rows:
        return None

    # Rebuild CSV content
    cleaned_csv = '\n'.join([','.join(header)] + valid_data_rows)

    try:
        df_parsed = pd.read_csv(io.StringIO(cleaned_csv))
        return df_parsed.to_numpy()
    except Exception as e:
        print("Failed to parse response:\n", cleaned_csv)
        return None

# Normalize responses that look like CSV tables but lack code markers
def enforce_csv_block(response):
    if pd.isna(response):
        return response

    # Fix mislabeled or missing block types
    response = re.sub(r'```(plaintext|text|tsv)', '```csv', response, flags=re.IGNORECASE)

    # If already wrapped with a block marker, leave as-is
    if "```csv" in response:
        return response

    # If it appears to be a CSV-like table (e.g., lines with commas and starting with digits or commas), wrap it
    if re.search(r"^\s*[,0-9]+\s*,", response.strip(), re.MULTILINE):
        return f"```csv\n{response.strip()}\n```"

    return response

df['Response'] = df['Response'].apply(enforce_csv_block)

# Apply parser to each response
df['ParsedResponse'] = df['Response'].apply(parse_embedded_csv)

# Filter valid arrays
valid_arrays = df['ParsedResponse'].dropna().to_list()
invalid_count = len(df) - len(valid_arrays)

# Create NumPy object array
valid_numpy_array = np.empty(len(valid_arrays), dtype=object)
for i, arr in enumerate(valid_arrays):
    valid_numpy_array[i] = arr



# Save the file
np.save(filename, valid_numpy_array)

# Summary output
print(f"Stored {len(valid_numpy_array)} valid responses to '{filename}'")
print(f"Found {len(valid_numpy_array)} valid arrays and {invalid_count} invalid arrays.")
print(valid_numpy_array)
