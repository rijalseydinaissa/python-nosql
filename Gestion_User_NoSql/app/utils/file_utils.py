import pandas as pd

def exporter_csv(etudiants, filename="etudiants.csv"):
    df = pd.DataFrame(etudiants)
    df.to_csv(filename, index=False)
    print(f"Données exportées dans {filename}")

def importer_csv(filename="etudiants.csv"):
    df = pd.read_csv(filename)
    return df.to_dict(orient="records")
