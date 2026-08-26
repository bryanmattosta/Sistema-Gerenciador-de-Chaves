from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine, Column, Integer, String, Numeric, Date
from sqlalchemy.orm import declarative_base, sessionmaker
from flask_sqlalchemy import SQLAlchemy
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
from tabelas import engine, Base, Chave, Usuario, Perfil, Ambiente, Movimentacao
from random import randint
from datetime import datetime
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect
from email.message import EmailMessage
import os
from werkzeug.utils import secure_filename
from flask import send_file
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import random
import smtplib
import time


#cria a sesao
Session = sessionmaker(bind=engine)
sessao  = Session()

#criar o app
app = Flask(__name__)
app.secret_key="63f4945d921d599f27ae4fdf5bada3f1"
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
csrf = CSRFProtect(app)

#variaveis do email (gmail)
EMAIL = "senacdf.operadormicro@gmail.com"
SENHA_EMAIL = "uetz ezsn jjuy klyo"

#enviar email de nova senha
def enviar_email(destinatario, nova_senha):
    mensagem = EmailMessage()
    mensagem["Subject"] = "Nova senha - Sistema"
    mensagem["From"] = EMAIL
    mensagem["To"] = destinatario
    mensagem.set_content(f"""Olá! Sua nova senha de acesso ao sistema é:
                        {nova_senha} 
                        Utilize essa senha para acessar o sistema. 
                        Atenciosamente, Sistema""")
    servidor = smtplib.SMTP("smtp.gmail.com", 587)
    servidor.starttls()
    servidor.login(EMAIL,SENHA_EMAIL)
    servidor.send_message(mensagem)
    servidor.quit()


def enviar_email_reserva(destinatario, codigo_reserva):
    mensagem = EmailMessage()
    mensagem["Subject"] = "Confirmação de Reserva - Sistema de Chaves"
    mensagem["From"] = EMAIL
    mensagem["To"] = destinatario
    mensagem.set_content(f"""Olá! Sua reserva foi realizada com sucesso.
    
Seu código de reserva é: {codigo_reserva}
Guarde este código para retirar a chave.

Atenciosamente, 
Sistema de Gerenciamento de Chaves""")
    
    servidor = smtplib.SMTP("smtp.gmail.com", 587)
    servidor.starttls()
    servidor.login(EMAIL, SENHA_EMAIL)
    servidor.send_message(mensagem)
    servidor.quit()

app = Flask(__name__)
app.secret_key="jPsAzLWzvd9pwQWric93xduG6wFrDpXb"
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
# csrf = CSRFProtect(app)


