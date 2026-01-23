import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Controle de Estoque - Bella Vista", layout="wide")

# Estilização CSS correta
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
    }
    .card {
        padding: 20px;
        background-color: white;
        border-radius: 10px;
        border: 1px solid #e5e7eb;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Inicialização do "Banco de Dados" na memória
if 'estoque' not in st.session_state:
    st.session_state.estoque = pd.DataFrame(columns=['Produto', 'Quantidade', 'Categoria', 'Última Atualização'])

st.title("📦 Controle de Estoque Bella Vista")

# Sidebar para cadastro
with st.sidebar:
    st.header("Cadastrar Novo Produto")
    nome = st.text_input("Nome do Produto")
    qtd = st.number_input("Quantidade Inicial", min_value=0, step=1)
    cat = st.selectbox("Categoria", ["Bebidas", "Alimentos", "Limpeza", "Outros"])
    
    if st.button("Adicionar ao Estoque"):
        if nome:
            novo_item = {
                'Produto': nome, 
                'Quantidade': qtd, 
                'Categoria': cat, 
                'Última Atualização': datetime.now().strftime("%d/%m/%Y %H:%M")
            }
            st.session_state.estoque = pd.concat([st.session_state.estoque, pd.DataFrame([novo_item])], ignore_index=True)
            st.success(f"{nome} adicionado!")
        else:
            st.error("Por favor, digite o nome do produto.")

# Área Principal - Visualização
st.subheader("Itens em Estoque")
if st.session_state.estoque.empty:
    st.info("Nenhum produto cadastrado ainda.")
else:
    # Exibe a tabela
    st.dataframe(st.session_state.estoque, use_container_width=True)
    
    # Botão para limpar tudo (Cuidado!)
    if st.button("Limpar Tudo"):
        st.session_state.estoque = pd.DataFrame(columns=['Produto', 'Quantidade', 'Categoria', 'Última Atualização'])
        st.rerun()
