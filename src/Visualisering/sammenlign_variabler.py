def analyser_skydekke_solskinn(data_path=None):
    import pandas as pd
    import matplotlib.pyplot as plt
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import mean_squared_error, r2_score
    import os

    if data_path is None:
        data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'updated_london_weather.json')

    # Last inn data
    with open(data_path, 'r') as f:
        data = pd.read_json(f)

    # Sjekk at nødvendige kolonner finnes
    if 'cloud_cover' not in data.columns or 'sunshine' not in data.columns:
        raise ValueError("Filen må inneholde kolonnene 'cloud_cover' og 'sunshine'.")

    # Fjern rader med manglende verdier i relevante kolonner
    subset = data[['cloud_cover', 'sunshine']].dropna()

    # Beregn sentrale mål
    mean_sky = subset['cloud_cover'].mean()
    median_sky = subset['cloud_cover'].median()
    std_sky = subset['cloud_cover'].std()

    mean_sun = subset['sunshine'].mean()
    median_sun = subset['sunshine'].median()
    std_sun = subset['sunshine'].std()

    print(f"Skydekke - Gjennomsnitt: {mean_sky:.2f}, Median: {median_sky:.2f}, Std: {std_sky:.2f}")
    print(f"Solskinn  - Gjennomsnitt: {mean_sun:.2f}, Median: {median_sun:.2f}, Std: {std_sun:.2f}")

    X = subset[['cloud_cover']].values
    y = subset['sunshine'].values

    # Beregn korrelasjon
    corr = subset['cloud_cover'].corr(subset['sunshine'])
    print(f"Korrelasjon mellom skydekke og solskinn: {corr:.2f}")

    # Regresjon (forutsi solskinn basert på skydekke)
    model = LinearRegression()
    model.fit(X, y)
    pred = model.predict(X)
    print(f"Regresjonskoeffisient: {model.coef_[0]:.2f}, Intercept: {model.intercept_:.2f}")

    # Visualisering
    plt.figure(figsize=(8,5))
    plt.scatter(subset['cloud_cover'], subset['sunshine'], alpha=0.6, label='Data')
    plt.plot(subset['cloud_cover'], pred, color='red', label='Regresjonslinje')
    plt.xlabel('Skydekke (%)')
    plt.ylabel('Solskinn (timer)')
    plt.title('Sammenheng mellom skydekke og solskinn i London')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    analyser_skydekke_solskinn()
