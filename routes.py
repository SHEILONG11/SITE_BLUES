from main import app
from flask import Flask,render_template, request, flash, redirect, url_for
from datetime import datetime
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv #UTILIZO O DOTENV PARA PUXAR OS DADOS/INFORMACOES DO ARQUIVO .ENV
import os

load_dotenv()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

#PROJETOS
@app.route('/dogpage')
def dogpage():
    return render_template('Projetos/templates/dogpage.html')
@app.route('/sobre')
def sobre():
    return render_template('/Projetos/templates/sobre.html')

#FORMULÁRIO

@app.route('/formulario')
def formulario():
    return render_template('projetos/templates/myform.html')

@app.route('/processar', methods=['POST'])
def processar():
    print("FORM DATA:", request.form)  # depuração
    # obtém dados do form
    nome = request.form.get('nome')
    email = request.form.get('email')
    telefone = request.form.get('telefone')
    sexo = request.form.get('sexo')
    idade = request.form.get('idade')
    # você já tem data_hora no formulário mas você gera você mesmo:
    data_hora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    if nome is None or nome == "" or idade is None or idade == "":
        flash('Nome e idade são obrigatórios!', 'error')
        return redirect(url_for('/formulario'))
    
    # conecta ao banco
    config = {
        'host': os.getenv('DB_HOST'),
        'port': int(os.getenv('DB_PORT')),
        'database': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD')
    }
    try:
        connection = mysql.connector.connect(**config)
        inserir_cliente(connection, nome, email, telefone, sexo, idade)
    except Error as e:
        print(f"❌Erro ao conectar/inserir: {e}")
        flash("Erro ao salvar os dados no banco", "danger")
        return redirect(url_for("/formulario"))
    finally:
        try:
            if connection and connection.is_connected():
                connection.close()
        except NameError:
            pass

    flash("Dados salvos com sucesso!", "success")
    return redirect(url_for("/visualizar"))


def inserir_cliente(connection,nome,email,telefone,sexo,idade): #AQUI ENTRA NOSSAS VARIAVEIS COMECANDO COM A CONEXAO
    try:
        cursor = connection.cursor()
        query = "INSERT INTO clientes (Nome, Email, Telefone, Sexo, Idade) VALUES (%s, %s, %s, %s, %s)" #A "%s" SERVE PARA CADA VALORES DAS VARIAVEIS QUE ESTOU CRIANDO NA TABELA clientes
        values = (nome, email, telefone, sexo, idade)
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        print(f"✅Cliente inserido com ID: {cursor.lastrowid}")
        return cursor.lastrowid
    except Error as e:
        print(f"❌Erro ao inserir cliente: {e}")
        return redirect(url_for("/formulario"))

    
    
#PRIMEIRO MODO DE MOSTRAR OS CLIENTES
@app.route('/visualizar')          
def visualizar():
    # Conecta ao banco
    config = {
        'host': os.getenv('DB_HOST'),
        'port': int(os.getenv('DB_PORT')),
        'database': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD')
    }
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        cursor.execute("SELECT nome, email, telefone, sexo, idade FROM clientes")
        dados = cursor.fetchall()  # pega todas as linhas
        # Se quiser os nomes das colunas também:
        colunas = [desc[0] for desc in cursor.description]
    except Error as e:
        print("Erro ao buscar os dados:", e)
        dados = []
        colunas = []
    finally:
        cursor.close()
        connection.close()

    # Passa os dados para o template
    return render_template('Projetos/templates/dados.html', dados=[colunas] + dados)


#CRUD DE MARIA
#READ
#SEGUNDO MODO DE MOSTRAR OS CLIENTES

