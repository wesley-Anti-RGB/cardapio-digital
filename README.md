# Cardápio Digital: Sabor da Vila
 
Sistema web de cardápio digital para uma lanchonete fictícia. Mostra
produtos, preços e categorias e permite simular um pedido, com o
cálculo do total feito em Python.
 
Projeto desenvolvido no Curso Técnico Subsequente de Desenvolvimento
de Sistemas.
 
## Objetivo
 
Praticar a integração entre HTML, CSS e Python construindo um sistema
completo: o navegador mostra o cardápio e envia o formulário, e o
Python recebe os dados, valida as quantidades, calcula o pedido e
devolve a página atualizada.
 
## Tecnologias utilizadas
 
- **HTML**: estrutura, categorias, cartões de produtos e formulário.
- **CSS**: identidade visual, Flexbox, CSS Grid e responsividade.
- **Python 3**: servidor local com `http.server`, leitura do
  formulário com `urllib.parse` e proteção dos dados com `html`.

Sem frameworks, sem JavaScript, sem banco de dados e sem instalar
bibliotecas com pip.
 
## Funcionalidades
 
- Cabeçalho com nome da lanchonete e menu de navegação
- Apresentação do estabelecimento
- Categorias: lanches, hambúrgueres, pizzas, bebidas e sobremesas
- 15 produtos em cartões com imagem, nome, descrição e preço
- Campo de quantidade em cada produto
- Cálculo do subtotal de cada item e do total do pedido em Python
- Resumo do pedido com produtos, quantidades e valores
- Validação de quantidades vazias, negativas, decimais ou acima de 20
- Identificação do cliente pelo nome
- Escolha entre retirada no balcão e consumo no local
- Confirmação de pedido simulado
- Layout responsivo para computador, tablet e celular
 
## Estrutura
 
```
cardapio-digital/
    index.html
    style.css
    app.py
    README.md
    imagens/
```
 
## Como executar
 
1. Instale o Python 3 (única dependência).
2. Abra o terminal dentro da pasta `cardapio-digital`.
3. Execute `python app.py` (ou `py app.py` no Windows).
4. Abra o navegador em `http://127.0.0.1:8000`.
5. Para parar o servidor, aperte `Ctrl + C` no terminal.
 
## Limitações
 
- O pedido é apenas uma simulação: nada é enviado, pago ou salvo.
- Sem banco de dados, os dados somem ao fechar a página.
- O GitHub Pages não executa Python: o sistema roda localmente.
 
## Autor
 
Wesley .S