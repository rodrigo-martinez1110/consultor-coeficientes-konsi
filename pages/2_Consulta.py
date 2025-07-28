import streamlit as st
import pandas as pd
from supabase import create_client, Client
pd.options.mode.chained_assignment = None  # Desativa o SettingWithCopyWarning

# --- Configuração da página
st.set_page_config(page_title="Consulta de Coeficientes", layout="wide")
st.title("📊 Consulta de Coeficientes")

# --- Conexão Supabase
url = st.secrets["supabase"]["url"]
key = st.secrets["supabase"]["key"]

supabase: Client = create_client(url, key)

# --- Mapeamento de bancos
bancos_mapeamento = {
    "MeuCashCard": "2", "Santander": "33", "Banco do Brasil": "74", "Banco Master": "243",
    "BMG": "318", "Banco Digio": "335", "Banco Mercantil": "389", "Banco Safra": "422",
    "Capital Consig": "465", "Banco Industrial": "604", "Banco PAN": "623", "Banco Pine": "643",
    "Banco DigiMais": "654", "Banco Daycoval": "707", "Banco Olé": "955", "VemCard": "6613"
}

# Mapeamento reverso: código -> nome
codigo_para_nome = {v: k for k, v in bancos_mapeamento.items()}

try:
    # --- Consulta dados do Supabase
    res = supabase.table("db_coeficientes").select("*").order("data_consulta", desc=True).execute()
    data = res.data

    if data:
        df = pd.DataFrame(data)
        df['data_consulta'] = pd.to_datetime(df['data_consulta']).dt.date

        st.sidebar.markdown("### 🔍 Filtros Dinâmicos")

        # Filtro 1: Convênio (obrigatório)
        convenios_disponiveis = sorted(df['convenio'].dropna().unique())
        selected_convenio = st.sidebar.selectbox("Convênio", convenios_disponiveis)

        df_filtrado = df[df['convenio'] == selected_convenio]

        # Filtro 2: Categoria do Convênio
        categorias_disponiveis = sorted(df_filtrado['categoria_convenio'].dropna().unique())
        selected_categoria = st.sidebar.selectbox("Categoria do Convênio", ["Todos"] + categorias_disponiveis)
        if selected_categoria != "Todos":
            df_filtrado = df_filtrado[df_filtrado['categoria_convenio'] == selected_categoria]

        # Filtro 3: Produto
        produtos_disponiveis = sorted(df_filtrado['produto'].dropna().unique())
        selected_produto = st.sidebar.selectbox("Produto", ["Todos"] + produtos_disponiveis)
        if selected_produto != "Todos":
            df_filtrado = df_filtrado[df_filtrado['produto'] == selected_produto]

        # Filtro 4: Banco (exibe nome, filtra por código)
        bancos_codigos_disponiveis = sorted(df_filtrado['banco'].dropna().unique())
        bancos_rotulos = {
            f"{codigo} - {codigo_para_nome.get(codigo, 'Desconhecido')}": codigo
            for codigo in bancos_codigos_disponiveis
        }
        selected_banco_label = st.sidebar.selectbox("Banco", ["Todos"] + list(bancos_rotulos.keys()))
        if selected_banco_label != "Todos":
            selected_banco_codigo = bancos_rotulos[selected_banco_label]
            df_filtrado = df_filtrado[df_filtrado['banco'] == selected_banco_codigo]

        # Ordenar do mais recente para o mais antigo
        df_filtrado = df_filtrado.sort_values(by="data_consulta", ascending=False)

        # --- Colunas para exibir
        colunas_exibir = [
            'data_consulta', 'convenio', 'categoria_convenio', 'produto',
            'coeficiente', 'coef_parcela', 'quant_parcela',
            'comissao', 'taxa_juros', 'banco'
        ]

        if 'margem_valor' in df_filtrado.columns and 'tipo_margem' in df_filtrado.columns:
            df_filtrado['margem_exibida'] = df_filtrado.apply(
                lambda row: f"{row['margem_valor']}%" if row['tipo_margem'] == 'percentual'
                else f"R$ {row['margem_valor']:.2f}", axis=1
            )
            colunas_exibir.append('margem_exibida')
        elif 'margem_seguranca' in df_filtrado.columns:
            colunas_exibir.append('margem_seguranca')

        df_exibir = df_filtrado[colunas_exibir]

        # --- Formatação
        for col in ['coeficiente', 'coef_parcela', 'comissao', 'taxa_juros']:
            if col in df_exibir.columns:
                df_exibir[col] = df_exibir[col].astype(float).round(2)

        # Substitui código do banco pelo nome
        if 'banco' in df_exibir.columns:
            df_exibir['banco'] = df_exibir['banco'].map(codigo_para_nome).fillna(df_exibir['banco'])

        # --- Exibição
        st.subheader(f"📋 Registros para: {selected_convenio}")
        st.dataframe(df_exibir, use_container_width=True)

    else:
        st.info("Nenhum dado encontrado.")

except Exception as e:
    st.error(f"❌ Erro ao consultar dados: {e}")
