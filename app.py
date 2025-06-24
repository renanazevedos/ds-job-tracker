import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import json

# Configurar janela
st.set_page_config(page_title="Análise de Clusters", layout="wide")
st.title("🔍 Vagas por Cluster")

# Carregar dados
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data/processed/vagas_com_clusters.csv")
        df["data_coleta"] = pd.to_datetime(df["data_coleta"])
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        return pd.DataFrame()

@st.cache_data
def load_top_terms():
    try:
        with open("data/processed/top_terms.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.warning(f"Não foi possível carregar os termos dos clusters: {e}")
        return {}


df = load_data()
top_terms = load_top_terms()

# Verificar carregamento
if 'cluster' not in df.columns:
    st.error("Arquivo não contém coluna 'cluster'. Verifique seu Jupyter Notebook.")
    st.stop()

# Clusters
cluster_labels = {
    0: "Generalistas/Corporativas",
    1: "Machine Learning",
    2: "BI/Análise",
    3: "Marketing Digital",
    4: "Engenharia de Dados"
}
df['cluster_label'] = df['cluster'].map(cluster_labels)

# Visualização
st.header("Distribuição dos Clusters")

fig = px.bar(
    df['cluster_label'].value_counts().reset_index(),
    x='cluster_label',
    y='count',
    orientation='v',
    labels={'cluster_label': 'Tipo de Vaga', 'count': 'Quantidade'},
    color='cluster_label',
    color_discrete_sequence=px.colors.qualitative.Pastel
)
fig.update_layout(title="Distribuição de Vagas por Cluster")
st.plotly_chart(fig, use_container_width=True)

# Explorador de vagas
st.divider()
st.header("Explorar Vagas por Cluster")

selected_cluster = st.selectbox(
    "Selecione um tipo de vaga:",
    options=list(cluster_labels.values())
)

# Pega o número do cluster correspondente ao rótulo
cluster_number = [k for k, v in cluster_labels.items() if v == selected_cluster][0]

# Exibir termos principais
if str(cluster_number) in top_terms:
    st.markdown("**🔑 Principais termos neste cluster:**")
    st.write(", ".join(top_terms[str(cluster_number)]))

# Filtrar e mostrar vagas
filtered_df = df[df['cluster_label'] == selected_cluster]
st.write(f"**{len(filtered_df)} vagas encontradas:**")

st.dataframe(
    filtered_df[['title', 'company', 'work_mode', 'data_coleta', 'link']],
    hide_index=True,
    height=400,
    use_container_width=True
)

#data
st.caption("Dashboard atualizado em " + datetime.now().strftime("%d/%m/%Y %H:%M"))
