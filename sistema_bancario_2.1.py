# VARIAVEIS
AGENCIA = "0001"
LIMITE_SAQUES = 3

saldo = 1000
limite_por_saque = 500
extrato = ""
saques_efetuados = 0
usuarios = []
contas = []

#MENUS
def menu_principal(): 
    menu_principal = """

    [1]\tDepósito
    [2]\tSaque
    [3]\tExtrato
    [4]\tNovo Usuário
    [5]\tNova Conta
    [6]\tListar Contas
    [0]\tSair

    >>> """
    return input(menu_principal)

def menu_confirmar():
  
    confirmacao = input(
        """
    Confirmar?
    [1] Sim
    [2] Não

    >>> """)
    
    if confirmacao != "1":
        menu_principal()

# DEPÓSITO
def deposito(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += (f"\n{"Depósito":<22} R$ {valor:>10.2f}")
        print(f"Valor depositado de R$ {valor:.2f}")
    else:
        print(f"Valor de de R$ {valor:.2f} inválido. Tente novamente.")
    return saldo, extrato

# SAQUE 
def saque(*, saldo, valor, extrato, limite_por_saque, saques_efetuados, LIMITE_SAQUES):
    if (valor > limite_por_saque) or (saques_efetuados >= LIMITE_SAQUES) or (valor > saldo):
        print("Operação não permitida. Verifique o extrato da sua conta.")
    elif valor > 0:
        saques_efetuados += 1
        saldo -= valor
        extrato += (f"\n{"Saque":<21}- R$ {valor:>10.2f}")
        print("Operação realizada com sucesso")
    else:
        print("Operação falhou. Informe um valor válido.")
    return saldo, extrato, saques_efetuados

# EXTRATO
def exibir_extrato(saldo, /, *, extrato):
    print(extrato)
    print(f"{"=" * 36}\n{"Saldo em Conta":<24}R${saldo:>10.2f}")
        
# filtrar usuario
def verificar_cliente(cpf, usuarios):
    clientes_cadastrados = [cliente for cliente in usuarios if cliente["cpf"] == cpf]
    return clientes_cadastrados[0] if clientes_cadastrados else None

# NOVO USUÁRIO
def novo_usuario(usuarios):
    cpf = input("Informe o CPF (somente números):  ")
    # if (len(cpf) != 11):
        # print("Digite um CPF válido.")
    
    cliente = verificar_cliente(cpf,usuarios)
    
    if cliente:
        print("Cliente já cadastrado.")
        return
    
    nome = input("Nome completo:  ")
    data_nascimento = input("Data de nascimento (dd-mm-aaaa):  ")
    endereco = input("Endereço (rua, nr, bairro, cidade-UF):  ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("\nNovo cliente cadastrado com sucesso!")
        
# NOVA CONTA

def nova_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF:  ")
    cliente = verificar_cliente(cpf, usuarios)

    if cliente:
        print("\n Parabéns! Você abriu sua conta!")
        return {"agencia": agencia, "numero_conta": numero_conta, "cliente": cliente}
    print("cliente não encontrado")

# LISTAR CONTAS

def listar_contas(contas):
    for conta in contas:
        print(f"""
        {'Agência:':<10}{conta['agencia']:<}
        {'C/C:':<10}{conta['numero_conta']:<}
        {'Titular:':<10}{conta['cliente']['nome']:<}
        """)

# OPERAÇÃO    

while True:
    opcao = menu_principal()

    if opcao == "1":
        print(f"{"=" * 11}{"DEPÓSITO":^14}{"=" * 11}")
        valor = float(input("Digite o valor do depósito:  "))
        menu_confirmar()
        saldo, extrato = deposito(saldo, valor, extrato)

    elif opcao == "2":
        print(f"{"=" * 11}{"SAQUE":^14}{"=" * 11}")
        valor_saque = float(input("Digite o valor desejado:  "))
        menu_confirmar()
        saldo, extrato, saques_efetuados = saque(
            saldo=saldo, 
            valor = valor_saque,
            extrato = extrato,
            limite_por_saque= limite_por_saque,
            saques_efetuados = saques_efetuados,
            LIMITE_SAQUES= LIMITE_SAQUES
        )

# EXTRATO
    elif opcao == "3":
        print(f"{"=" * 11}{"EXTRATO":^14}{"=" * 11}")
        exibir_extrato(saldo, extrato=extrato)
        print(f"\n{"Saques diários disponíveis:":<33}{LIMITE_SAQUES - saques_efetuados:>3}")
        
# NOVO CLIENTE
    elif opcao == "4":
        novo_usuario(usuarios)

# NOVA CONTA
    elif opcao == "5":
        numero_conta = len(contas) +1
        conta = nova_conta(AGENCIA, numero_conta, usuarios)

        if conta:
            contas.append(conta)
            
# LISTAR CONTAS 
    elif opcao == "6":
        listar_contas(contas)

# SAIR
    elif opcao == "0":
        print("Operação encerrado pelo usuário. Obrigado por usar nossos serviços.")
        break