'''@app.route('/imprimir')
def imprimir_clientes(connection):
    config = {
        'host': os.getenv('DB_HOST'),
        'port': int(os.getenv('DB_PORT')),
        'database': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD')
    }
    try:
        cursor = connection.cursor()
        query = 'SELECT * FROM clientes'
        cursor.execute(query)
        clientes = cursor.fetchall()

        if clientes:
            print("======MEUS CLIENTES======")
            for cliente in clientes:
                print("ID",cliente[0])
                print("Nome",cliente[1])
                print("Email",cliente[2])
                print("Telefone",cliente[3])
                print("Sexo",cliente[4])
                print("Idade",cliente[5])
                print("\n")

    except Error as e:
        print(f"Erro ao encontrar cliente: {e}")
        connection.rollback()
        return None'''
   
#UPDATE
@app.route('/editar')
def editar_cliente(connection, id, novo_nome=None, novo_email=None, novo_telefone=None, novo_sexo=None, novo_idade=None):
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM clientes WHERE id_cliente = %s"
        cursor.execute(query, (id,))
        cliente = cursor.fetchone()
        print(cliente)

        variaveis = []
        valores = []

        if novo_nome is not None: # SE EU TIVER INSERIDO UM NOME
            variaveis.append('nome = %s')
            valores.append(novo_nome)
        if novo_email is not None:
            variaveis.append('email = %s')
            valores.append(novo_email)
        if novo_telefone is not None:
            variaveis.append('telefone = %s')
            valores.append(novo_telefone)
        if novo_sexo is not None:
            variaveis.append('sexo = %s')
            valores.append(novo_sexo)
        if novo_idade is not None:
            variaveis.append('idade = %s')
            valores.append(novo_idade)

        valores.append(id)
        query = f"UPDATE clientes SET {', '.join(variaveis)} WHERE id_cliente = %s"
        cursor.execute(query, valores)
        connection.commit()

    except Error as e:
        print(f"Erro ao encontrar cliente {e}")
        connection.rollback()
        return None

#DELETE
@app.route("/deletar")
def deletar_cliente(connection, id):
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM cliente WHERE id_cliente = %s"
        cursor.execute(query)
        cliente = cursor.fetchone()
    
    except Error as e:
        print(f"Erro ao encontrar cliente: {e}")
        connection.rollback()
        return None
    
    
#REPOSITORIOS
@app.route('/modulo01')
def modulo01():
    return render_template('Modulo01.html')
@app.route('/aulas')
def aulas():
    return render_template('/Projetos/templates/aulas.html')
@app.route('/desafios')
def desafio():
    return render_template('/Projetos/templates/desafios.html')
#AULAS DOS REPOSITORIOS
@app.route('/aula02')
def aula02():
    return render_template('/aulas/aula02.html')
@app.route('/aula07')
def aula07():
    return render_template('/aulas/aula07.html')
@app.route('/aula08')
def aula08():
    return render_template('/aulas/aula08.html')
@app.route('/aula08-B')
def aula08b():
    return render_template('/aulas/aula08-B.html')
@app.route('/aula09')
def aula09():
    return render_template('/aulas/aula09.html')
@app.route('/aula10')
def aula10():
    return render_template('/aulas/aula10.html')
@app.route('/aula11')
def aula11():
    return render_template('/aulas/aula11.html')
@app.route('/aula12')
def aula12():
    return render_template('/aulas/aula12.html')

#DESAFIOS DOS REPOSITORIOS
@app.route('/ex04')
def ex04():
    return render_template('/desafios/ex04.html')
@app.route('/ex07')
def ex07():
    return render_template('/desafios/ex07.html')
@app.route('/ex09')
def ex09():
    return render_template('/desafios/ex09.html')
@app.route('/ex09/pagina01')
def ex09pagina01():
    return render_template('/desafios/pagina01.html')
@app.route('/ex09/pagina02')
def ex09pagina02():
    return render_template('/desafios/pagina02.html')
@app.route('/ex09/pagina03')
def ex09pagina03():
    return render_template('/desafios/pagina03.html')
@app.route('/ex09/pagina04')
def ex09pagina04():
    return render_template('/desafios/pagina04.html')
