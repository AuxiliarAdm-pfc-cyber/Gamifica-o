# streamlit_app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------
# Passo 1: Objetivo do Estudo
# ----------------------
st.title("🔍 Pipeline de Gamificação Educacional - PFC")

st.markdown("""
## 🎯 Objetivo do Estudo
Este aplicativo apresenta de forma interativa o funcionamento do pipeline de gamificação do projeto **PFC - Provocando Futuros Cientistas**.

Ele visa atribuir pontuações aos alunos com base em presenças, participações e atividades, transformando o engajamento em **PFCoins** (moeda gamificada).
""")

# ----------------------
# Passo 2: Upload dos Dados
# ----------------------
st.sidebar.title("📥 Upload dos Arquivos")
matricula_file = st.sidebar.file_uploader("Lista de Matrículas (CSV)", type=["csv"])
presenca_file = st.sidebar.file_uploader("Lista de Presenças (CSV)", type=["csv"])
atividade_file = st.sidebar.file_uploader("Cadastro de Atividades (CSV)", type=["csv"])

if matricula_file and presenca_file and atividade_file:
    try:
        df_matricula = pd.read_csv(matricula_file)
        df_presenca = pd.read_csv(presenca_file)
        df_atividades = pd.read_csv(atividade_file)

        # ----------------------
        # Passo 3: Análise da Estrutura
        # ----------------------
        st.markdown("## 🧱 Estrutura Inicial dos Dados")
        st.subheader("Lista de Matrícula")
        st.dataframe(df_matricula.head())
        st.subheader("Lista de Presença")
        st.dataframe(df_presenca.head())
        st.subheader("Cadastro de Atividades")
        st.dataframe(df_atividades.head())

        # ----------------------
        # Passo 4: Limpeza e Normalização
        # ----------------------
        st.markdown("## 🧹 Limpeza e Normalização")

        def normalizar_nomes(nome):
            return nome.strip().lower().replace(" ", "")

        df_presenca["Nome"] = df_presenca["Nome"].astype(str).apply(normalizar_nomes)
        df_matricula["Nome"] = df_matricula["Nome"].astype(str).apply(normalizar_nomes)

        df = pd.merge(df_presenca, df_matricula, on="Nome", how="left")

        # ----------------------
        # Passo 5: AED - Visualizações
        # ----------------------
        st.markdown("## 📊 Análise Exploratória dos Dados")
        if "Presença" in df.columns:
            contagem = df["Presença"].value_counts()
            fig, ax = plt.subplots()
            ax.bar(contagem.index, contagem.values)
            ax.set_title("Distribuição de Presenças e Faltas")
            ax.set_ylabel("Quantidade")
            st.pyplot(fig)
        else:
            st.warning("Coluna 'Presença' não encontrada no arquivo de presença.")

        # ----------------------
        # Passo 6: Prompt/Gerador dos Dados
        # ----------------------
        st.markdown("## ⚙️ Prompt de Geração de Dados")
        st.code("""
Regras = {
    "Presencas": 100,
    "Faltas": -100,
    "Termo de Compromisso": 100,
    "Atividades Gerais": 30,
    "Clube de Ciências": 100,
    # ... outras regras ...
}
""", language='python')

        # ----------------------
        # Passo 7: Interpretação dos Resultados
        # ----------------------
        st.markdown("## 🧠 Interpretação dos Resultados")
        if "Presença" in df.columns:
            df["PFCoins"] = df["Presença"].map({"Presente": 100, "Falta": -100})
            ranking = df.groupby("Nome")["PFCoins"].sum().sort_values(ascending=False).reset_index()
            st.dataframe(ranking)
            st.success("🎉 O pipeline foi executado com sucesso e o ranking foi gerado!")
        else:
            st.error("A coluna 'Presença' não está disponível para gerar o ranking.")

    except Exception as e:
        st.error(f"Erro ao processar os arquivos: {e}")
else:
    st.warning("Por favor, envie os 3 arquivos para iniciar o processamento.")
