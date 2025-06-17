import streamlit as st
import pandas as pd
import plotly.express as px

# Título da aplicação
st.set_page_config(page_title="Painel COVID-19", layout="wide")
st.title("📊 Painel de Monitoramento da COVID-19")
st.markdown("Dados obtidos de [Our World in Data](https://ourworldindata.org/coronavirus)")

# Carregar dados
@st.cache_data
def carregar_dados():
    url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
    df = pd.read_csv(url)
    df["date"] = pd.to_datetime(df["date"])
    return df

df = carregar_dados()

# Filtros
paises = df["location"].dropna().unique()
pais_selecionado = st.sidebar.selectbox("Selecione um país:", sorted(paises), index=sorted(paises).index("Brazil"))
dados_pais = df[df["location"] == pais_selecionado]

# Métricas principais
st.subheader(f"📍 Indicadores para {pais_selecionado}")
col1, col2, col3 = st.columns(3)

total_casos = int(dados_pais["total_cases"].dropna().max())
total_mortes = int(dados_pais["total_deaths"].dropna().max())
total_vacinados = int(dados_pais["people_fully_vaccinated"].dropna().max())

col1.metric("Total de Casos", f"{total_casos:,}")
col2.metric("Total de Mortes", f"{total_mortes:,}")
col3.metric("Total Vacinados", f"{total_vacinados:,}")

# Gráficos interativos
st.markdown("### Evolução temporal")

fig1 = px.line(
    dados_pais,
    x="date",
    y="new_cases",
    title="Novos casos diários",
    labels={"new_cases": "Novos Casos", "date": "Data"}
)
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.line(
    dados_pais,
    x="date",
    y="new_deaths",
    title="Novas mortes diárias",
    labels={"new_deaths": "Novas Mortes", "date": "Data"},
    color_discrete_sequence=["red"]
)
st.plotly_chart(fig2, use_container_width=True)

fig3 = px.line(
    dados_pais,
    x="date",
    y="people_fully_vaccinated",
    title="Pessoas totalmente vacinadas ao longo do tempo",
    labels={"people_fully_vaccinated": "Vacinados", "date": "Data"},
    color_discrete_sequence=["green"]
)
st.plotly_chart(fig3, use_container_width=True)

# Rodapé
st.markdown("---")
st.caption("Desenvolvido com 💻 por [Nicolas Freitas] - Dados públicos fornecidos por Our World in Data")
