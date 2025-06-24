import os
import pandas as pd
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import json
from nltk.corpus import stopwords


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
    arquivo = os.path.join("data", "raw", "linkedin_datascience_jobs.csv")
    if not os.path.exists(arquivo):
        raise FileNotFoundError(f"{arquivo} não encontrado.")
    return pd.read_csv(arquivo)

def main():
    df = carregar_arquivo_raw()

    if 'data_coleta' not in df.columns:
        df['data_coleta'] = datetime.now().strftime('%Y-%m-%d')
    
    df["title"] = df["title"].fillna("")
    df["description"] = df["description"].fillna("")
    
    df["titulo_descr"] = df["title"] + " " + df["description"]
    
    # Extrair features
    df["senioridade"] = df["titulo_descr"].apply(extrair_senioridade)
    df["idioma"] = df["description"].apply(extrair_idioma)
    df["certificado"] = df["description"].apply(extrair_certificado)
    
    # Vetorização TF-IDF para clustering
    stopwords_custom =  stopwords.words("portuguese") + stopwords.words("english") + ['vaga', 'área', 'experiência', 'modelo', 'responsável','empresa', 'pessoa', 'atuar', 'informações', 'projeto', 'trabalho','pra','mundo','gente','quer','ter', 'vaga', 'nós', 'estar', 'será', 'todos', 'das', 'sempre', 'will', 'etc', 'fazer', 'aos', 'ano', 'os', 'até', 'suas', 'ser', 'além', 'pessoa', 'cada', 'à', 'todas', 'são', 'não', 'nos', 'sua', 'nossos', 'sobre', 'utilizando', 'nossa', 'onde', 'dia', 'todo', 'a', 'de', 'e', 'para', 'em', 'da', 'atividades', 'principais', 'do', 'somos', 'um', 'é', 'está', 'busca', 'buscando', 'dados', 'que', 'o', 'nosso', 'na', 'como', 'você', 'trabalhar', 'ou', 'mais','ao','seu','por','toda','less', 'more', 'Show', 'se', 'uma', 'dos', 'estamos', 'moreShow', 'você', 'deficiência', 'disability', 'odontológico', 'saúde', 'nossas', 'Entrevista', 'anos','parte','pelo', 'Desconto', 'aqui']
    vectorizer = TfidfVectorizer(stop_words=stopwords_custom, max_features=1000)
    X = vectorizer.fit_transform(df["titulo_descr"])
    
    # Clustering KMeans
    n_clusters = 5
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df["cluster"] = kmeans.fit_predict(X)
    
    output_path = os.path.join("data", "processed", "vagas_com_clusters.csv")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print("Arquivo processado salvo em data/processed/vagas_com_clusters.csv")

    # Extrair top termos por cluster
    top_terms = {}
    vocab = vectorizer.get_feature_names_out()
    for cluster_id in sorted(df['cluster'].unique()):
        mask = (df['cluster'] == cluster_id).to_numpy()
        termos_cluster = X[mask]
        termos_freq = termos_cluster.sum(axis=0).A1
        termos_dict = {vocab[i]: termos_freq[i] for i in range(len(vocab))}
        termos_ordenados = sorted(termos_dict.items(), key=lambda x: x[1], reverse=True)[:15]
        top_terms[str(cluster_id)] = [termo for termo, _ in termos_ordenados]

    with open(os.path.join("data", "processed", "top_terms.json"), "w", encoding="utf-8") as f:
        json.dump(top_terms, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()

