import tkinter as tk


# ==========================================
# JANELA
# ==========================================

janela = tk.Tk()
janela.title("Calculadora")
janela.geometry("350x560")
janela.resizable(False, False)


# ==========================================
# VARIÁVEIS
# ==========================================

expressao = ""
tema_atual = "Preto"


# ==========================================
# TEMAS
# ==========================================

temas = {
    "Preto": {
        "fundo": "#1e1e1e",
        "visor": "#2b2b2b",
        "numero": "#333333",
        "operador": "#ff9500",
        "igual": "#34c759",
        "texto": "#ffffff"
    },

    "Vermelho": {
        "fundo": "#2b0f0f",
        "visor": "#451515",
        "numero": "#6b2020",
        "operador": "#e63946",
        "igual": "#34c759",
        "texto": "#ffffff"
    },

    "Branco": {
        "fundo": "#eeeeee",
        "visor": "#ffffff",
        "numero": "#dddddd",
        "operador": "#ff9500",
        "igual": "#34c759",
        "texto": "#111111"
    },

    "Amarelo": {
        "fundo": "#332f00",
        "visor": "#4a4300",
        "numero": "#665d00",
        "operador": "#ffc107",
        "igual": "#34c759",
        "texto": "#ffffff"
    },

    "Azul": {
        "fundo": "#0d1b2a",
        "visor": "#1b263b",
        "numero": "#274c77",
        "operador": "#0077b6",
        "igual": "#34c759",
        "texto": "#ffffff"
    },

    "Verde": {
        "fundo": "#0b2e13",
        "visor": "#123d1b",
        "numero": "#1b5e20",
        "operador": "#43a047",
        "igual": "#34c759",
        "texto": "#ffffff"
    }
}


# ==========================================
# FUNÇÕES PARA SALVAR E CARREGAR O TEMA
# ==========================================

def salvar_tema(nome_tema):
    try:
        with open("config.txt", "w", encoding="utf-8") as arquivo:
            arquivo.write(nome_tema)
    except Exception:
        pass


def carregar_tema():
    try:
        with open("config.txt", "r", encoding="utf-8") as arquivo:
            tema = arquivo.read().strip()

            if tema in temas:
                return tema

    except FileNotFoundError:
        pass

    return "Preto"


# ==========================================
# FUNÇÕES DA CALCULADORA
# ==========================================

def atualizar_visor():
    visor_var.set(expressao)


def adicionar(valor):
    global expressao

    expressao += str(valor)
    atualizar_visor()


def limpar():
    global expressao

    expressao = ""
    visor_var.set("0")


def apagar():
    global expressao

    expressao = expressao[:-1]

    if expressao:
        atualizar_visor()
    else:
        visor_var.set("0")


def calcular():
    global expressao

    try:
        resultado = eval(expressao)

        if isinstance(resultado, float) and resultado.is_integer():
            resultado = int(resultado)

        expressao = str(resultado)
        atualizar_visor()

    except ZeroDivisionError:
        expressao = ""
        visor_var.set("Não é possível dividir por 0")

    except Exception:
        expressao = ""
        visor_var.set("Erro")


# ==========================================
# SISTEMA DE TEMAS
# ==========================================

def mudar_tema(nome_tema):
    global tema_atual

    tema_atual = nome_tema

    tema = temas[nome_tema]

    # Cor do texto
    if nome_tema == "Branco":
        cor_texto = "#111111"
    else:
        cor_texto = "#ffffff"

    # Janela
    janela.configure(bg=tema["fundo"])

    # Frame
    frame.configure(bg=tema["fundo"])

    # Visor
    visor.configure(
        bg=tema["visor"],
        disabledbackground=tema["visor"],
        disabledforeground=cor_texto
    )

    # Botão de temas
    botao_temas.configure(
        bg=tema["numero"],
        fg=cor_texto,
        activebackground=tema["visor"],
        activeforeground=cor_texto
    )

    # Botões
    for botao in botoes_widgets:

        texto = botao["text"]

        # Operadores
        if texto in ["+", "−", "×", "÷"]:

            botao.configure(
                bg=tema["operador"],
                fg="#ffffff",
                activebackground=tema["operador"],
                activeforeground="#ffffff"
            )

        # Igual
        elif texto == "=":

            botao.configure(
                bg=tema["igual"],
                fg="#ffffff",
                activebackground=tema["igual"],
                activeforeground="#ffffff"
            )

        # Números e outros
        else:

            botao.configure(
                bg=tema["numero"],
                fg=cor_texto,
                activebackground=tema["visor"],
                activeforeground=cor_texto
            )


# ==========================================
# MENU DE TEMAS
# ==========================================

