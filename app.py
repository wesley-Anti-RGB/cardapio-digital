# Cardápio Digital: lanchonete Sabor da Vila
# Usa somente a biblioteca padrão do Python: nada para instalar.

import os
import random
from http.server import ThreadingHTTPServer
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs
from html import escape

PASTA = os.path.dirname(os.path.abspath(__file__))
PORTA = 8000
LIMITE_POR_ITEM = 20

# Cadastro: o código de cada produto aponta para nome e preço
PRODUTOS = {
    # Lanches
    "misto": {"nome": "Misto Quente", "preco": 8.00},
    "cachorro": {"nome": "Cachorro-Quente", "preco": 10.00},
    "natural": {"nome": "Sanduíche Natural", "preco": 12.00},
    # Hambúrgueres
    "xburguer": {"nome": "X-Burguer", "preco": 15.00},
    "xsalada": {"nome": "X-Salada", "preco": 17.00},
    "xbacon": {"nome": "X-Bacon", "preco": 20.00},
    # Pizzas
    "mussarela": {"nome": "Pizza de Mussarela", "preco": 22.00},
    "calabresa": {"nome": "Pizza de Calabresa", "preco": 24.00},
    "frango": {"nome": "Pizza de Frango", "preco": 26.00},
    # Bebidas
    "suco": {"nome": "Suco de Laranja", "preco": 7.00},
    "refri": {"nome": "Refrigerante Lata", "preco": 6.00},
    "agua": {"nome": "Água Mineral", "preco": 3.50},
    # Sobremesas
    "pudim": {"nome": "Pudim de Leite", "preco": 7.50},
    "brownie": {"nome": "Brownie", "preco": 8.50},
    "acai": {"nome": "Açaí na Tigela", "preco": 15.00},
}

OPCOES = {
    "retirada": "Retirada no balcão",
    "local": "Consumo no local",
}

TIPOS_IMAGEM = {
    ".svg": "image/svg+xml",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
}

# ---------- 1. Funções de apoio ----------

def ler_arquivo(nome):
    """Lê um arquivo de texto da pasta do projeto."""
    caminho = os.path.join(PASTA, nome)
    with open(caminho, encoding="utf-8") as arquivo:
        return arquivo.read()

def moeda(valor):
    """Transforma 1234.5 em 'R$ 1.234,50'."""
    texto = f"{valor:,.2f}"
    texto = texto.replace(",", "X").replace(".", ",")
    texto = texto.replace("X", ".")
    return f"R$ {texto}"

def campo(dados, nome):
    """Pega o valor de um campo enviado pelo formulário."""
    return dados.get(nome, [""])[0]

def ler_quantidade(texto, nome):
    """Converte o texto em número inteiro. Devolve (qtd, erro)."""
    texto = texto.strip()
    if texto == "":
        return 0, None
    try:
        qtd = int(texto)
    except ValueError:
        return 0, f"A quantidade de {nome} precisa ser inteira."
    if qtd < 0:
        return 0, f"A quantidade de {nome} não pode ser negativa."
    if qtd > LIMITE_POR_ITEM:
        erro = f"O limite é {LIMITE_POR_ITEM} unidades de {nome}."
        return 0, erro
    return qtd, None

# ---------- 2. Regras do pedido ----------

def ler_formulario(dados):
    """Organiza os dados enviados pelo navegador."""
    form = {
        "nome": campo(dados, "nome").strip(),
        "consumo": campo(dados, "consumo"),
        "quantidades": {},
    }
    for codigo in PRODUTOS:
        texto = campo(dados, "qtd_" + codigo).strip()
        if texto == "":
            texto = "0"
        form["quantidades"][codigo] = texto
    return form

def calcular_pedido(form):
    """Monta a lista de itens e calcula subtotais e total."""
    itens = []
    erros = []
    total = 0
    for codigo, produto in PRODUTOS.items():
        texto = form["quantidades"][codigo]
        qtd, erro = ler_quantidade(texto, produto["nome"])
        if erro:
            erros.append(erro)
            continue
        if qtd == 0:
            continue
        subtotal = qtd * produto["preco"]
        total = total + subtotal
        itens.append({
            "nome": produto["nome"],
            "qtd": qtd,
            "preco": produto["preco"],
            "subtotal": subtotal,
        })
    return itens, round(total, 2), erros

def validar_cliente(form):
    """Confere o nome e a forma de consumo. Devolve os erros."""
    erros = []
    if form["nome"] == "":
        erros.append("Informe seu nome para confirmar o pedido.")
    elif len(form["nome"]) > 40:
        erros.append("O nome pode ter no máximo 40 caracteres.")
    if form["consumo"] not in OPCOES:
        erros.append("Escolha retirada no balcão ou consumo no local.")
    return erros

# ---------- 3. Montagem da página ----------

def montar_mensagens(lista):
    """Transforma a lista de (tipo, texto) em parágrafos."""
    html = ""
    for tipo, texto in lista:
        html += f'<p class="mensagem {tipo}">{escape(texto)}</p>\n'
    return html

def montar_resumo(itens, total):
    """Cria a tabela do resumo com os itens escolhidos."""
    if not itens:
        return '<p class="vazio">Nenhum produto escolhido.</p>'
    linhas = ""
    for item in itens:
        linhas += (f"<tr><td>{escape(item['nome'])}</td>"
                   f"<td>{item['qtd']}</td>"
                   f"<td>{moeda(item['preco'])}</td>"
                   f"<td>{moeda(item['subtotal'])}</td></tr>\n")
    return f"""<table class="tabela-pedido"><thead><tr><th>Produto</th><th>Qtd.</th><th>Preço</th><th>Subtotal</th></tr></thead><tbody>{linhas}</tbody><tfoot><tr><td colspan="3">Total do pedido</td><td>{moeda(total)}</td></tr></tfoot></table>"""

