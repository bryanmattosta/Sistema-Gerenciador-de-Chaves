from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine, Column, Integer, String, Numeric, Date
from sqlalchemy.orm import declarative_base, sessionmaker
from flask_sqlalchemy import SQLAlchemy
from tabelas import engine, Base, Chave, Usuario, Perfil, Ambiente, Movimentacao
from random import randint
from datetime import datetime
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect
from email.message import EmailMessage
from flask import send_file
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import random
import smtplib


#cria a sesao
Session = sessionmaker(bind=engine)
sessao  = Session()


app = Flask(__name__)
app.secret_key="123456"

#home
@app.route("/")
def home(): 
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
def consultar_chave():
    #Pegar a chave foi informada
    chave_nome = request.args.get("nome_chave","")
    todos_ambientes = sessao.query(Ambiente).all()
    #consultar chave
    chaves = sessao.query(Chave).filter(Chave.nome_chave.like(f"%{chave_nome}%")).all()
    #chamar cahve.html para mostrar dados
    return render_template('chave.html', chaves=chaves, ambientes=todos_ambientes)

#alterar
@app.route("/chave/alterar", methods=["POST"])
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

#chave 
@app.route("/chave/excluir", methods=["POST"])
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
def usuario():
    # 1. Pega os perfis para preencher o <select> do formulário
    todos_perfis = sessao.query(Perfil).all()
    
    if request.method == "POST":
        # 2. Pegando os dados EXATOS do HTML e do Banco
        email = request.form.get("email")
        senha_usuario = request.form.get("senha_usuario")
        id_perfil = request.form.get("id_perfil")
        
        # 3. Validação (usando o E-mail, já que não temos o nome)
        if not email or email.strip() == "":
            flash("O E-mail é obrigatório!", "danger")
            # Envia os perfis e dados vazios para a tela não quebrar
            return render_template("usuario.html", perfis=todos_perfis, dados=[])

        # 4. Inserir usuário no banco
        novo_usuario = Usuario(
            email=email, 
            senha_usuario=senha_usuario, 
            id_perfil=id_perfil
        )
        
        sessao.add(novo_usuario)
        sessao.commit()
        flash("Usuário salvo com sucesso!", "success")

        # Redireciona para a página inicial após o envio
        return redirect(url_for("usuario"))
   
    # 5. Ao abrir a tela, manda os perfis para o <select> e a lista vazia para a consulta
    return render_template('usuario.html', perfis=todos_perfis, dados=[])

#consultar usuário
@app.route("/usuario/consultar", methods=["GET"])
def consultar_usuario():
    
    # 1. Pega o e-mail que foi digitado na barra de pesquisa
    email_busca = request.args.get("email", "")
    
    # 2. Faz o JOIN entre Usuário e Perfil, mas filtrando pelo E-MAIL
    usuarios_perfis = sessao.query(Usuario, Perfil).join(
        Perfil, Usuario.id_perfil == Perfil.id_perfil
    ).filter(
        Usuario.email.like(f"%{email_busca}%")
    ).all()
    
    # 3. Busca todos os perfis (Isso é obrigatório para o <select> da Modal de Editar não quebrar!)
    todos_perfis = sessao.query(Perfil).all()
    
    # 4. Chama a tela enviando os resultados da busca (dados) e os perfis
    return render_template("usuario.html", dados=usuarios_perfis, perfis=todos_perfis)

