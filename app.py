import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configuração da Página
st.set_page_config(page_title="Bella Vista - Gestão de Estoque", layout="wide", page_icon="📦")

# 2. Estilização CSS Corrigida (O erro estava aqui)
st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    .stMetric { background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    div[data-testid="stExpander"] { border: none !important; box-shadow: none !important; }
    .footer { position: fixed; bottom: 0; width: 100%; text-align: center; color: gray; font-size: 12px; }
    </style>
    """, unsafe_allow_html=True)

# 3. Inicialização do Estado (Banco de dados temporário)
if 'estoque' not in st.session_state:
    # Dados iniciais de exemplo
    dados_iniciais = [
        {'Produto': 'Cerveja Lata', 'Quantidade': 50, 'Categoria': 'Bebidas', 'Preço': 5.50},
        {'Produto': 'Água sem Gás', 'Quantidade': 20, 'Categoria': 'Bebidas', 'Preço': 3.00}
    ]
    st.session_state.estoque = pd.DataFrame(dados_iniciais)

# --- CABEÇALHO ---
st.title("📦 Sistema de Estoque Bella Vista")
st.write(f"Hoje é: {datetime.now().strftime('%d/%m/%Y')}")

# --- DASHBOARD DE MÉTRICAS ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total de Itens", len(st.session_state.estoque))
with col2:
    total_unidades = st.session_state.estoque['Quantidade'].sum()
    st.metric("Total de Unidades", int(total_unidades))
with col3:
    st.metric("Alertas de Estoque Baixo", len(st.session_state.estoque[st.session_state.estoque['Quantidade'] < 5]))

st.divider()

# --- BARRA LATERAL: CADASTRO ---
with st.sidebar:
    st.header("➕ Novo Produto")
    novo_nome = st.text_input("Nome do Produto")
    nova_cat = st.selectbox("Categoria", ["Bebidas", "Alimentos", "Limpeza", "Higiene", "Outros"])
    nova_qtd = st.number_input("Quantidade", min_value=0, step=1)
    novo_preco = st.number_input("Preço Unitário (R$)", min_value=0.0, step=0.50)
    
    if st.button("Cadastrar no Sistema"):
        if novo_nome:
            novo_item = pd.DataFrame([{'Produto': novo_nome, 'Quantidade': nova_qtd, 'Categoria': nova_cat, 'Preço': novo_preco}])
            st.session_state.estoque = pd.concat([st.session_state.estoque, novo_item], ignore_index=True)
            st.success("Produto cadastrado!")
            st.rerun()
        else:
            st.warning("O nome é obrigatório.")

# --- CORPO PRINCIPAL: BUSCA E TABELA ---
st.subheader("🔍 Gerenciamento de Itens")
busca = st.text_input("Pesquisar produto pelo nome...", "")

# Filtragem
df_filtrado = st.session_state.estoque
if busca:
    df_filtrado = df_filtrado[df_filtrado['Produto'].str.contains(busca, case=False)]

# Exibição e Edição
if not df_filtrado.empty:
    for index, row in df_filtrado.iterrows():
        with st.expander(f"{row['Produto']} - {row['Quantidade']} un ({row['Categoria']})"):
            c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
            with c1:
                st.write(f"**Preço:** R$ {row['Preço']:.2f}")
            with c2:
                if st.button("➕ Adicionar 1", key=f"add_{index}"):
                    st.session_state.estoque.at[index, 'Quantidade'] += 1
                    st.rerun()
            with c3:
                if st.button("➖ Remover 1", key=f"sub_{index}"):
                    if st.session_state.estoque.at[index, 'Quantidade'] > 0:
                        st.session_state.estoque.at[index, 'Quantidade'] -= 1
                        st.rerun()
            with c4:
                if st.button("🗑️ Excluir", key=f"del_{index}"):
                    st.session_state.estoque = st.session_state.estoque.drop(index).reset_index(drop=True)
                    st.rerun()
else:
    st.info("Nenhum produto encontrado.")

# --- EXPORTAR ---
st.sidebar.divider()
if st.sidebar.button("📥 Baixar Planilha Excel"):
    csv = st.session_state.estoque.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button("Clique aqui para baixar", csv, "estoque_bella_vista.csv", "text/csv")
