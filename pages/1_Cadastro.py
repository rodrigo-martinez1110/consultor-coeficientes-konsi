import streamlit as st
from supabase import create_client, Client
from datetime import date

# --- Conexão Supabase
url = st.secrets["supabase"]["url"]
key = st.secrets["supabase"]["key"]

supabase: Client = create_client(url, key)

# --- Listas fixas
convenios = sorted([
    'GOV AM', 'GOV AL', 'GOV BA', 'GOV CE', 'GOV ES', 'GOV GO', 'GOV SC', 'GOV MA',
    'GOV MS', 'GOV MT', 'GOV PE', 'GOV PI', 'GOV PR', 'GOV RJ', 'GOV RO', 'GOV SP',
    'PREF BELEM', 'PREF BH', 'PREF GOIANIA', 'PREF JP', 'PREF MARINGA', 'PREF RECIFE',
    'PREF RJ', 'PREF SP', 'PREF SSA', 'PREF CURITIBA'               
])

categorias_por_convenio = {
    "GOV SP": ["Geral", "SEFAZ", "PMESP", "SPPREV", "AOL", "CLT"],
    "PREF RJ": ["Geral", "EDUCACAO; GUARDA", "COMLURB"],
    "GOV AL": ["Geral", "Saque Complementar"],
}

produtos = ['Crédito Novo', 'Cartão Benefício', 'Cartão Consignado', 'Refinanciamento', 'Portabilidade']

bancos_mapeamento = {
    "2 - MeuCashCard": "2",
    "33 - Santander": "33",
    "74 - Banco do Brasil": "74",
    "243 - Banco Master": "243",
    "318 - BMG": "318",
    "335 - Banco Digio": "335",
    "389 - Banco Mercantil": "389",
    "422 - Banco Safra": "422",
    "465 - Capital Consig": "465",
    "604 - Banco Industrial": "604",
    "623 - Banco PAN": "623",
    "643 - Banco Pine": "643",
    "654 - Banco DigiMais": "654",
    "707- Banco Daycoval": "707",
    "955 - Banco Olé": "955",
    "6613 - VemCard": "6613"
}

# --- Título da página
st.title("📥 Cadastro de Coeficientes")

# --- Layout em colunas
col1, col2 = st.columns(2)

with col1:
    selected_convenio = st.selectbox("1. Convênio *", convenios)
    banco_label = st.selectbox("Banco", list(bancos_mapeamento.keys()))
    banco = bancos_mapeamento[banco_label]
    coeficiente = st.number_input("3. Coeficiente", format="%.4f")
    # NOVO BLOCO: Tipo de margem
    
    quant_parcela = st.number_input("4. Quantidade de Parcelas", step=1, min_value=1)
    data_consulta = st.date_input("6. Data da Consulta", value=date.today(), format="YYYY-MM-DD")

with col2:
    categoria_opcoes = categorias_por_convenio.get(selected_convenio, ["Geral"])
    selected_categoria = st.selectbox("7. Segmentação do Coeficiente", categoria_opcoes)
    selected_produto = st.selectbox("8. Produto", produtos)
    comissao = st.number_input("9. Comissão (%)", format="%.2f")
    coef_parcela = st.number_input("10. Coeficiente por Parcela", format="%.4f")
    taxa_juros = st.number_input("11. Taxa de Juros (%)", format="%.2f")
    
st.write("---")
tipo_margem = st.radio("5. Tipo de Margem de Segurança", ["Percentual (%)", "Valor fixo (R$)"], index=0)
if tipo_margem == "Percentual (%)":
    margem_valor = st.number_input("Margem Segurança (%)", format="%.2f", min_value=0.0)
    tipo_margem_salvar = "percentual"
else:
    margem_valor = st.number_input("Margem Segurança (R$)", format="%.2f", min_value=0.0)
    tipo_margem_salvar = "fixo"
st.write("---")

# --- Botão de envio
if st.button("✅ Salvar coeficiente"):
    erros = []
    if not selected_convenio:
        erros.append("Convênio é obrigatório.")
    if not banco:
        erros.append("Banco é obrigatório.")
    if coeficiente <= 0:
        erros.append("Coeficiente deve ser maior que 0.")
    if quant_parcela <= 0:
        erros.append("Quantidade de parcelas deve ser maior que 0.")
    if not selected_produto:
        erros.append("Produto é obrigatório.")

    if erros:
        for erro in erros:
            st.error(f"❌ {erro}")
    else:
        data = {
            "convenio": selected_convenio,
            "categoria_convenio": selected_categoria,
            "produto": selected_produto,
            "banco": banco,
            "coeficiente": coeficiente,
            "quant_parcela": quant_parcela,
            "coef_parcela": coef_parcela,
            "comissao": comissao,
            "taxa_juros": taxa_juros,
            "tipo_margem": tipo_margem_salvar,
            "margem_seguranca": margem_valor,
            "data_consulta": str(data_consulta)
        }

        try:
            supabase.table("db_coeficientes").insert(data).execute()
            st.success("✅ Registro inserido com sucesso!")
        except Exception as e:
            st.error(f"❌ Erro ao inserir no banco: {e}")
