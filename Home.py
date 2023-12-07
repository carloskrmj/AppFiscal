import sys
import streamlit as st
from app_1 import gerar_resposta
import pandas as pd
from streamlit.web.cli import main
from connect_db import planoContas, serarchAccount, insertNorma
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

st.set_page_config(page_title="Meu Especialista Contábil - ChatGPT", layout='wide', initial_sidebar_state='expanded')
st.markdown('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)


# # # # # # # # # # # #  PÁGINA 1  # # # # # # # # # # # #
def intro():
    df = planoContas()

    def chargeDB():
        df = planoContas()
        return df


    with st.container():
        st.sidebar.header('Meu Especialista Contábil')

        # Lista de contas sintéticas da tabela

        nomeConta = df['Nome_conta']
        conta = st.sidebar.selectbox("Selecione uma conta ou insira uma abaixo:", nomeConta, index=None)
        # inserir uma conta contábil
        sentence = st.sidebar.text_input(f'Insira uma conta:', placeholder='Ex: Ativo')
        codConta = st.sidebar.text_input('Insira o código da conta:', placeholder='Ex: 1.1.01.01')
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

        pergunta = ''

        # procura informações na base de dados, se não houver informação, pergunta para o chatgpt
        dfVer = serarchAccount(sentence)
        bdTraduz = dfVer.iloc[0]['Name_account']
        bdCaract = dfVer.iloc[0]['Natureza_conta']
        bdNormaC = dfVer.iloc[0]['Norma_contabil']

        for question in solicitacao:
            if question == 'Tradução para o inglês' and bdTraduz == '':
                pergunta = (f'Traduza para o inglês "{sentence}", '
                            f'limite sua resposta apenas para a tradução da palavra')
                resposta['Tradução para o inglês'] = gerar_resposta(pergunta)[0]

                # insere informação no banco
                insertNorma('Name_account', resposta['Tradução para o inglês'], sentence)
            else:
                resposta['Tradução para o inglês'] = bdTraduz

            if question == 'Característica e aplicação da conta' and bdCaract == '':
                pergunta = (f'Seja um especialista contábil e descreva as '
                            f'características e aplicações da conta contábil  {sentence}, '
                            f'limite sua resposta a 500 caracteres')
                resposta['Característica e aplicação da conta'] = gerar_resposta(pergunta)[0]

                # insere informação no banco
                insertNorma('Natureza_conta', resposta['Característica e aplicação da conta'], sentence)
            else:
                resposta['Característica e aplicação da conta'] = bdCaract

            if question == 'Norma contábil e orientações para as operações no grupo da conta' and bdNormaC == '':
                pergunta = (f'Seja um especialista contábil e oriente as operações no grupo da conta contábil {sentence}, '
                            f'limite sua resposta a 500 caracteres')
                resposta['Norma contábil e orientações para as operações no grupo da conta'] = gerar_resposta(pergunta)[0]

                # insere informação no banco
                insertNorma('Norma_contabil',
                            resposta['Norma contábil e orientações para as operações no grupo da conta'],
                            sentence)
            else:
                resposta['Norma contábil e orientações para as operações no grupo da conta'] = bdNormaC



        if len(resposta) == 0:
            return "Não há dados suficientes para uma resposta satisfatória!"
        else:
            df = planoContas()
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
                if 'Tradução para o inglês' in resposta and op1:
                    st.text_area("Tradução da conta:",
                                 resposta['Tradução para o inglês'],
                                 height=5, disabled=False)
                if 'Característica e aplicação da conta' in resposta and op2:
                    st.text_area("Característica e aplicação da conta:",
                                 resposta['Característica e aplicação da conta'],
                                 height=150, disabled=False)
                if 'Norma contábil e orientações para as operações no grupo da conta' in resposta and op3:
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


# # # # # # # # # # # #  PÁGINA 2  # # # # # # # # # # # #
def pcontas():
    df = planoContas()

    @st.cache_data
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')

    with st.container():
        # filtro = st.multiselect('Filtrar produto', prod, placeholder='Nenhum produto selecionado')
        # if filtro:
        #    df = df.loc[df['PRODUTO'].isin(filtro)]
        df['Select'] = False

        df = df[['Codigo_conta', 'Nome_conta', "Name_account", "Select", "Natureza_conta", "Norma_contabil"]]

        df2 = st.data_editor(
            df,
            num_rows="dynamic",
            hide_index=True,
            disabled=["Codigo_conta", "Nome_conta", "Name_account", "Natureza_conta", "Norma_contabil"],
            column_config={"COD": st.column_config.Column(
                "COD",
                width="small",
            ),
                "Name_account": st.column_config.Column(
                    "Name_account",
                    width="large",
                ),
                "Nome_conta": st.column_config.Column(
                    "Nome_conta",
                    width="medium",
                ),
                "Select": st.column_config.Column(
                    "Select",
                    width="medium",
                ),
            }
        )

        # salva lista de contas selecionadas
        gerar = st.button('Gerar relatório')
        if gerar:
            dfs = df2.loc[df2['Select'] == True]
            del dfs['Select']
            dfs.reset_index(inplace=True, drop=True)
            st.write(dfs)
            csv = convert_df(dfs)

            st.download_button(
                label="Salvar Plano de contas",
                data=csv,
                file_name='Plano_de_Contas.csv',
                mime='text/csv',
            )
        # if salvar:
        #    dfs = df2.loc[df2['Select'] == True]
        #    del dfs['Select']
        #    dfs.reset_index(inplace=True, drop=True)
        #    st.write(dfs)


st.header('Meu Especialista Contábil')

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

authenticator.login('Login', 'main')

if st.session_state["authentication_status"]:
    page_names_to_funcs = {
        "Home": intro,
        "Plano de Contas": pcontas,
    }
    demo_name = st.sidebar.selectbox("Choose a demo", page_names_to_funcs.keys())
    page_names_to_funcs[demo_name]()

    with st.sidebar:
        authenticator.logout('Logout', 'main', key='unique_key')
        st.write(f'Welcome *{st.session_state["name"]}*')

elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.write('')


#if __name__ == '__main__':
#    import re
#    sys.argv = ['streamlit', 'run', 'Home.py']
#    try:
#        sys.exit(main())
#    except:
#        pass


# alterar tela plano de contas para tela relatório tela de relatório
# salvar relatório com seleção da tabela
# tela home incluir campo com código da conta, salvar resultado no banco
# supabase sbp_359b6f41585f8fa68008d4ec1e94bec16181fb04