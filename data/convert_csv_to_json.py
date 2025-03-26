import pandas as pd

# Skriver inn navnet til CSV fila vår
csv_file = "london_weather.csv"

# Leser CSV fila
df = pd.read_csv(csv_file)

# Konverterer til JSON
json_file = "london_weather.json"
df.to_json(json_file, orient="records", indent=4)

print(f"Converted JSON saved as {json_file}")
