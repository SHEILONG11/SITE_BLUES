from flask import Flask,render_template, request, flash, redirect, url_for
from datetime import datetime
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv #UTILIZO O DOTENV PARA PUXAR OS DADOS/INFORMACOES DO ARQUIVO .ENV
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = '1234'

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
    return render_template('myform.html')

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
        return redirect(url_for("formulario"))
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
        query = "INSERT INTO clientes (nome, email, telefone, sexo, idade) VALUES (%s, %s, %s, %s, %s)" #A %s SERVE PARA CADA VALORES DAS VARIAVEIS QUE ESTOU CRIANDO NA TABELA clientes
        values = (nome, email, telefone, sexo, idade)
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        print(f"✅Cliente inserido com ID: {cursor.lastrowid}")
        return cursor.lastrowid
    except Error as e:
        print(f"❌Erro ao inserir cliente: {e}")
        return redirect(url_for("/formulario"))

    
    
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
    return render_template('dados.html', dados=[colunas] + dados)
    
@app.route('/editar')
def editar():
    return render_template("editar.html")
    

#REPOSITORIOS
@app.route('/modulo01')
def modulo01():
    return render_template('Modulo01.html')
@app.route('/aulas')
def aulas():
    return render_template('aulas.html')
@app.route('/desafios')
def desafio():
    return render_template('desafios.html')
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


if __name__ == '__main__':
    app.run(debug='True')