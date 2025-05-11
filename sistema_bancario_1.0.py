menu = """

[1] Depósito
[2] Saque
[3] Extrato
[0] Sair

>>> """

menu_confirma = """

Confirmar?
[1] Sim
[2] Não

>>> """

menu_voltar = """

Voltar ao menu principal?
[1] Voltar
[0] Encerrar o atendimento

>>> """

saldo_inicial = 1000
saldo_final = saldo_inicial
limite_saque = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:
    opcao = int(input(menu))

    if (opcao != 1) and (opcao != 2) and (opcao != 3) and (opcao != 0):
        print("Opção inválida. Tente novamente.")
    
# DEPÓSITO
    elif opcao == 1:
        print("Depósito")
        valor_deposito = int(input("Digite o valor desejado:  "))
        confirmar = int(input(menu_confirma))
        if confirmar == 1:
            saldo_final += valor_deposito
            extrato += (f"{"Depósito":<17} R$ {valor_deposito:>10.2f}\n")
            print(f"Valor depositado de R$ {valor_deposito:.2f}")
            print("Operação realizada com sucesso")
            
# SAQUE
    elif opcao == 2:
        print("Saque")
        valor_saque = float(input("Digite o valor desejado:  "))
        if (valor_saque > limite_saque) or (numero_saques >= LIMITE_SAQUES) or (valor_saque > saldo_final):
            print("Operação não permitida. Verifique o extrato da sua conta.")
            voltar = int(input(menu_voltar))
            if voltar == 2:
                print("Operação encerrado pelo usuário. Obrigado por usar nossos serviços.")
                break
        else:
            confirmar = int(input(menu_confirma))
            if confirmar == 1:
                limite_saque += valor_saque
                numero_saques += 1
                saldo_final -= valor_saque
                extrato += (f"{"Saque":<16}- R$ {valor_saque:>10.2f}\n")
                print("Operação realizada com sucesso")
            
# EXTRATO
    elif opcao == 3:
        print(f"\n{"Extrato":^31}\n{"-" * 31}")
        print(f"{"Saldo inicial":<17} R$ {saldo_inicial:>10.2f}")
        print(extrato)
        print(f"{"-" * 31}\n{"Saldo em conta":<17} R$ {saldo_final:>10.2f}")
        print(f"\nSaques diários disponíveis: {(3 - numero_saques):>3}")
        voltar = int(input(menu_voltar))
        if voltar == 0:
            print("Operação encerrado pelo usuário. Obrigado por usar nossos serviços.")
            break
    else: 
        print("Operação encerrado pelo usuário. Obrigado por usar nossos serviços.")
        break