def csv_til_json_london(csv_file="london_weather.csv", json_file="london_weather.json"):
    import pandas as pd
    df = pd.read_csv(csv_file)
    df.to_json(json_file, orient="records", indent=4)
    print(f"Konvertert til JSON og lagret som {json_file}")
