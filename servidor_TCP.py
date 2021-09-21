#   JOGO DA VELHA - ATIVIDADE COM SOCKET TCP
#   Disciplina: Redes 1    Docente: Alvaro Souza
#   Discente: Felipe Xavier
#   
#   Jogador 'O'

import os
import socket

ip = ""
porta = 50000
origem = (ip, porta)

total_jogadas = 0
quem_venceu=""
jogada=""

simbolo = ["X", "O"]
jogadas_permitidas = ("0,0", "0,1", "0,2", "1,0", "1,1", "1,2", "2,0", "2,1", "2,2")
velha = [
    [" ", " ", " "],
    [" ", " ", " "],
    [" ", " ", " "]
]

def tela():
    global total_jogadas

    total_jogadas = 0
    for v in velha:
        total_jogadas += v.count('X') + v.count('O')

    os.system("clear")
    print("     0     1     2")
    print(" ")
    print("0   ", velha[0][0], " | ", velha[0][1], " | ", velha[0][2])
    print("---------------------")
    print("1   ", velha[1][0], " | ", velha[1][1], " | ", velha[1][2])
    print("---------------------")
    print("2   ", velha[2][0], " | ", velha[2][1], " | ", velha[2][2])
    print(" ")
    print("Jogadas: ", total_jogadas)
    print(" ")

def fim_jogo():
    global quem_venceu
    global total_jogadas
    soma_l = soma_c = 0
    
    for s in simbolo:
        # Verifica linhas e colunas
        for i in range(0,3):
            for j in range(0,3):    
                if velha[j][i] == s:
                    soma_c += 1
                if velha[i][j] == s:
                    soma_l += 1
            if soma_c == 3 or soma_l == 3:
                quem_venceu = s
                return True
            soma_l = 0
            soma_c = 0

        # Verifica as duas diagonais
        # diagonal principal
        diagonal = velha[0][0] == s and velha[1][1] == s and velha[2][2] == s     
        # diagonal secundaria     
        diagonal = diagonal or (velha[0][2] == s and velha[1][1] == s and velha[2][0] == s)   
        if diagonal:
            quem_venceu = s
            return True

        # Verifica se ocorrreu o numero maximo de jogadas...deu velha    
        if total_jogadas == 9:
            quem_venceu = "Velha"
            return True
    
    return False


def jogar():
    global jogada
    global quem_joga
    resposta = ""

    os.system("clear")
    tela()

    while jogada not in jogadas_permitidas:
        jogada = input("Informe [Linha, Coluna]: ")
        
    
    l,c = jogada.split(",")
    l = int(l)
    c = int(c)

    if(velha[l][c] != "X" and velha[l][c] != "O"):
        jogada = ""
        velha[l][c] = simbolo[1]

    os.system("clear")
    tela()

    resposta = ','.join(velha[0])
    resposta += ";" + ','.join(velha[1])
    resposta += ";" + ','.join(velha[2])

    return resposta



tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

tcp.bind(origem)
tcp.listen(1)
tcp_dados, cliente = tcp.accept()


while not fim_jogo():
    tam_resp = int.from_bytes(tcp_dados.recv(1), 'big')
    resp = tcp_dados.recv(tam_resp)
    resp = resp.decode()
    
    velha = []
    resp = resp.split(';')   
    for r in resp:
        velha.append(r.split(','))
    
    msg = jogar()
    
    tam = (len(msg)).to_bytes(1, 'big')
    tcp_dados.send(tam + msg.encode())


tcp_dados.close()
tcp.close()

tela()
print("                                    FIM DE JOGO!")
print("-------------------------------------------------")

if quem_venceu != "Velha":
    print("    Jogador \"", quem_venceu, "\" venceu!")
else:
    print("    Deu velha...")

print("-------------------------------------------------")
print(" ")
