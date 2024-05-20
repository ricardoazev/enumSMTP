#!/bin/python
import socket
import sys
import re

print("                              _________   __________________________") 
print("  ____   ____  __ __  _____  /   _____/  /     \__    ___/\______  \ ")
print("_/ __ \ /    \|  |  \/     \ \_____  \  /  \ /  \|    |    |     ___/")
print("\  ___/|   |  \  |  /  Y Y  \/        \/    Y    \    |    |    |    ")
print(" \___  >___|  /____/|__|_|  /_______  /\____|__  /____|    |____|    ")
print("     \/     \/            \/        \/         \/                    ")
print("===================Dev-Ricardo=======================================")

if len(sys.argv) != 3:
    print("Modo de uso: python smtpenum.py IP lista_de_usuarios")
    sys.exit(0)

def connect_to_smtp_server(ip, port):
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.connect((ip, port))
    banner = tcp.recv(1024)
    print(banner.decode())  # Decodifica e imprime o banner
    return tcp

# Conectar ao servidor SMTP
tcp = connect_to_smtp_server(sys.argv[1], 25)

# Abrir o arquivo de usuários e verificar cada um
with open(sys.argv[2], 'r') as file:
    for linha in file:
        linha = linha.strip()  # Remove quebras de linha e espaços em branco
        if not linha:
            continue  # Pula linhas vazias
        # Conectar ao servidor SMTP se a conexão for fechada
        try:
            tcp.send(("VRFY " + linha + "\r\n").encode())
            user = tcp.recv(1024)
            user_decoded = user.decode() # Decodifica a resposta para usar com re.search
            # Se o usuário for encontrado, imprimir
            if re.search("252", user_decoded):
                print("Usuario encontrado: " + user_decoded.strip("252 2.0.0"))
        except ConnectionResetError:
            print("Conexão encerrada pelo servidor. Reconectando...")
            tcp.close()
            tcp = connect_to_smtp_server(sys.argv[1], 25)

tcp.close()  # Fecha a conexão TCP

