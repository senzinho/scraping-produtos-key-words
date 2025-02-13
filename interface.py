import streamlit as st
import requests
from bs4 import BeautifulSoup
from collections import Counter
import re

def extrair_palavras_chave(url):
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        texto = soup.get_text()
        
        palavras = re.findall(r'\b[a-zA-ZÀ-ÿ]{4,}\b', texto.lower())
        contagem = Counter(palavras)
        palavras_comuns = [palavra for palavra, freq in contagem.most_common(10)]
        
        return palavras_comuns
    except Exception as e:
        return [f"Erro: {e}"]

def main():
    st.title("Análise de Palavras-Chave e Produtos")
    
    url = st.text_input("Insira o link do site:")
    if st.button("Analisar"):
        if url:
            st.success(f"Analisando: {url}")
            palavras_chave = extrair_palavras_chave(url)
            
            st.subheader("Palavras-chave encontradas:")
            st.write(", ".join(palavras_chave))
        else:
            st.error("Por favor, insira um link válido.")
            
if __name__ == "__main__":
    main()
