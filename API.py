#Pericles Maikon de Jesus Costa
#COMP0455 - T01

from flask import Flask, request, jsonify, render_template_string
from flasgger import Swagger
import json
import os

#Criação do arquivo JSON
ARQUIVO_USUARIOS = 'usuarios.json'

app = Flask(__name__)   #Inicia a API
swagger = Swagger(app)  #Inicia o Swagger

#Função para carregar usuários do arquivo JSON
def carregar_usuarios():
    if os.path.exists(ARQUIVO_USUARIOS):
        with open(ARQUIVO_USUARIOS, 'r') as f:
            return json.load(f)
    return []

#Função para salvar usuários no arquivo JSON
def salvar_usuarios(usuarios):
    with open(ARQUIVO_USUARIOS, 'w') as f:
        json.dump(usuarios, f, indent=4)

#Carregar usuários ao iniciar
Usuarios = carregar_usuarios()

@app.route('/')
def home():
    return render_template_string('''
    <h1>API de Pericles</h1>
    <button onclick="window.location.href='/criar'">Criar Usuário</button><br><br>
    <button onclick="window.location.href='/usuario/'">Pesquisar Usuário</button><br><br>
    <button onclick="window.location.href='/usuarios'">Mostrar Todos os Usuários</button>
    ''')

@app.route('/usuarios', methods=['GET'])
def obter_usuarios():
    #Codigo para Swagger
    '''
    Obter todos os usuários.
    ---
    responses:
      200:
        description: Lista de usuários
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  cpf:
                    type: integer
                  nome:
                    type: string
                  data_nascimento:
                    type: string
    '''
    return jsonify(Usuarios)

@app.route('/usuario/')
def solicitar_cpf():
    return 'Insira o CPF no final da URL!'

@app.route('/usuario/<int:cpf>', methods=['GET'])
def obter_usuario(cpf):
    #Codigo para Swagger
    '''
    Obter um usuário pelo CPF.
    ---
    parameters:
      - name: cpf
        in: path
        type: integer
        required: true
        description: O CPF do usuário
    responses:
      200:
        description: Informações do usuário
        content:
          application/json:
            schema:
              type: object
              properties:
                cpf:
                  type: integer
                nome:
                  type: string
                data_nascimento:
                  type: string
      404:
        description: Usuário não encontrado
    '''
    #Procura o usuário no arquivo
    usuario = next((usuario for usuario in Usuarios if usuario.get('cpf') == cpf), None)
    if usuario:
        return jsonify(usuario)
    else:
        return jsonify({"erro": "Usuário não encontrado."}), 404

@app.route('/criar')
def criar():
    #Formulário de criação em HTML
    return render_template_string('''
        <h1>Criar Usuário</h1>
        <form action="/criar-usuario" method="POST">
            <label for="cpf">CPF:</label><br>
            <input type="text" id="cpf" name="cpf"><br><br>
        
            <label for="nome">Nome:</label><br>
            <input type="text" id="nome" name="nome"><br><br>
        
            <label for="data_nascimento">Data de Nascimento:</label><br>
            <input type="date" id="data_nascimento" name="data_nascimento"><br><br>
        
            <input type="submit" value="Criar Usuário">
        </form>
    ''')

@app.route('/criar-usuario', methods=['POST'])
def criar_usuario():
    #Codigo para Swagger
    '''
    Criar um novo usuário.
    ---
    consumes:
      - application/x-www-form-urlencoded
    parameters:
      - name: cpf
        in: formData
        type: integer
        required: true
        description: CPF do usuário
      - name: nome
        in: formData
        type: string
        required: true
        description: Nome do usuário
      - name: data_nascimento
        in: formData
        type: string
        format: date
        required: true
        description: Data de nascimento do usuário
    responses:
      201:
        description: Usuário criado com sucesso
        content:
          text/html:
            schema:
              type: string
              example: "<h1>Usuário Criado!</h1>"
      404:
        description: Usuário já existe
    '''
    #Coleta informações do formulário
    cpf = int(request.form.get('cpf'))
    nome = request.form.get('nome')
    data_nascimento = request.form.get('data_nascimento')

    #Verifica se o usuario já foi criado
    usuario_existente = next((usuario for usuario in Usuarios if usuario.get('cpf') == cpf), None)
    if usuario_existente:
        return render_template_string('''
        <h1>Erro: Usuário já existe!</h1>
        <button onclick="window.location.href='/'">Home</button>
        '''), 404
        
    usuario = {
        "cpf": cpf,
        "nome": nome,
        "data_nascimento": data_nascimento
    }
        
    Usuarios.append(usuario)
    salvar_usuarios(Usuarios)
        
    return render_template_string('''
    <h1>Usuário Criado!</h1>
    <button onclick="window.location.href='/'">Home</button>
    '''), 201

app.run(debug=True)