#Decorador para proteger a pagina
#proteger as paginas basta colocar @login_obrigatorio
def login_obrigatorio(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "email" not in session:
            flash("Faça o login primeiro para acessar o sistema!", "warning") # <--- Alerta amigável
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

def administrador_obrigatorio(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "email" not in session:
            flash("Faça login para continuar.", "warning")
            return redirect(url_for("login"))
        
        if session.get("nivel") != "Administrador":
            flash("Você não tem permissão para acessar esta página.", "danger")
            return redirect(url_for("reserva"))
       
        return func(*args, **kwargs)
    return wrapper

def professor_obrigatorio(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "email" not in session:
            flash("Faça login para continuar.", "warning")
            return redirect(url_for("login"))
        
        if session.get("nivel") != "Professor":
            flash("Você não tem permissão para acessar esta página.", "danger")
            return redirect(url_for("reserva"))
       
        return func(*args, **kwargs)
    return wrapper

def atendente_obrigatorio(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "email" not in session:
            flash("Faça login para continuar.", "warning")
            return redirect(url_for("login"))
        
        if session.get("nivel") != "Atendente":
            flash("Você não tem permissão para acessar esta página.", "danger")
            return redirect(url_for("reserva"))
       
        return func(*args, **kwargs)
    return wrapper

@app.context_processor
def injetar_usuario():
    return {
        "usuario_logado": session.get("perfil", "Visitante"),
        "cargo_logado": session.get("nivel", "Convidado")
    }

#home
@app.route("/")
@login_obrigatorio
def home(): 
    # --- VERIFICAÇÃO DE SEGURANÇA DA FOTO NA SESSÃO ---
    foto_atual = session.get("foto_usuario")
    if foto_atual and foto_atual != "icon_user.png":
        caminho_fisico = os.path.join('static', 'img', foto_atual)
        if not os.path.exists(caminho_fisico):
            session["foto_usuario"] = "icon_user.png"
    # --------------------------------------------------

    total_ambientes = sessao.query(Ambiente).count()
    total_reservas = sessao.query(Movimentacao).filter(Movimentacao.id_movimentacao).count()
    total_devolucoes = sessao.query(Movimentacao).filter(Movimentacao.status == "Retirado").count()
    total_usuarios = sessao.query(Usuario).count()

    return render_template(
        "index.html", total_ambientes=total_ambientes,
        total_reservas=total_reservas,
        total_devolucoes=total_devolucoes,
        total_usuarios=total_usuarios
    )
    

#chave 
@app.route("/chave", methods=["GET", "POST"])
@login_obrigatorio
@administrador_obrigatorio
def chave():
    # Lista de todos os ambientes para preencher o <select>
    todos_ambiente = sessao.query(Ambiente).all()

    if request.method == "POST":
        # Pegando os dados EXATOS que vêm do HTML e que existem no banco
        nome_chave = request.form.get("nome_chave")
        id_ambiente = request.form.get("id_ambiente")
        observacao_chave = request.form.get("observacao_chave")
        
        # Validação do nome
        if not nome_chave or nome_chave.strip() == "":
            flash("Nome da Chave é obrigatório!", "danger")
            # Tem que passar os ambientes aqui também, senão a tela quebra!
            return render_template("chave.html", ambientes=todos_ambiente)

        # Inserir chave (já definindo status=1 para nascer Ativa)
        c = Chave(
            nome_chave=nome_chave, 
            id_ambiente=id_ambiente, 
            observacao_chave=observacao_chave, 
            status=1
        )
        
        sessao.add(c)
        sessao.commit()
        flash("Chave salva com sucesso!", "success")

        # Redireciona para a página inicial após o envio do formulário
        return redirect(url_for("chave"))
        
    return render_template('chave.html', ambientes=todos_ambiente)

#chave consultar
@app.route("/chave/consultar", methods=["GET", "POST"])
@login_obrigatorio
@administrador_obrigatorio
def consultar_chave():
    #Pegar a chave foi informada
    chave_nome = request.args.get("nome_chave","")
    todos_ambientes = sessao.query(Ambiente).all()
    #consultar chave
    chaves = sessao.query(Chave).filter(Chave.nome_chave.like(f"%{chave_nome}%")).all()
    #chamar cahve.html para mostrar dados
    return render_template('chave.html', chaves=chaves, ambientes=todos_ambientes)

#alterar chave
@app.route("/chave/alterar", methods=["POST"])
@login_obrigatorio
@administrador_obrigatorio
def alterar_chave():
    
    # 1. Pega o ID que veio escondido no formulário da modal
    id_chave = request.form.get("id_chave")
    
    # 2. Busca a chave no banco
    chave = sessao.query(Chave).get(id_chave)
    
    # 3. Valida se a chave existe
    if chave is None:
        flash("Chave não encontrada.", "danger")
        return redirect(url_for("chave"))
        
    # 4. Pega os dados EXATOS usando os nomes da sua tabela MySQL
    nome_chave = request.form.get("nome_chave")
    id_ambiente = request.form.get("id_ambiente")
    observacao_chave = request.form.get("observacao_chave")
    status = request.form.get("status")
    
    # 5. Validação de segurança simples
    if not nome_chave or nome_chave.strip() == "":
        flash("Nome da Chave é obrigatório!", "danger")
        return redirect(url_for("chave"))
        
    # 6. Atualiza o objeto com os dados novos (Fiel ao banco de dados)
    chave.nome_chave = nome_chave
    chave.id_ambiente = id_ambiente
    chave.observacao_chave = observacao_chave
    chave.status = int(status) # <-- A mágica da conversão pra inteiro aqui!
    
    # 7. Salva as alterações
    sessao.commit()
    flash("Chave alterada com sucesso!", "success") # Corrigido o typo 'sucess'
        
    # Volta para a tela principal de chaves
    return redirect(url_for("chave"))

#chave excluir
@app.route("/chave/excluir", methods=["POST"])
@login_obrigatorio
@administrador_obrigatorio
def excluir_chave():
    # 1. Pega o ID que veio escondido no formulário da modal
    id_chave = request.form.get("id_chave")
    
    # 2. Busca a chave no banco
    chave = sessao.query(Chave).get(id_chave)
    
    # 3. Realiza a exclusao da chave
    if chave:
        sessao.delete(chave)
        sessao.commit()
        flash("Excluído com sucesso!", "success") # Corrigido para 'success' com dois 'c' e dois 's'
    else:
        flash("Chave não encontrada!", "danger")
    
    # 4. Retorna a tela principal de chaves
    return redirect(url_for("chave"))

#usuario
@app.route("/usuario", methods=["GET", "POST"])
@login_obrigatorio
@administrador_obrigatorio
def usuario():
    # 1. Pega os perfis para preencher o <select> do formulário
    todos_perfis = sessao.query(Perfil).all()
    
    if request.method == "POST":
        # 2. Pegando os dados EXATOS do HTML e do Banco
        email = request.form.get("email")
        senha_usuario = request.form.get("senha_usuario")
        id_perfil = request.form.get("id_perfil")
        nivel = request.form.get("nivel") # <-- Capturando o nível enviado pelo select do HTML
        senha_hash = generate_password_hash(senha_usuario)
        
        # 3. Validação (usando o E-mail)
        if not email or email.strip() == "":
            flash("O E-mail é obrigatório!", "danger")
            # Envia os perfis e dados vazios para a tela não quebrar
            return render_template("usuario.html", perfis=todos_perfis, dados=[])

        # 4. Inserir usuário no banco (com o nível)
        novo_usuario = Usuario(
            email=email, 
            senha_usuario=senha_hash, 
            id_perfil=id_perfil,
            nivel=nivel # <-- Atribuindo o nível ao modelo/banco
        )
        
        sessao.add(novo_usuario)
        sessao.commit()
        flash("Usuário salvo com sucesso!", "success")

        # Redireciona para a página após o envio
        return redirect(url_for("usuario"))
   
    # 5. Ao abrir a tela, manda os perfis para o <select> e a lista vazia para a consulta
    return render_template('usuario.html', perfis=todos_perfis, dados=[])

#consultar usuário
@app.route("/usuario/consultar", methods=["GET"])
@login_obrigatorio
@administrador_obrigatorio
def consultar_usuario():
    
    email_busca = request.args.get("email", "")
    
    usuarios_perfis = sessao.query(Usuario, Perfil).join(
        Perfil, Usuario.id_perfil == Perfil.id_perfil
    ).filter(
        Usuario.email.like(f"%{email_busca}%")
    ).all()
    
    # Validação de segurança: se o arquivo físico da foto foi deletado da pasta, força o ícone padrão
    for u, p in usuarios_perfis:
        if p.foto_perfil:
            caminho_fisico = os.path.join('static', 'img', p.foto_perfil)
            if not os.path.exists(caminho_fisico):
                p.foto_perfil = "icon_user.png"
    
    todos_perfis = sessao.query(Perfil).all()
    
    return render_template("usuario.html", dados=usuarios_perfis, perfis=todos_perfis)

#alterar usuario
@app.route("/usuario/alterar", methods=["POST"])
@login_obrigatorio
@administrador_obrigatorio
def alterar_usuario():
    # 1. Pega o ID que veio escondido no formulário da modal
    id_usuario = request.form.get("id_usuario")
    
    # 2. Busca os dados do usuário no banco
    usuario = sessao.query(Usuario).get(id_usuario)
    
    # 3. Valida se o usuário existe
    if usuario is None:
        flash("Usuário não encontrado", "danger")
        return redirect(url_for("usuario"))
    
    # 4. Pega os dados exatos do HTML/Banco (incluindo o nível)
    email = request.form.get("email")
    senha_usuario = request.form.get("senha_usuario")
    id_perfil = request.form.get("id_perfil")
    nivel = request.form.get("nivel") # <-- Capturando o nível atualizado do modal
    
    # 5. Validação de segurança (usando email)
    if not email or email.strip() == "":
        flash("O E-mail é obrigatório!", "danger")
        return redirect(url_for("usuario"))
        
    # 6. Atualiza o objeto com os dados novos (com criptografia na senha e salvando o nível)
    usuario.email = email
    usuario.senha_usuario = generate_password_hash(senha_usuario) # Mantendo o hash seguro
    usuario.id_perfil = int(id_perfil) # Convertendo o ID do perfil para número inteiro!
    usuario.nivel = nivel # <-- Atualizando o nível do usuário
    
    # 7. Salva as alterações
    sessao.commit()
    flash("Usuário alterado com sucesso!", "success") 
    
    # Retorna para a tela principal
    return redirect(url_for("usuario"))

#usuario excluir
@app.route("/usuario/excluir", methods=["POST"])
@login_obrigatorio
@administrador_obrigatorio
def excluir_usuario():
   
    id_usuario = request.form.get("id_usuario")
    
   
    usuario = sessao.query(Usuario).get(id_usuario)

   
    if usuario:
        sessao.delete(usuario)
        sessao.commit()
        flash("Excluído com sucesso!", "success") 
    else:
        flash("Usuário não encontrado!", "danger")

    
    return redirect(url_for("usuario"))

#ambiente
@app.route("/ambiente", methods=["GET", "POST"])
@login_obrigatorio
@administrador_obrigatorio
def ambiente():
    if request.method == "POST":
        
        ambiente = request.form.get("nome_sala")
        observacao_ambiente = request.form.get("observacao_ambiente")
        tipo= request.form.get("tipo")
        localizacao=request.form.get("localizacao")
        
        
     
        if ambiente == "":
            flash("Nome da Sala é obrigatório!", "danger")
            return render_template("ambiente.html")

       
        a = Ambiente(nome_sala=ambiente, observacao_ambiente=observacao_ambiente, tipo=tipo, localizacao=localizacao)
        sessao.add(a)
        sessao.commit()
        flash("Sala salvo com sucesso!", "success")

       
        return redirect(url_for("ambiente"))
    
    return render_template('ambiente.html')

#ambiente consultar
@app.route("/ambiente/consultar",methods=["GET", "POST"])
@login_obrigatorio
@administrador_obrigatorio
def consultar_ambiente():
    
    ambiente_nome = request.args.get("ambiente","")
    
   
    ambientes = sessao.query(Ambiente).filter(Ambiente.nome_sala.like(f"%{ambiente_nome}%"))
    
    
    return render_template('ambiente.html', ambientes=ambientes)

#alterar ambiente
@app.route("/ambiente/alterar", methods=["POST"])
@login_obrigatorio
@administrador_obrigatorio
def alterar_ambiente():
  
    id_ambiente = request.form.get("id_ambiente")
    
   
    ambiente = sessao.query(Ambiente).get(id_ambiente)
    
   
    if ambiente is None:
        flash("Ambiente não encontrado.", "danger")
        return redirect(url_for("ambiente"))
        
   
    nome_sala = request.form.get("nome_sala")
    tipo = request.form.get("tipo")
    localizacao = request.form.get("localizacao")
    status = request.form.get("status")
    observacao = request.form.get("observacao_ambiente")
    
  
    if not nome_sala or nome_sala.strip() == "":
        flash("Nome do Ambiente é obrigatório!", "danger")
        return redirect(url_for("ambiente"))
        
  
    ambiente.nome_sala = nome_sala
    ambiente.tipo = tipo
    ambiente.localizacao = localizacao
    ambiente.status_ambiente = int(status)
    ambiente.observacao_ambiente = observacao
    
   
    sessao.commit()
    flash("Ambiente alterado com sucesso!", "success")
        
  
    return redirect(url_for("ambiente"))

#ambiente excluir
@app.route("/ambiente/excluir", methods=["POST"])
@login_obrigatorio
@administrador_obrigatorio
def excluir_ambiente():
    
    id_ambiente = request.form.get("id_ambiente")
    
  
    ambiente = sessao.query(Ambiente).get(id_ambiente)

    if ambiente:
        sessao.delete(ambiente)
        sessao.commit()
        flash("Excluído com sucesso!", "success") 
    else:
        flash("Ambiente não encontrado!", "danger")

    
    return redirect(url_for("ambiente"))

#perfil
@app.route("/perfil", methods=["GET", "POST"])
@login_obrigatorio
def perfil():

    if request.method == "POST":
        
        nome_perfil = request.form.get("nome_perfil")
        matricula = request.form.get("matricula")
        cargo = request.form.get("cargo")
        
        if not nome_perfil or nome_perfil.strip() == "":
            flash("Nome do Perfil é obrigatório!", "danger")
            # Importante: passar os perfis existentes de volta pra tela não quebrar a listagem se der erro
            perfis = sessao.query(Perfil).all()
            
            # Validação caso o arquivo físico tenha sumido
            for p in perfis:
                if p.foto_perfil:
                    caminho_fisico = os.path.join('static', 'img', p.foto_perfil)
                    if not os.path.exists(caminho_fisico):
                        p.foto_perfil = "icon_user.png"
                        
            return render_template("perfil.html", perfis=perfis)

        # --- LÓGICA DE CAPTURA E SALVAMENTO DA FOTO ---
        foto = request.files.get('foto')
        nome_arquivo = "icon_user.png"  # Valor padrão caso nenhuma foto seja enviada

        if foto and foto.filename != '':
            # Limpa o nome do arquivo para evitar caracteres especiais e espaços
            nome_arquivo = secure_filename(foto.filename)
            # Define o caminho completo dentro da sua pasta static/img/
            caminho_completo = os.path.join('static', 'img', nome_arquivo)
            # Salva o arquivo fisicamente na pasta
            foto.save(caminho_completo)
        # ---------------------------------------------

        p = Perfil(
            nome_perfil=nome_perfil, 
            matricula=matricula, 
            cargo=cargo,
            foto_perfil=nome_arquivo,  # Adicionando o nome da foto no banco
            status_perfil=1
        )
        
        sessao.add(p)
        sessao.commit()
        flash("Perfil salvo com sucesso!", "success")

        return redirect(url_for("perfil"))
   
    # Para o método GET (quando a página apenas carrega)
    perfis = sessao.query(Perfil).all()
    
    # Validação de segurança: se o arquivo físico foi deletado da pasta, força o ícone padrão
    for p in perfis:
        if p.foto_perfil:
            caminho_fisico = os.path.join('static', 'img', p.foto_perfil)
            if not os.path.exists(caminho_fisico):
                p.foto_perfil = "icon_user.png"

    return render_template('perfil.html', perfis=perfis)

#consultar perfil
@app.route("/perfil/consultar", methods=["GET"])
@login_obrigatorio
def consultar_perfil():
   
    nome_busca = request.args.get("nome_perfil", "")
    
    perfis = sessao.query(Perfil).filter(Perfil.nome_perfil.like(f"%{nome_busca}%")).all()
    
    return render_template("perfil.html", perfis=perfis)

#alterar perfil
@app.route("/perfil/alterar", methods=["POST"])
@login_obrigatorio
def alterar_perfil():
    
    id_perfil = request.form.get("id_perfil")
    
    perfil = sessao.query(Perfil).get(id_perfil)
    
    if perfil is None:
        flash("Perfil não encontrado", "danger")
        return redirect(url_for("perfil"))
    
    nome_perfil = request.form.get("nome_perfil")
    matricula = request.form.get("matricula")
    cargo = request.form.get("cargo")
    status_perfil = request.form.get("status_perfil")
    
    if not nome_perfil or nome_perfil.strip() == "":
        flash("Nome do Perfil é obrigatório!", "danger")
        return redirect(url_for("perfil"))
        
    perfil.nome_perfil = nome_perfil
    perfil.matricula = matricula
    perfil.cargo = cargo
    perfil.status_perfil = int(status_perfil) 
    
    # --- LÓGICA DE ALTERAÇÃO DA FOTO ---
    foto = request.files.get('foto')
    if foto and foto.filename != '':
        nome_arquivo = secure_filename(foto.filename)
        caminho_completo = os.path.join('static', 'img', nome_arquivo)
        foto.save(caminho_completo)
        perfil.foto_perfil = nome_arquivo  # Atualiza a foto apenas se uma nova foi enviada
    # ----------------------------------
    
    sessao.commit()
    flash("Perfil alterado com sucesso!", "success") 
    
    return redirect(url_for("perfil"))

#perfil excluir
@app.route("/perfil/excluir", methods=["POST"])
@login_obrigatorio
def excluir_perfil():
  
    id_perfil = request.form.get("id_perfil")
    
    perfil = sessao.query(Perfil).get(id_perfil)

    if perfil:
        sessao.delete(perfil)
        sessao.commit()
        flash("Excluído com sucesso!", "success") 
    else:
        flash("Perfil não encontrado!", "danger")

    return redirect(url_for("perfil"))

#movimentacao confirmar
@app.route("/movimentacao", methods=["GET", "POST"])
@login_obrigatorio
def movimentacao():
    if request.method == "POST":
        mov = sessao.query(Movimentacao).filter_by(codigo_reserva=request.form.get("codigo_reserva")).first()
        if mov:
            mov.date_hora_retirada, mov.status = datetime.now(), "Retirado"
            sessao.commit()
            flash(f"Retirada registrada! Cód: {mov.codigo_reserva}", "success")
        else:
            flash("Reserva não encontrada!", "danger")
        return redirect(url_for("movimentacao"))
    
    reservas_pendentes = sessao.query(Movimentacao, Perfil, Chave).join(Perfil, Movimentacao.id_perfil == Perfil.id_perfil).join(Chave, Movimentacao.id_chave == Chave.id_chave).filter(Movimentacao.status == "Reservado").all()
    movimentacoes_retiradas = sessao.query(Movimentacao, Perfil, Chave).join(Perfil, Movimentacao.id_perfil == Perfil.id_perfil).join(Chave, Movimentacao.id_chave == Chave.id_chave).filter(Movimentacao.status == "Retirado").all()
    
    return render_template('movimentacao.html', reservas_pendentes=reservas_pendentes, movimentacoes_retiradas=movimentacoes_retiradas)

#estonar_movimentacao
@app.route("/movimentacao/estornar", methods=["POST"])
@login_obrigatorio
def estornar_retirada():
    mov = sessao.query(Movimentacao).get(request.form.get("id_movimentacao"))
    if mov:
        mov.status, mov.date_hora_retirada = "Reservado", None
        sessao.commit()
        flash("Retirada estornada com sucesso!", "warning")
    else:
        flash("Movimentação não encontrada!", "danger")
    return redirect(url_for("movimentacao"))

#devolucao confirmar
@app.route("/devolucao", methods=["GET", "POST"])
@login_obrigatorio
def devolucao():
    if request.method == "POST":
        mov = sessao.query(Movimentacao).filter_by(codigo_reserva=request.form.get("codigo_reserva")).first()
        if mov:
            mov.date_hora_devolucao, mov.status = datetime.now(), "Devolvido"
            sessao.commit()
            flash(f"Devolução registrada! Cód: {mov.codigo_reserva}", "success")
        else:
            flash("Movimentação não encontrada!", "danger")
        return redirect(url_for("devolucao"))
    chaves_retiradas = sessao.query(Movimentacao, Perfil, Chave).join(Perfil, Movimentacao.id_perfil == Perfil.id_perfil).join(Chave, Movimentacao.id_chave == Chave.id_chave).filter(Movimentacao.status == "Retirado").all()
    chaves_devolvidas = sessao.query(Movimentacao, Perfil, Chave).join(Perfil, Movimentacao.id_perfil == Perfil.id_perfil).join(Chave, Movimentacao.id_chave == Chave.id_chave).filter(Movimentacao.status == "Devolvido").all()
    return render_template('devolucao.html', chaves_retiradas=chaves_retiradas, chaves_devolvidas=chaves_devolvidas)

#estonar_devolucao
@app.route("/devolucao/estornar", methods=["POST"])
@login_obrigatorio
def estornar_devolucao():
    mov = sessao.query(Movimentacao).get(request.form.get("id_movimentacao"))
    if mov:
        mov.status, mov.date_hora_devolucao = "Retirado", None
        sessao.commit()
        flash("Devolução estornada com sucesso!", "warning")
    else:
        flash("Movimentação não encontrada!", "danger")
    return redirect(url_for("devolucao"))

#reserva
@app.route("/reserva", methods=["GET", "POST"])
@login_obrigatorio
def reserva():
    todos_perfis = sessao.query(Perfil).all()
    todas_chaves = sessao.query(Chave).all()
    
    if request.method == "POST":
        id_perfil = request.form.get("id_perfil")
        id_chave = request.form.get("id_chave")
        date_hora_reserva = request.form.get("date_hora_reserva")
        date_hora_devolucao_prev = request.form.get("date_hora_devolucao_prev")
        
        status = "Reservado"
        
        # Gera o código aleatório de 6 dígitos
        codigo_reserva = str(randint(100000, 999999))

        nova_mov = Movimentacao(
            id_perfil=id_perfil,
            id_chave=id_chave,
            codigo_reserva=codigo_reserva,
            status=status,
            date_hora_reserva=date_hora_reserva,
            date_hora_devolucao_prev=date_hora_devolucao_prev
        )
        
        sessao.add(nova_mov)
        sessao.commit()
        
        # BUSCA O E-MAIL DO USUÁRIO USANDO O id_perfil QUE VEIO DO FORMULÁRIO
        usuario_destino = sessao.query(Usuario).filter_by(id_perfil=id_perfil).first()
        
        if usuario_destino and usuario_destino.email:
            # Envia o e-mail usando o e-mail encontrado na tabela de usuário
            enviar_email_reserva(usuario_destino.email, codigo_reserva)
        
        flash(f"Reserva realizada com sucesso! Código: {codigo_reserva}", "success")
        return redirect(url_for("reserva"))
        
    return render_template('reserva.html', perfils=todos_perfis, chaves=todas_chaves, dados_reservas=[])

#consultar reserva
@app.route("/reserva/consultar", methods=["GET"])
@login_obrigatorio
def consultar_reserva():
    termo_busca = request.args.get("reserva", "")
    
    query = sessao.query(Movimentacao, Perfil, Chave).join(
        Perfil, Movimentacao.id_perfil == Perfil.id_perfil
    ).join(
        Chave, Movimentacao.id_chave == Chave.id_chave
    )
    
    if termo_busca.strip():
        query = query.filter(Movimentacao.codigo_reserva.like(f"%{termo_busca}%"))
        
    dados_reservas = query.all()
    
    todos_perfis = sessao.query(Perfil).all()
    todas_chaves = sessao.query(Chave).all()
    
    return render_template("reserva.html", dados_reservas=dados_reservas, perfils=todos_perfis, chaves=todas_chaves)

#alterar reserva
@app.route("/reserva/alterar", methods=["POST"])
@login_obrigatorio
def alterar_reserva():
    id_movimentacao = request.form.get("id_movimentacao")
    mov = sessao.query(Movimentacao).get(id_movimentacao)
    
    if mov is None:
        flash("Reserva não encontrada.", "danger")
        return redirect(url_for("reserva"))
        
    mov.id_perfil = request.form.get("id_perfil")
    mov.id_chave = request.form.get("id_chave")
    mov.date_hora_reserva = request.form.get("date_hora_reserva")
    mov.date_hora_devolucao_prev = request.form.get("date_hora_devolucao_prev")
    
    sessao.commit()
    flash("Reserva alterada com sucesso!", "success")
    return redirect(url_for("reserva"))

#reserva excluir
@app.route("/reserva/excluir", methods=["POST"])
@login_obrigatorio
def excluir_reserva():
    id_movimentacao = request.form.get("id_movimentacao")
    mov = sessao.query(Movimentacao).get(id_movimentacao)

    if mov:
        sessao.delete(mov)
        sessao.commit()
        flash("Excluído com sucesso!", "success")
    else:
        flash("Reserva não encontrada!", "danger")

    return redirect(url_for("reserva"))

#historico
@app.route("/historico", methods=["GET"])
@login_obrigatorio
def historico():
    termo_busca = request.args.get("busca", "").strip()
    historico_geral = []
    
    
    if "busca" in request.args and not termo_busca:
        flash("Para pesquisar, o código da reserva é obrigatório!", "warning")
        return redirect(url_for("historico"))
    
    if termo_busca:
        historico_geral = sessao.query(Movimentacao, Perfil, Chave).join(
            Perfil, Movimentacao.id_perfil == Perfil.id_perfil
        ).join(
            Chave, Movimentacao.id_chave == Chave.id_chave
        ).filter(
            Movimentacao.codigo_reserva.like(f"%{termo_busca}%")
        ).all()
        
    return render_template('historico.html', historico=historico_geral, termo_busca=termo_busca)

#relatorio
@app.route("/relatorio", methods=["GET"])
@administrador_obrigatorio
def relatorio():
    # Pega os valores que vieram do formulário de filtro
    data_inicio = request.args.get("data_inicio")
    data_fim = request.args.get("data_fim")
    status_filtro = request.args.get("status")
    
    # Inicia a consulta unindo Movimentacao com Perfil e Chave para buscar os nomes reais
    query = sessao.query(Movimentacao, Perfil, Chave).join(
        Perfil, Movimentacao.id_perfil == Perfil.id_perfil
    ).join(
        Chave, Movimentacao.id_chave == Chave.id_chave
    )
    
    # Se o usuário escolheu um status, filtra por ele
    if status_filtro:
        query = query.filter(Movimentacao.status == status_filtro)
        
    # Filtros de data
    if data_inicio:
        query = query.filter(Movimentacao.date_hora_reserva >= data_inicio)
    if data_fim:
        query = query.filter(Movimentacao.date_hora_reserva <= data_fim)
        
    # Executa a consulta final com os filtros aplicados
    resultados = query.all()
    
    # Monta a lista organizada para o HTML com a primeira letra maiúscula (.title())
    dados_relatorio = []
    for mov, perfil, chave in resultados:
        dados_relatorio.append({
            "codigo_reserva": mov.codigo_reserva,
            "nome_perfil": perfil.nome_perfil.title() if perfil.nome_perfil else "",
            "nome_chave": chave.nome_chave.title() if chave.nome_chave else "",
            "date_hora_reserva": mov.date_hora_reserva,
            "status": mov.status
        })
    
    return render_template('relatorio.html', dados_relatorio=dados_relatorio)

#esqueci_senha
@app.route("/esqueci-senha", methods=["GET", "POST"])
def esqueci_senha():
    if request.method == "POST":
        email = request.form.get("email")
        usuario = sessao.query(Usuario).filter_by(email=email).first()
        
        if usuario is None:
            flash("E-mail não encontrado!", "danger")
            return redirect(url_for("esqueci_senha"))
        
        nova_senha = str(random.randint(100000, 999999))
        usuario.senha_usuario = generate_password_hash(nova_senha)
        sessao.commit()
        enviar_email(email, nova_senha)
        flash("Uma nova senha foi enviada para seu e-mail!","success")
        return redirect(url_for("login"))

    return render_template("esqueci_senha.html")

#login
import time

@app.route("/login", methods=["GET", "POST"])
def login():
    # Garante que a variável sempre exista com valor padrão
    tempo_bloqueio = 0

    # Verifica se o usuário está bloqueado por excesso de tentativas
    bloqueio_ate = session.get("bloqueio_ate", 0)
    tempo_atual = time.time()
    
    if tempo_atual < bloqueio_ate:
        tempo_bloqueio = int(bloqueio_ate - tempo_atual)
        flash(f"Muitas tentativas incorretas. Aguarde {tempo_bloqueio} segundos para tentar novamente.", "danger")
        return render_template('login.html', tempo_bloqueio=tempo_bloqueio)

    if request.method == "POST":
        email_login = request.form.get('email')
        senha_login = request.form.get('senha')
        
        # Busca o usuário no banco de dados pelo e-mail
        usuario = sessao.query(Usuario).filter_by(email=email_login).first()
        
        # Verifica se o usuário existe e se a senha está correta
        if usuario and check_password_hash(usuario.senha_usuario, senha_login):
            # Login bem-sucedido: limpa o contador de tentativas e o bloqueio
            session.pop("tentativas_login", None)
            session.pop("bloqueio_ate", None)

            session["id_usuario"] = usuario.id_usuario
            session["email"] = usuario.email          
            session["id_perfil"] = usuario.id_perfil
            session["nivel"] = usuario.nivel      
            
            # Pega os dados do perfil vinculado (nome e foto)
            perfil = sessao.query(Perfil).filter_by(id_perfil=usuario.id_perfil).first()
            if perfil:
                session["perfil"] = perfil.nome_perfil
                # Pega a foto do perfil (se não tiver, usa o ícone padrão)
                session["foto_usuario"] = perfil.foto_perfil if perfil.foto_perfil else "icon_user.png"
            else:
                session["foto_usuario"] = "icon_user.png"
            
            # Flash card verde de sucesso
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("home"))
        
        # --- LÓGICA DE CONTROLE DE TENTATIVAS FALHAS ---
        tentativas = session.get("tentativas_login", 0) + 1
        session["tentativas_login"] = tentativas
        
        if tentativas >= 5:
            tempo_bloqueio = 30
            session["bloqueio_ate"] = time.time() + tempo_bloqueio
            flash(f"Limite de tentativas excedido. Aguarde {tempo_bloqueio} segundos.", "danger")
            return render_template('login.html', tempo_bloqueio=tempo_bloqueio)
        
        restantes = 5 - tentativas
        flash(f"E-mail ou senha inválidos. Você tem mais {restantes} tentativa(s).", "danger")
        
    return render_template('login.html', tempo_bloqueio=tempo_bloqueio)

#logout
@app.route("/logout")
@login_obrigatorio
def logout():
    session.clear()
    flash("Logout realizado.", "success")
    return redirect(url_for("login"))



# perfil_adm = sessao.query(Perfil).first()
# if perfil_adm is None:
#     perfil_adm = Perfil(nome_perfil="Administrador")
#     sessao.add(perfil_adm)
#     sessao.commit()
#     print("Perfil 'Administrador' criado com sucesso!")

# email_admin = "bryan@gmail.com"
# usuario_existente = sessao.query(Usuario).filter_by(email=email_admin).first()

# if usuario_existente is None:
#     novo_usuario = Usuario(
#         email=email_admin,
#         senha_usuario=generate_password_hash("1234"),  
#         id_perfil=perfil_adm.id_perfil,               
#         nivel="Administrador"                         
#     )
#     sessao.add(novo_usuario)
#     sessao.commit()
#     print(f"Usuário Administrador ({email_admin}) criado com sucesso!")
# else:
#     print("Usuário Administrador já existe no banco.")

app.run(debug=True)