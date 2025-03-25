import pandas as pd

# Replace with your actual CSV file name
csv_file = "LondonWeatherData.csv"

# Read the CSV file
df = pd.read_csv(csv_file)

# Convert to JSON
json_file = "LondonWeatherData.json"
df.to_json(json_file, orient="records", indent=4)

print(f"Converted JSON saved as {json_file}")