def montar_confirmacao(form, total):
    """Cria o quadro de confirmação do pedido simulado."""
    numero = random.randint(100, 999)
    nome = escape(form["nome"])
    forma = OPCOES[form["consumo"]]
    return f"""<div class="confirmacao"><h3>Pedido simulado nº {numero} confirmado!</h3><p>Obrigado, {nome}. Forma escolhida: {forma}.</p><p>Valor total: <strong>{moeda(total)}</strong></p><p class="nota">Simulação escolar: nada foi enviado à cozinha, nenhum pagamento foi feito e nenhum dado foi salvo.</p></div>"""

def montar_pagina(form, acao):
    """Faz os cálculos e preenche as marcações do index.html."""
    itens, total, erros = calcular_pedido(form)
    resumo = montar_resumo(itens, total)
    mensagens = []
    confirmacao = ""

    if acao == "inicio":
        mensagens.append(("info", "Escolha as quantidades no cardápio e clique em Atualizar resumo."))
    elif erros:
        for erro in erros:
            mensagens.append(("erro", erro))
        resumo = ('<p class="vazio">Corrija as quantidades para ver o total.</p>')
    elif not itens:
        mensagens.append(("alerta", "Seu pedido está vazio. Escolha pelo menos um produto."))
    elif acao == "confirmar":
        erros_cliente = validar_cliente(form)
        for erro in erros_cliente:
            mensagens.append(("erro", erro))
        if not erros_cliente:
            mensagens.append(("ok", "Pedido simulado confirmado."))
            confirmacao = montar_confirmacao(form, total)
    else:
        mensagens.append(("ok", "Resumo atualizado. Para finalizar, informe seu nome e confirme."))

    unidades = 0
    for item in itens:
        unidades = unidades + item["qtd"]

    pagina = ler_arquivo("index.html")
    for codigo, produto in PRODUTOS.items():
        marca = codigo.upper()
        preco = moeda(produto["preco"])
        qtd = escape(form["quantidades"][codigo])
        pagina = pagina.replace("{{PRECO_" + marca + "}}", preco)
        pagina = pagina.replace("{{QTD_" + marca + "}}", qtd)

    retirada = ""
    local = ""
    if form["consumo"] == "retirada":
        retirada = "checked"
    elif form["consumo"] == "local":
        local = "checked"

    pagina = pagina.replace("{{ITENS}}", str(unidades))
    pagina = pagina.replace("{{NOME}}", escape(form["nome"]))
    pagina = pagina.replace("{{MARCAR_RETIRADA}}", retirada)
    pagina = pagina.replace("{{MARCAR_LOCAL}}", local)
    pagina = pagina.replace("{{MENSAGENS}}", montar_mensagens(mensagens))
    pagina = pagina.replace("{{RESUMO}}", resumo)
    pagina = pagina.replace("{{CONFIRMACAO}}", confirmacao)
    return pagina

# ---------- 4. Servidor ----------

class Atendente(BaseHTTPRequestHandler):
    """Atende cada pedido (requisição) que chega do navegador."""

    def do_GET(self):
        caminho = self.path.split("?")[0]
        if caminho == "/":
            form = ler_formulario({})
            pagina = montar_pagina(form, "inicio")
            self.responder(200, "text/html", pagina)
        elif caminho == "/style.css":
            css = ler_arquivo("style.css")
            self.responder(200, "text/css", css)
        elif caminho.startswith("/imagens/"):
            self.enviar_imagem(caminho)
        else:
            self.responder(404, "text/plain", "Não encontrado")

    def do_POST(self):
        tamanho = int(self.headers.get("Content-Length", 0))
        corpo = self.rfile.read(tamanho).decode("utf-8")
        dados = parse_qs(corpo, keep_blank_values=True)
        form = ler_formulario(dados)
        acao = campo(dados, "acao")
        pagina = montar_pagina(form, acao)
        self.responder(200, "text/html", pagina)

    def enviar_imagem(self, caminho):
        nome = os.path.basename(caminho)
        extensao = os.path.splitext(nome)[1].lower()
        arquivo = os.path.join(PASTA, "imagens", nome)
        if extensao not in TIPOS_IMAGEM:
            self.responder(404, "text/plain", "Não encontrado")
        elif not os.path.isfile(arquivo):
            self.responder(404, "text/plain", "Não encontrado")
        else:
            with open(arquivo, "rb") as imagem:
                conteudo = imagem.read()
            self.responder(200, TIPOS_IMAGEM[extensao], conteudo)

    def responder(self, codigo, tipo, conteudo):
        if isinstance(conteudo, str):
            conteudo = conteudo.encode("utf-8")
            tipo = tipo + "; charset=utf-8"
        self.send_response(codigo)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(conteudo)))
        self.end_headers()
        self.wfile.write(conteudo)

def mostrar_cadastro():
    """Lista os produtos no terminal e confere o index.html."""
    html = ler_arquivo("index.html")
    print("Produtos cadastrados:")
    for codigo, produto in PRODUTOS.items():
        print(f"  {produto['nome']:<20} {moeda(produto['preco'])}")
        if f'name="qtd_{codigo}"' not in html:
            print(f"  ATENÇÃO: falta o campo qtd_{codigo} no HTML")

mostrar_cadastro()
servidor = ThreadingHTTPServer(("127.0.0.1", PORTA), Atendente)
print(f"Cardápio Digital rodando em http://127.0.0.1:{PORTA}")
print("Para parar o servidor, aperte Ctrl + C")

try:
    servidor.serve_forever()
except KeyboardInterrupt:
    print("Servidor encerrado.")