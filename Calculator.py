import customtkinter as ctk

# ---------- Cores no estilo da calculadora do iPhone ----------
COR_FUNDO = "#000000"
COR_NUMERO = "#333333"
COR_NUMERO_HOVER = "#555555"
COR_OPERADOR = "#510E7E"
COR_OPERADOR_HOVER = "#FFB143"
COR_FUNCAO = "#A5A5A5"
COR_FUNCAO_HOVER = "#D4D4D2"
COR_TEXTO_CLARO = "#FFFFFF"
COR_TEXTO_ESCURO = "#000000"

# ---------- Estado da calculadora ----------
operacao_atual = ""
primeiro_numero = None
operador = None

# ---------- Funções de lógica ----------
def atualizar_display(texto):
    display.configure(text=texto)

def clique_numero(numero):
    global operacao_atual
    if numero == "," and "," in operacao_atual:
        return  # evita duas vírgulas
    operacao_atual += str(numero)
    atualizar_display(operacao_atual)

def clique_operador(op):
    global operacao_atual, primeiro_numero, operador
    if operacao_atual == "":
        return
    primeiro_numero = float(operacao_atual.replace(",", "."))
    operador = op
    operacao_atual = ""

def clique_igual():
    global operacao_atual, primeiro_numero, operador
    if primeiro_numero is None or operacao_atual == "":
        return
    segundo_numero = float(operacao_atual.replace(",", "."))

    if operador == "+":
        resultado = primeiro_numero + segundo_numero
    elif operador == "-":
        resultado = primeiro_numero - segundo_numero
    elif operador == "×":
        resultado = primeiro_numero * segundo_numero
    elif operador == "÷":
        resultado = primeiro_numero / segundo_numero if segundo_numero != 0 else "Erro"
    else:
        resultado = segundo_numero

    resultado_str = str(resultado).replace(".", ",")
    atualizar_display(resultado_str)
    operacao_atual = resultado_str
    primeiro_numero = None
    operador = None

def clique_funcao(funcao):
    global operacao_atual, primeiro_numero, operador
    if funcao == "C":
        operacao_atual = ""
        primeiro_numero = None
        operador = None
        atualizar_display("0")
    elif funcao == "+/-":
        if operacao_atual.startswith("-"):
            operacao_atual = operacao_atual[1:]
        elif operacao_atual != "":
            operacao_atual = "-" + operacao_atual
        atualizar_display(operacao_atual if operacao_atual else "0")
    elif funcao == "%":
        if operacao_atual != "":
            valor = float(operacao_atual.replace(",", ".")) / 100
            operacao_atual = str(valor).replace(".", ",")
            atualizar_display(operacao_atual)

# ---------- Janela principal ----------
ctk.set_appearance_mode("dark")
janela = ctk.CTk()
janela.title("Calculadora")
janela.geometry("320x480")
janela.configure(fg_color=COR_FUNDO)

# ---------- Display ----------
display = ctk.CTkLabel(
    janela,
    text="0",
    font=("Arial", 48),
    anchor="e",
    text_color=COR_TEXTO_CLARO,
    fg_color=COR_FUNDO,
)
display.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=15, pady=(30, 10))

# ---------- Botões ----------
# (texto, linha, coluna, colspan, tipo)
botoes = [
    ("C", 1, 0, 1, "funcao"), ("+/-", 1, 1, 1, "funcao"), ("%", 1, 2, 1, "funcao"), ("÷", 1, 3, 1, "operador"),
    ("7", 2, 0, 1, "numero"), ("8", 2, 1, 1, "numero"), ("9", 2, 2, 1, "numero"), ("×", 2, 3, 1, "operador"),
    ("4", 3, 0, 1, "numero"), ("5", 3, 1, 1, "numero"), ("6", 3, 2, 1, "numero"), ("-", 3, 3, 1, "operador"),
    ("1", 4, 0, 1, "numero"), ("2", 4, 1, 1, "numero"), ("3", 4, 2, 1, "numero"), ("+", 4, 3, 1, "operador"),
    ("0", 5, 0, 2, "numero"), (",", 5, 2, 1, "numero"), ("=", 5, 3, 1, "operador"),
]

for texto, linha, coluna, colspan, tipo in botoes:
    if tipo == "numero":
        cor, cor_hover, cor_texto = COR_NUMERO, COR_NUMERO_HOVER, COR_TEXTO_CLARO
        comando = lambda t=texto: clique_numero(t)
    elif tipo == "operador":
        cor, cor_hover, cor_texto = COR_OPERADOR, COR_OPERADOR_HOVER, COR_TEXTO_CLARO
        comando = clique_igual if texto == "=" else (lambda t=texto: clique_operador(t))
    else:  # funcao
        cor, cor_hover, cor_texto = COR_FUNCAO, COR_FUNCAO_HOVER, COR_TEXTO_ESCURO
        comando = lambda t=texto: clique_funcao(t)

    botao = ctk.CTkButton(
        janela,
        text=texto,
        font=("Arial", 26),
        fg_color=cor,
        hover_color=cor_hover,
        text_color=cor_texto,
        corner_radius=40,
        width=70,
        height=70,
        command=comando,
    )

    sticky = "w" if colspan == 2 else "nsew"
    botao.grid(row=linha, column=coluna, columnspan=colspan, padx=6, pady=6, sticky=sticky)

# Faz linhas e colunas crescerem de forma proporcional
for i in range(6):
    janela.rowconfigure(i, weight=1)
for i in range(4):
    janela.columnconfigure(i, weight=1)

janela.mainloop()