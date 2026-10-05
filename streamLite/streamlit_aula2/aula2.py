import streamlit as st
import pandas as pd

st.title("🚌 Expresso Mobilidade")
st.subheader("Painel do Operador")

# Identificação do operador
nome = st.text_input("Digite seu nome:")
if nome:
    st.write(f"Bem-vindo(a), **{nome}**! Bom turno de trabalho.")

st.divider()

# Consulta de rota específica
linha = st.selectbox(
    "Selecione a linha prioritária:",
    ["510 - Terminal Central", "520 - Bairro Norte", "550 - Zona Sul", "620 - Aeroporto"]
)
st.write("📍 Linha selecionada:", linha)

horarios = {
    "510 - Terminal Central": ["06:00", "07:30", "09:00", "11:00", "13:00"],
    "520 - Bairro Norte":     ["06:15", "07:45", "09:15", "11:15", "13:15"],
    "550 - Zona Sul":         ["06:30", "08:00", "09:30", "11:30", "13:30"],
    "620 - Aeroporto":        ["05:00", "07:00", "10:00", "14:00", "18:00"],
}
st.dataframe(pd.DataFrame({"Horários": horarios[linha]}), use_container_width=True)

st.divider()

# Seleção de múltiplas linhas
linhas = st.multiselect(
    "Selecione as linhas para relatório consolidado:",
    ["510 - Terminal Central", "520 - Bairro Norte", "550 - Zona Sul", "620 - Aeroporto"]
)

dados = {
    "510 - Terminal Central": {"Passageiros/dia": 1200, "Ônibus": 4},
    "520 - Bairro Norte":     {"Passageiros/dia": 850,  "Ônibus": 3},
    "550 - Zona Sul":         {"Passageiros/dia": 970,  "Ônibus": 3},
    "620 - Aeroporto":        {"Passageiros/dia": 600,  "Ônibus": 2},
}

if linhas:
    df_rel = pd.DataFrame([{"Linha": l, **dados[l]} for l in linhas])
    st.dataframe(df_rel, use_container_width=True)

st.divider()

# Disparo de cálculo de frota
if st.button("🚍 Calcular Demanda e Distribuição de Frota"):
    if not linhas:
        st.warning("Selecione ao menos uma linha para calcular.")
    else:
        st.success("Cálculo concluído!")
        col1, col2, col3 = st.columns(3)
        total_pass   = sum(dados[l]["Passageiros/dia"] for l in linhas)
        total_onibus = sum(dados[l]["Ônibus"] for l in linhas)
        col1.metric("Linhas Selecionadas", len(linhas))
        col2.metric("Total Passageiros/dia", total_pass)
        col3.metric("Ônibus Necessários", total_onibus)
        st.bar_chart(pd.DataFrame(
            {"Passageiros/dia": {l: dados[l]["Passageiros/dia"] for l in linhas}}
        ))
