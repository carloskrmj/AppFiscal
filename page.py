import sys

import streamlit as st
from app_1 import gerar_resposta
import pandas as pd
from streamlit.web.cli import main

df = pd.read_csv('Contas_Sinteticas.csv',  encoding='ISO-8859-1', sep=";")
st.set_page_config(page_title="Meu Especialista Contábil - ChatGPT", layout='wide', initial_sidebar_state='expanded')


def chargeDB():
    df = pd.read_csv('Contas_Sinteticas.csv', encoding="ISO-8859-1", sep=";")
    return df


with st.container():
    st.sidebar.header('Meu Especialista Contábil')

    # Lista de contas sintéticas da tabela

    nomeConta = df['Nome da conta']
    conta = st.sidebar.selectbox("Selecione uma conta sintética ou insira uma abaixo:", nomeConta)
    # inserir uma conta contábil
    sentence = st.sidebar.text_input(f'Insira Conta:', placeholder='Ex: Ativo')
    st.sidebar.write("---")

    st.sidebar.write("Selecione uma ou mais opções")
    op1 = st.sidebar.checkbox('Tradução para o inglês')
    op2 = st.sidebar.checkbox('Característica e aplicação da conta')
    op3 = st.sidebar.checkbox('Norma contábil e orientações para as operações no grupo da conta')

    solicitacao = []
    if op1:
        solicitacao.append("Tradução para o inglês")
    if op2:
        solicitacao.append("Característica e aplicação da conta")
    if op3:
        solicitacao.append("Norma contábil e orientações para as operações no grupo da conta")


    st.sidebar.write("---")


def callChat(solicitacao, sentence):
    if sentence == '':
        return "Não há dados suficientes para uma resposta satisfatória!"

    resposta = {}
    for question in solicitacao:
        if question == 'Tradução para o inglês':
            pergunta = (f'Traduza para o inglês "{sentence}", '
                        f'limite sua resposta apenas para a tradução da palavra')

        elif question == 'Característica e aplicação da conta':
            pergunta = (f'Seja um especialista contábil e descreva as '
                        f'características e aplicações da conta contábil  {sentence}, '
                        f'limite sua resposta a 500 caracteres')

        elif question == 'Norma contábil e orientações para as operações no grupo da conta':
            pergunta = (f'Seja um especialista contábil e oriente as operações no grupo da conta contábil {sentence}, '
                        f'limite sua resposta a 500 caracteres')
        else:
            pergunta = ''

        resposta[question] = gerar_resposta(pergunta)[0]

    if len(resposta) == 0:
        return "Não há dados suficientes para uma resposta satisfatória!"
    else:
        return resposta


with st.container():
    #executa a função de busca no chatgpt
    button = st.sidebar.button("Run", type="primary")
    resposta = ""
    if button:
        if sentence == "":
            sentence = conta
        resposta = callChat(solicitacao, sentence)


col1, col2 = st.columns([3, 1], gap="large")

st.write("---")

with st.container():
    with col1:
        if button:
            if 'Tradução para o inglês' in resposta:
                st.text_area("Tradução da conta:",
                             resposta['Tradução para o inglês'],
                             height=5, disabled=False)
            if 'Característica e aplicação da conta' in resposta:
                st.text_area("Característica e aplicação da conta:",
                             resposta['Característica e aplicação da conta'],
                             height=150, disabled=False)
            if 'Norma contábil e orientações para as operações no grupo da conta' in resposta:
                st.text_area("Normas e orientações para as operações no grupo da conta:",
                             resposta['Norma contábil e orientações para as operações no grupo da conta'],
                             height=150, disabled=False)
        else:
            st.text_area("Tradução da conta:",
                         "",
                         height=5, disabled=False)
            st.text_area("Característica e aplicação da conta:",
                         "",
                         height=150, disabled=False)
            st.text_area("Normas e orientações para as operações no grupo da conta:",
                         "",
                         height=150, disabled=False)

    with col2:
        st.write("---")
        buttonPlanContas = st.link_button("Criar um Plano de Contas", "http://localhost:8501/#criar-um-plano-de-contas")
        buttonBookPlanContas = st.link_button("Criar um Book do Plano de Contas", "http://localhost:8501/#criar-um-book-do-plano-de-contas")


if __name__ == '__main__':
    import re
    sys.argv = ['streamlit', 'run', 'page.py']
    try:
        sys.exit(main())
    except:
        pass


