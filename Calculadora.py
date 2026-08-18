# Calculadora

num1 = int(input("Digite o primeiro numero: "))
num2 = int(input("Digite o segundo numero: "))
operacao = input("Digite a operação: ")

match operacao:
    case "+":
        res = num1 + num2
    case "-":
        res = num1 - num2
    case "*":
        res = num1 * num2
    case "/":
        res = num1 / num2

print(f"Resultado = {res}")