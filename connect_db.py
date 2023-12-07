from sqlalchemy import create_engine
from sqlalchemy import insert
from urllib.parse import quote_plus
import pandas as pd
from config import *
import psycopg2


def planoContas():
    engine = create_engine(f'postgresql://{usename}:%s@{host}:5432/{database}' % quote_plus(password))
    try:
        df = pd.read_sql_query('select * from "plano_de_contas"', con=engine)
        return df
    except Exception as e:
        return str(e)


#planoContas()

def serarchAccount(account):
    engine = create_engine(f'postgresql://{usename}:%s@{host}:5432/{database}' % quote_plus(password))
    try:
        df = pd.read_sql_query(f'select * from "plano_de_contas" where "Nome_conta" = ' + "'" + account + "'", con=engine)

        return df
    except Exception as e:
        return str(e)


#serarchAccount('Ativo Circulante')


def validaUser(user, pswd):
    import hashlib
    engine = create_engine(f'postgresql://{usename}:%s@{host}:5432/{database}' % quote_plus(password))
    def hash_password(password):
        password_bytes = password.encode('utf-8')
        hash_object = hashlib.sha256(password_bytes)
        return hash_object.hexdigest()

    pswd = hash_password(pswd)
    try:
        df = pd.read_sql_query(f'select * from "plano_de_contas_lg"',
                               con=engine)
        if '@' in user:
            df = df.loc[(df['email'] == user) & (df['pswd'] == pswd)]
        else:
            df = df.loc[(df['username'] == user) & (df['pswd'] == pswd)]

        return df
    except Exception as e:
        return str(e)

#df = validaUser('user', 'pswd')


def insertUser(user, email, pswd):
    import hashlib

    def hash_password(password):
        password_bytes = password.encode('utf-8')
        hash_object = hashlib.sha256(password_bytes)
        return hash_object.hexdigest()

    hashed_password = hash_password(pswd)

    engine = create_engine(f'postgresql://{usename}:%s@{host}:5432/{database}' % quote_plus(password))
    data = [(user, email, hashed_password)]
    colunas = ['username', 'email', 'pswd']
    df = pd.DataFrame(data=data, columns=colunas)

    try:
        df.to_sql('plano_de_contas_lg', engine, index=False, if_exists='append')
        return True
    except Exception as e:
        return str(e)

#insertUser('user', 'email', 'pswd')


def insertNorma(coluna, norma, onde):
    try:
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=usename,
            password=password,
            port=port
        )
        cursor = conn.cursor()
        query = "UPDATE plano_de_contas SET " + '"%s"' % (coluna) + "= '%s' WHERE " % (norma) + '"Nome_conta"' + " = '%s';" % (onde)

        print(query)
        cursor.execute(query)

        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(e)
