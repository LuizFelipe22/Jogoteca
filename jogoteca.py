from flask import Flask, render_template, request, redirect, session, flash

class Jogo:
    def __init__(self, nome, estreia, desenvolvedores, telefone):
        self.nome = nome
        self.estreia = estreia
        self.desenvolvedores = desenvolvedores
        self.telefone = telefone

class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha

usuario1 = Usuario("Mateus", "Mat", "1010")
usuario2 = Usuario("Luiz Felipe", "Luiz", "2222")
usuario3 = Usuario("João Pedro", "JP", "1234")

usuarios = {usuario1.nickname: usuario1,
            usuario2.nickname: usuario2,
            usuario3.nickname: usuario3}

Jogo1 = Jogo("Clash Royale", "2016", "Supercell", "99999999999")
Jogo2 = Jogo("Need for Speed", "2014", "Electronic Arts, EA Gothenburg, etc", "55555555555")
Jogo3 = Jogo("Fifa", "2021", "EA Romania e EA Vancouver", "42193278462")
lista = [Jogo1, Jogo2, Jogo3]

app = Flask(__name__)
app.secret_key = 'Luiz'

@app.route("/")
def index():
    return render_template("lista.html", titulo="Jogos", jogos=lista)

@app.route("/novojogo")
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('login?proxima=novojogo')
    return render_template("novojogo.html", titulo="Adicione um novo jogo")

@app.route("/criar", methods=["POST",])
def criar():
    nome = request.form['nome']
    estreia = request.form['estreia']
    desenvolvedores = request.form['desenvolvedores']
    telefone = request.form['telefone']
    jogo = Jogo(nome, estreia, desenvolvedores, telefone)
    lista.append(jogo)
    return redirect('/')

@app.route("/login")
def login():
    proxima = request.args.get('proxima')
    return render_template("login.html", proxima=proxima)

@app.route("/autenticar", methods=['POST',])
def autenticar():
    if(request.form['usuario'] in usuarios):
        resposta = usuarios[request.form['usuario']]
        if(request.form['senha'] == resposta.senha):
            session['usuario_logado'] = request.form['usuario']
            flash(session['usuario_logado'] + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect('/{}'.format(proxima_pagina))
    else:
        flash('Usuário não localizado!')
        return redirect('/login')

@app.route("/logaut")
def logaut():
    session['usuario_logado'] = None
    flash("Usuário desconectado.")
    return redirect('/')

app.run(debug=True)