#alterar usuario
@app.route("/usuario/alterar", methods=["POST"])
def alterar_usuario():
    # 1. Pega o ID que veio escondido no formulário da modal
    id_usuario = request.form.get("id_usuario")
    
    # 2. Busca os dados do usuário no banco
    usuario = sessao.query(Usuario).get(id_usuario)
    
    # 3. Valida se o usuário existe
    if usuario is None:
        flash("Usuário não encontrado", "danger")
        return redirect(url_for("usuario"))
    
    # 4. Pega os dados exatos do HTML/Banco
    email = request.form.get("email")
    senha_usuario = request.form.get("senha_usuario")
    id_perfil = request.form.get("id_perfil")
    
    # 5. Validação de segurança (usando email)
    if not email or email.strip() == "":
        flash("O E-mail é obrigatório!", "danger")
        return redirect(url_for("usuario"))
        
    # 6. Atualiza o objeto com os dados novos
    usuario.email = email
    usuario.senha_usuario = senha_usuario
    usuario.id_perfil = int(id_perfil) # Convertendo o ID do perfil para número inteiro!
    
    # 7. Salva as alterações
    sessao.commit()
    flash("Usuário alterado com sucesso!", "success") 
    
    # Retorna para a tela principal
    return redirect(url_for("usuario"))

#usuario excluir falta ver
@app.route("/usuario/excluir", methods=["POST"])
def excluir_usuario():
    # 1. Pega o ID que veio escondido no formulário da modal
    id_usuario = request.form.get("id_usuario")
    
    # 2. Busca os dados do usuário
    usuario = sessao.query(Usuario).get(id_usuario)

    # 3. Realiza a exclusão do usuário
    if usuario:
        sessao.delete(usuario)
        sessao.commit()
        flash("Excluído com sucesso!", "success") # Corrigido para 'success'
    else:
        flash("Usuário não encontrado!", "danger")

    # 4. Retorna a tela principal do usuário
    return redirect(url_for("usuario"))

#ambiente
@app.route("/ambiente", methods=["GET", "POST"])
def ambiente():
    if request.method == "POST":
        # Aqui você pode processar os dados do formulário, por exemplo, salvando em um banco de dados
        ambiente = request.form.get("nome_sala")
        observacao_ambiente = request.form.get("observacao_ambiente")
        tipo= request.form.get("tipo")
        localizacao=request.form.get("localizacao")
        
        
        # Validação do nome
        if ambiente == "":
            flash("Nome da Sala é obrigatório!", "danger")
            return render_template("ambiente.html")

        #inserir ambiente
        a = Ambiente(nome_sala=ambiente, observacao_ambiente=observacao_ambiente, tipo=tipo, localizacao=localizacao)
        sessao.add(a)
        sessao.commit()
        flash("Sala salvo com sucesso!", "success")

        # Redireciona para a página inicial após o envio do formulário
        return redirect(url_for("ambiente"))
    
    return render_template('ambiente.html')

#ambiente consultar
@app.route("/ambiente/consultar",methods=["GET", "POST"])
def consultar_ambiente():
    #Pegar o ambiente informado
    ambiente_nome = request.args.get("ambiente","")
    
    #consultar chave
    ambientes = sessao.query(Ambiente).filter(Ambiente.nome_sala.like(f"%{ambiente_nome}%"))
    
    #chamar p ambiente.html para mostrar dados
    return render_template('ambiente.html', ambientes=ambientes)

#alterar ambiente
@app.route("/ambiente/alterar", methods=["POST"])
def alterar_ambiente():
    # 1. Pega o ID que veio escondido naquele campo <input type="hidden"> da modal
    id_ambiente = request.form.get("id_ambiente")
    
    # 2. Busca o ambiente no banco
    ambiente = sessao.query(Ambiente).get(id_ambiente)
    
    # 3. Valida se o ambiente existe
    if ambiente is None:
        flash("Ambiente não encontrado.", "danger")
        return redirect(url_for("ambiente"))
        
    # 4. Pega os dados exatos usando os atributos 'name' do HTML
    nome_sala = request.form.get("nome_sala")
    tipo = request.form.get("tipo")
    localizacao = request.form.get("localizacao")
    status = request.form.get("status")
    observacao = request.form.get("observacao_ambiente")
    
    # 5. Validação de segurança simples
    if not nome_sala or nome_sala.strip() == "":
        flash("Nome do Ambiente é obrigatório!", "danger")
        return redirect(url_for("ambiente"))
        
    # 6. Atualiza o objeto com os dados novos
    ambiente.nome_sala = nome_sala
    ambiente.tipo = tipo
    ambiente.localizacao = localizacao
    ambiente.status_ambiente = int(status)
    ambiente.observacao_ambiente = observacao
    
    # 7. Salva as alterações direto
    sessao.commit()
    flash("Ambiente alterado com sucesso!", "success")
        
    # Volta para a tela de ambientes
    return redirect(url_for("ambiente"))