def abrir_menu_temas():

    menu = tk.Toplevel(janela)

    menu.title("Escolha um tema")
    menu.geometry("280x390")
    menu.resizable(False, False)

    tema = temas[tema_atual]

    if tema_atual == "Branco":
        cor_texto = "#111111"
    else:
        cor_texto = "#ffffff"

    menu.configure(bg=tema["fundo"])

    titulo = tk.Label(
        menu,
        text="Escolha um tema",
        font=("Arial", 18, "bold"),
        bg=tema["fundo"],
        fg=cor_texto
    )

    titulo.pack(pady=20)

    for nome, configuracao in temas.items():

        if nome == "Branco":
            texto_botao = "#111111"
        else:
            texto_botao = "#ffffff"

        botao_tema = tk.Button(
            menu,
            text=nome,
            font=("Arial", 13, "bold"),
            width=18,
            bg=configuracao["numero"],
            fg=texto_botao,
            activebackground=configuracao["visor"],
            activeforeground=texto_botao,
            command=lambda n=nome: selecionar_tema(n, menu)
        )

        botao_tema.pack(pady=5)


def selecionar_tema(nome_tema, menu):

    # Muda o tema
    mudar_tema(nome_tema)

    # Salva o tema escolhido
    salvar_tema(nome_tema)

    # Fecha o menu
    menu.destroy()

    # Devolve o foco para a calculadora
    janela.focus_force()


# ==========================================
# TECLADO
# ==========================================

def tecla(evento):

    caractere = evento.char
    tecla_pressionada = evento.keysym

    if caractere in "0123456789+-*/().":
        adicionar(caractere)

    elif caractere == ",":
        adicionar(".")

    elif tecla_pressionada == "Return":
        calcular()

    elif tecla_pressionada == "BackSpace":
        apagar()

    elif tecla_pressionada == "Escape":
        limpar()


# ==========================================
# VISOR
# ==========================================

visor_var = tk.StringVar(value="0")

visor = tk.Entry(
    janela,
    textvariable=visor_var,
    font=("Arial", 28, "bold"),
    justify="right",
    state="disabled",
    relief="flat",
    disabledbackground="#2b2b2b",
    disabledforeground="#ffffff"
)

visor.pack(
    padx=15,
    pady=(20, 10),
    ipady=15,
    fill="x"
)


# ==========================================
# BOTÃO DE TEMAS
# ==========================================

botao_temas = tk.Button(
    janela,
    text="Temas",
    font=("Arial", 12, "bold"),
    command=abrir_menu_temas,
    relief="flat"
)

botao_temas.pack(
    padx=15,
    pady=(0, 5),
    fill="x"
)


# ==========================================
# FRAME DOS BOTÕES
# ==========================================

frame = tk.Frame(janela)

frame.pack(
    expand=True,
    fill="both",
    padx=10,
    pady=10
)


# ==========================================
# BOTÕES
# ==========================================

botoes = [
    ("C", 0, 0, limpar),
    ("⌫", 0, 1, apagar),
    ("(", 0, 2, lambda: adicionar("(")),
    (")", 0, 3, lambda: adicionar(")")),

    ("7", 1, 0, lambda: adicionar("7")),
    ("8", 1, 1, lambda: adicionar("8")),
    ("9", 1, 2, lambda: adicionar("9")),
    ("÷", 1, 3, lambda: adicionar("/")),

    ("4", 2, 0, lambda: adicionar("4")),
    ("5", 2, 1, lambda: adicionar("5")),
    ("6", 2, 2, lambda: adicionar("6")),
    ("×", 2, 3, lambda: adicionar("*")),

    ("1", 3, 0, lambda: adicionar("1")),
    ("2", 3, 1, lambda: adicionar("2")),
    ("3", 3, 2, lambda: adicionar("3")),
    ("−", 3, 3, lambda: adicionar("-")),

    ("0", 4, 0, lambda: adicionar("0")),
    (".", 4, 1, lambda: adicionar(".")),
    ("=", 4, 2, calcular),
    ("+", 4, 3, lambda: adicionar("+")),
]


botoes_widgets = []


# ==========================================
# CRIAR BOTÕES
# ==========================================

for texto, linha, coluna, comando in botoes:

    botao = tk.Button(
        frame,
        text=texto,
        font=("Arial", 18, "bold"),
        command=comando,
        relief="flat"
    )

    botao.grid(
        row=linha,
        column=coluna,
        sticky="nsew",
        padx=4,
        pady=4
    )

    botoes_widgets.append(botao)


# Distribuição dos botões
for i in range(5):
    frame.rowconfigure(i, weight=1)

for i in range(4):
    frame.columnconfigure(i, weight=1)


# ==========================================
# CARREGAR TEMA SALVO
# ==========================================

tema_salvo = carregar_tema()
mudar_tema(tema_salvo)


# ==========================================
# TECLADO
# ==========================================

janela.bind_all("<Key>", tecla)


# ==========================================
# INICIAR
# ==========================================

janela.mainloop()