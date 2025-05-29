import pandas as pd
from datetime import date

today = date.today().isoformat()
raw_path = f"data/raw/{today}_raw.csv"
proc_path = "data/processed/jobs_processed.csv"

df = pd.read_csv(raw_path)

# extrair_senioridade, extrair_idioma, extrair_certificados, clusterizar, etc.

df["titulo_descr"] = df["title"].fillna("") + " " + df["description"].fillna("")
df["senioridade"]  = df["titulo_descr"].apply(extrair_senioridade)
df["idioma"]       = df["description"].apply(extrair_idioma)
df["certificados"] = df["description"].apply(extrair_certificados)

# clustering =
df["cluster"] = model_kmeans.predict(tfidf_vectorizer.transform(df["titulo_descr"]))
df["cluster_nome"] = df["cluster"].map(nome_clusters)

df.to_csv(proc_path, index=False, encoding="utf-8-sig")
print("Arquivo processado salvo:", proc_path)
