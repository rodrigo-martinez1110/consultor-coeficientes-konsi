import streamlit as st

st.set_page_config(page_title="Consultor de Coeficientes", page_icon="📊")

st.title("📘 Bem-vindo ao Consultor de Coeficientes")
st.markdown("---")

st.markdown("""
Este aplicativo foi desenvolvido para facilitar o **cadastro** e a **consulta de coeficientes financeiros** utilizados por correspondentes bancários e analistas de crédito.

### 🔧 Funcionalidades principais

#### 1. 📥 Cadastrar Coeficientes
- Permite inserir novos coeficientes no banco de dados Supabase.
- Campos obrigatórios: convênio, banco, coeficiente, parcelas e produto.
- Possui suporte a diferentes **categorias/lotações** específicas por convênio.
- A data da consulta pode ser preenchida manualmente ou será assumida como a data de hoje automaticamente.

#### 2. 📊 Consultar Coeficientes
- Permite visualizar os dados já cadastrados.
- Os dados são exibidos do **mais recente para o mais antigo**, com base na data da consulta.
- É possível filtrar os dados por **convênio**, **categoria** e **produto**, usando os filtros no menu lateral.

### 🧱 Estrutura Técnica
- Desenvolvido em **Streamlit** com backend no **Supabase**.
- Armazena dados como: convênio, banco, coeficiente, parcelas, comissão, taxas e data de consulta.
""")

st.info("Use o menu lateral para navegar entre as páginas de Cadastro e Consulta.")
st.markdown("---")
st.caption("Desenvolvido com 💙 por sua equipe.")
