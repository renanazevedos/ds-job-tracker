# Data Science Job Clustering

Durante minha transição de carreira para a área de Data Science, enfrentei um desafio comum: filtrar vagas relevantes em plataformas como o LinkedIn. Devido ao meu histórico profissional em Química Analítica, e apesar de já trabalhar com estatística aplicada, o algoritmo insistia em me recomendar sempre o mesmo tipo de vaga, sem apresentar vagas para meu novo direcionamento.

Essa experiência despertou a ideia deste projeto. Decidi aplicar técnicas de ciência de dados para investigar o próprio mercado de trabalho em Data Science. O projeto coleta automaticamente vagas do LinkedIn, realiza engenharia de features e aplica algoritmos de clustering para categorizar essas vagas de forma automatizada. Os resultados são apresentados em um dashboard interativo, que facilita a exploração dos diferentes perfis de vaga encontrados.

---

## 🎯 Objetivo

- Coletar vagas de Data Science no LinkedIn via web scraping  
- Processar e extrair informações relevantes das descrições  
- Aplicar TF-IDF e KMeans para agrupamento das vagas  
- Visualizar os grupos em um dashboard com Streamlit  

---

## 📁 Estrutura do Projeto

```
├── data
│   ├── raw                   # Dados brutos coletados do LinkedIn
│   └── processed             # Dados prontos para análise e visualização
├── notebooks                 # Análise e testes em Jupyter Notebooks
├── src
│   ├── linkedin_scraper.py   # Script de coleta de dados
│   └── process_jobs.py       # Engenharia de features e clustering
├── app.py                    # Aplicação Streamlit (dashboard)
├── main.py                   # Pipeline principal (coleta + processamento)
└── requirements.txt          # Dependências do projeto
```

---

## 🛠 Tecnologias Utilizadas

- Python 3.10+
- pandas, numpy
- scikit-learn (TF-IDF, KMeans)
- BeautifulSoup, requests
- Streamlit
- Plotly (para visualizações interativas)

---

## ▶️ Como Executar

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seuusuario/data-science-jobs.git
   cd data-science-jobs
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute a coleta e o processamento:**
   ```bash
   python main.py
   ```

4. **Rode o dashboard:**
   ```bash
   streamlit run app.py
   ```

---

## 📊 Funcionalidades do Dashboard

- Visualização da distribuição de vagas por cluster
- Filtro interativo para explorar diferentes grupos de vagas
- Exibição dos principais termos de cada cluster
- Links das vagas (copiáveis) para visualização no LinkedIn

---

## 💡 Melhorias Futuras

- Adição de novas variáveis no clustering (skills, localidade, senioridade, etc.)
- Classificação semiautomática de vagas com base em aprendizado supervisionado
- Deploy online do dashboard para acesso público
- Análises temporais com dados de múltiplos dias

---

## 🤝 Contribuições

Fique à vontade para abrir issues, sugerir melhorias ou contribuir com novas funcionalidades!

---

Desenvolvido por **[Renan](www.linkedin.com/in/renan-azevedos)**
