import os
import glob
import pandas as pd
import re
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

def extrair_senioridade(texto):
    texto = texto.lower()
    if "sênior" in texto or "senior" in texto:
        return "Sênior"
    elif "pleno" in texto:
        return "Pleno"
    elif "júnior" in texto or "junior" in texto:
        return "Júnior"
    elif "estagiario" in texto or "estagiário" in texto:
        return "Estagiário"
    else:
        return "Não especificado"

def extrair_idioma(texto):
    texto = texto.lower()
    if "ingles" in texto or "inglês" in texto:
        return "Inglês"
    elif "espanhol" in texto:
        return "Espanhol"
    else:
        return "Não especificado"

def extrair_certificado(texto):
    texto = texto.lower()
    if "azure" in texto:
        return "Microsoft Azure"
    elif "aws" in texto:
        return "Amazon Web Service"
    elif "google" in texto or "gcp" in texto:
        return "Google Cloud"
    else:
        return "Não especificado"

def carregar_arquivo_raw():
    arquivos = glob.glob("data/raw/*_raw.csv")
    if not arquivos:
        raise FileNotFoundError("Nenhum arquivo raw encontrado em data/raw/")
    ultimo_arquivo = max(arquivos, key=os.path.getctime)
    print(f"Carregando arquivo: {ultimo_arquivo}")
    return pd.read_csv(ultimo_arquivo)

def main():
    df = carregar_arquivo_raw()
    
    # Preencher campos nulos com string vazia para evitar erro na concatenação
    df["title"] = df["title"].fillna("")
    df["description"] = df["description"].fillna("")
    
    # Criar coluna texto combinada para extração
    df["titulo_descr"] = df["title"] + " " + df["description"]
    
    # Extrair features
    df["senioridade"] = df["titulo_descr"].apply(extrair_senioridade)
    df["idioma"] = df["description"].apply(extrair_idioma)
    df["certificado"] = df["description"].apply(extrair_certificado)
    
    # Vetorização TF-IDF para clustering (usar apenas descrição e título)
    vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
    X = vectorizer.fit_transform(df["titulo_descr"])
    
    # Clustering KMeans (exemplo: 5 clusters)
    n_clusters = 5
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df["cluster"] = kmeans.fit_predict(X)
    
    # Salvar arquivo processado
    df.to_csv("data/processed/jobs_processed.csv", index=False, encoding="utf-8-sig")
    print("Arquivo processado salvo em data/processed/jobs_processed.csv")

if __name__ == "__main__":
    main()