#ambiente excluir
@app.route("/ambiente/excluir", methods=["POST"])
def excluir_ambiente():
    # 1. Pega o ID que veio escondido no formulário da modal
    id_ambiente = request.form.get("id_ambiente")
    
    # 2. Busca o ambiente no banco
    ambiente = sessao.query(Ambiente).get(id_ambiente)

    # 3. Realiza a exclusao do ambiente
    if ambiente:
        sessao.delete(ambiente)
        sessao.commit()
        flash("Excluído com sucesso!", "success") # Corrigido para 'success'
    else:
        flash("Ambiente não encontrado!", "danger")

    # 4. Retorna a tela principal do ambiente
    return redirect(url_for("ambiente"))

#perfil
@app.route("/perfil", methods=["GET", "POST"])
def perfil():

    if request.method == "POST":
        # Pegando os dados EXATOS com os 'names' definidos no HTML
        nome_perfil = request.form.get("nome_perfil")
        matricula = request.form.get("matricula")
        cargo = request.form.get("cargo")
        
        # Validação de segurança simples
        if not nome_perfil or nome_perfil.strip() == "":
            flash("Nome do Perfil é obrigatório!", "danger")
            # Tem que passar a lista de perfis no erro também para não quebrar a página
            return render_template("perfil.html")

        # Inserir perfil (já definindo status_perfil=1 para nascer Ativo)
        p = Perfil(
            nome_perfil=nome_perfil, 
            matricula=matricula, 
            cargo=cargo,
            status_perfil=1
        )
        
        sessao.add(p)
        sessao.commit()
        flash("Perfil salvo com sucesso!", "success")

        # Redireciona para limpar o formulário e evitar duplo envio
        return redirect(url_for("perfil"))
   
    # Envia a variável 'perfis' para o HTML desenhar os cards
    return render_template('perfil.html')

#consultar perfil
@app.route("/perfil/consultar", methods=["GET"])
def consultar_perfil():
    # 1. Pega o texto que foi digitado na barra de pesquisa (nome exato do HTML)
    nome_busca = request.args.get("nome_perfil", "")
    
    # 2. Consulta o(s) perfil(is) no banco filtrando pelo nome
    perfis = sessao.query(Perfil).filter(Perfil.nome_perfil.like(f"%{nome_busca}%")).all()
    
    # 3. Chama a página perfil.html enviando os resultados da busca
    return render_template("perfil.html", perfis=perfis)

#alterar perfil
@app.route("/perfil/alterar", methods=["POST"])
def alterar_perfil():
    # 1. Pega o ID que veio escondido no formulário da modal
    id_perfil = request.form.get("id_perfil")
    
    # 2. Busca os dados do perfil no banco
    perfil = sessao.query(Perfil).get(id_perfil)
    
    # 3. Valida se existe o perfil
    if perfil is None:
        flash("Perfil não encontrado", "danger")
        return redirect(url_for("perfil"))
    
    # 4. Pega os dados exatos do HTML/Banco
    nome_perfil = request.form.get("nome_perfil")
    matricula = request.form.get("matricula")
    cargo = request.form.get("cargo")
    status_perfil = request.form.get("status_perfil")
    
    # 5. Validação de segurança
    if not nome_perfil or nome_perfil.strip() == "":
        flash("Nome do Perfil é obrigatório!", "danger")
        return redirect(url_for("perfil"))
        
    # 6. Atualiza o objeto com os dados novos
    perfil.nome_perfil = nome_perfil
    perfil.matricula = matricula
    perfil.cargo = cargo
    perfil.status_perfil = int(status_perfil) 
    
    # 7. Salva as alterações
    sessao.commit()
    flash("Perfil alterado com sucesso!", "success") 
    
    # Retorna para a tela principal
    return redirect(url_for("perfil"))

