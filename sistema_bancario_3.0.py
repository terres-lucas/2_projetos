import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo

        if valor > saldo:
            print("\nVocê não possui saldo suficiente.")

        elif valor > 0:
            print(f"\nSaque de: R$ {valor:.2f}")
            menu_confirmar()
            if opcao == "1":
                self._saldo -= valor
                print("\n=== Saque realizado com sucesso! ===")
                return True

        else:
            print("\nValor inválido.")

        return False

    def depositar(self, valor):
        if valor > 0:
            menu_confirmar()
            if opcao == "1":
                self._saldo += valor
                print("\nDepósito realizado com sucesso!")
        else:
            print("\O valor informado é inválido.")
            return False

        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == "saque"]
        )

        if valor > self._limite:
            print("\nO valor do saque excede o limite. Verifique seu extrato")

        elif numero_saques >= self._limite_saques:
            print("\nNúmero máximo de saques excedido. Verifique seu extrato")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            {"Agência":<10}:{self.agencia}
            {"C/C":<10}:{self.numero}
            {"Titular":<10}:\t{self.cliente.nome}
        """

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M"),
            }
        )

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def menu_principal():
    menu_principal = ("""\n
    =============== MENU =================
    [1]\tAcessar Conta
    [2]\tAbertura de Conta
    [3]\tSair
    """)
    print(textwrap.dedent(menu_principal))
    return input("Escolha uma opção: ")

def menu_conta():
    menu_conta = """\n
    =============== CONTA =================
    [1]\tDepósito
    [2]\tSaque
    [3]\tExtrato
    [4]\Minha(s) Conta(s)
    [5]\tVoltar
    """
    print(textwrap.dedent(menu_conta))
    return input("Escolha uma opção: ")

def menu_confirmar():
    menu_confirmar = """\n
    ============== CONFIRMAR ==============
    [1]\tSim
    [2]\tNão
    """
    print(textwrap.dedent(menu_confirmar))
    input("Escolha uma opção: ")
    if opcao == "2":
        return False
    else:
        return True

def menu_voltar(menu):
    menu_voltar = """\n
    =====================================

    Deseja realizar outra operação?
    [1]\tSim
    [2]\tNão
    """
    print(textwrap.dedent(menu_voltar))
    opcao = input("Escolha uma opção: ")
    if opcao == "1":
        opcao_menu = menu()
        return opcao_menu
    elif opcao == "2":
        return False

def menu_cadastro():
    menu_cadastro = ("""\n
    ============== CADASTRO ===============
    Se você já possui cadastro, selecione a opção 2.

    [1]\tCadastro
    [2]\tAbrir Nova Conta
    [3]\tSair
    """)
    print(textwrap.dedent(menu_cadastro))
    return input("Escolha uma opção: ")


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\Cliente não possui conta!")
        return

    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]


def depositar(clientes, cpf_cliente):
    cpf = cpf_cliente
    cliente = filtrar_cliente(cpf, clientes)

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def sacar(clientes, cpf_cliente):
    cpf = cpf_cliente
    cliente = filtrar_cliente(cpf, clientes)

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes, cpf_cliente):
    cpf = cpf_cliente
    cliente = filtrar_cliente(cpf, clientes)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")


def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\Já existe cliente com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("\n=== Cliente cadastrado com sucesso! ===")


def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
        contas.append(conta)
        cliente.contas.append(conta)
        print("\n=== Conta criada com sucesso! ===")

    else:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
        return

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

# implementações

def acessar_conta(cpf_cliente):
    cpf = cpf_cliente
    cliente = filtrar_cliente(cpf, clientes)
    if cliente:
        menu_conta()
    else:
        print("\nCliente não encontrado")



clientes = []
contas = []

while True:
    opcao = menu_principal()
    if opcao == "1":
        cpf = input("Informe o seu CPF: ")
        opcao = acessar_conta(cpf)
        
        if opcao == "1":
            depositar(clientes, cpf)
            menu_voltar(acessar_conta)

        elif opcao == "2":
            sacar(clientes, cpf)
            menu_voltar(acessar_conta)

        elif opcao == "3":
            exibir_extrato(clientes, cpf)
            menu_voltar(acessar_conta)

        elif opcao == "4":
            listar_contas(contas)

        elif opcao == "5":
            menu_voltar(menu_principal)

        else:
            print("Opção inválida. Tente novamente.")

    elif opcao == "2":
        opcao = menu_cadastro()
       
        if opcao == "1":
            opcao = criar_cliente(clientes)

        elif opcao == "2":
            numero_conta = len(contas) + 1
            opcao = criar_conta(numero_conta, clientes, contas)
        
    elif opcao == "3":
        print("Obrigado por usar nossos serviços!")
        break

    elif opcao == "4":
        print("Admin")
        listar_contas(contas)
        
    else:
        print("Opção inválida. Tente novamente.")