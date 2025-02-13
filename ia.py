import pandas as pd
import streamlit as st
from pytrends.request import TrendReq

def buscar_palavras_chave(produto):
    """Busca palavras-chave relacionadas a um produto no Google Trends."""
    try:
        pytrends = TrendReq(hl='pt-BR', tz=0)
        pytrends.build_payload([produto], cat=0, timeframe='now 7-d', geo='', gprop='')

        related_queries = pytrends.related_queries()

        # Verifica se há dados para o termo pesquisado
        if not related_queries or produto not in related_queries:
            st.warning("⚠️ O Google Trends não retornou dados para esse termo.")
            return pd.DataFrame(columns=["Palavra-chave", "Popularidade"])

        # Obtém palavras-chave "top" (mais populares)
        data = related_queries[produto].get('top')
        
        if data is None or data.empty:
            st.warning("🔍 Nenhuma palavra-chave encontrada para este termo.")
            return pd.DataFrame(columns=["Palavra-chave", "Popularidade"])
        
        return data[['query', 'value']].rename(columns={"query": "Palavra-chave", "value": "Popularidade"})

    except Exception as e:
        st.error(f"❌ Erro ao buscar palavras-chave: {e}")
        return pd.DataFrame(columns=["Palavra-chave", "Popularidade"])

# Interface Streamlit
st.set_page_config(page_title="Pesquisa de Palavras-chave", page_icon="🔍", layout="centered")

st.title("🔎 Pesquisa de Palavras-chave no Google Trends")
st.write("Digite um nome de produto para ver as palavras-chave mais buscadas globalmente.")

produto = st.text_input("🔍 Nome do Produto:")

if produto:
    with st.spinner("🔄 Buscando palavras-chave..."):
        palavras_chave_df = buscar_palavras_chave(produto)

    if not palavras_chave_df.empty:
        st.success("✅ Resultados encontrados!")
        st.dataframe(palavras_chave_df)
    else:
        st.warning("⚠️ Nenhuma palavra-chave relevante foi encontrada.")

# Para rodar: streamlit run nome_do_arquivo.py