#perfil excluir
@app.route("/perfil/excluir", methods=["POST"])
def excluir_perfil():
    # 1. Pega o ID que veio escondido no formulário da modal de exclusão
    id_perfil = request.form.get("id_perfil")
    
    # 2. Busca os dados do perfil pelo ID
    perfil = sessao.query(Perfil).get(id_perfil)

    # 3. Realiza a exclusão do perfil
    if perfil:
        sessao.delete(perfil)
        sessao.commit()
        flash("Excluído com sucesso!", "success") # Corrigido para 'success' (com 2 C's e 2 S's)
    else:
        flash("Perfil não encontrado!", "danger")

    # 4. Retorna a tela principal do perfil
    return redirect(url_for("perfil"))

@app.route("/movimentacao", methods=["GET", "POST"])
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
def estornar_retirada():
    mov = sessao.query(Movimentacao).get(request.form.get("id_movimentacao"))
    if mov:
        mov.status, mov.date_hora_retirada = "Reservado", None
        sessao.commit()
        flash("Retirada estornada com sucesso!", "warning")
    else:
        flash("Movimentação não encontrada!", "danger")
    return redirect(url_for("movimentacao"))

#devolucao #feita
@app.route("/devolucao", methods=["GET", "POST"])
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
def reserva():
    todos_perfis = sessao.query(Perfil).all()
    todas_chaves = sessao.query(Chave).all()
    
    if request.method == "POST":
        id_perfil = request.form.get("id_perfil")
        id_chave = request.form.get("id_chave")
        date_hora_reserva = request.form.get("date_hora_reserva")
        date_hora_devolucao_prev = request.form.get("date_hora_devolucao_prev")
        
        status = "Reservado"
        
        # CHAMANDO O RANDINT DIRETO (Sem o 'random.')
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
        flash(f"Reserva realizada com sucesso! Código: {codigo_reserva}", "success")
        return redirect(url_for("reserva"))
        
    return render_template('reserva.html', perfils=todos_perfis, chaves=todas_chaves, dados_reservas=[])

#consultar reserva
@app.route("/reserva/consultar", methods=["GET"])
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
@app.route("/historico", methods=["GET"])
def historico():
    termo_busca = request.args.get("busca", "").strip()
    historico_geral = []
    
    if termo_busca:
        historico_geral = sessao.query(Movimentacao, Perfil, Chave).join(
            Perfil, Movimentacao.id_perfil == Perfil.id_perfil
        ).join(
            Chave, Movimentacao.id_chave == Chave.id_chave
        ).filter(
            Movimentacao.codigo_reserva.like(f"%{termo_busca}%")
        ).all()
        
    return render_template('historico.html', historico=historico_geral, termo_busca=termo_busca)

@app.route("/esqueci-senha", methods=["GET", "POST"])
def esqueci_senha():
    if request.method == "POST":
        email = request.form.get("email")
        usuario = sessao.query(Usuario).filter_by(email=email).first()
        
        if usuario is None:
            flash("E-mail não encontrado!", "danger")
            return redirect(url_for("esqueci_senha"))
        
        nova_senha = str(random.randint(100000, 999999))
        usuario.senha = generate_password_hash(nova_senha)
        sessao.commit()
        enviar_email(email, nova_senha)
        flash("Uma nova senha foi enviada para seu e-mail!","success")
        return redirect(url_for("login"))

    return render_template("esqueci_senha.html")

app.run(debug=True)