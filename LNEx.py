#-*-coding: utf-8-*-
import socket
import select
import sys
import os
import thread
import subprocess

class Main():
  def __init__(self):
    os.system('cls' if os.name == 'nt' else 'clear')
    print ""
    print "        Bem-vindo ao LNEx  "
    print ""
    print "[+]  Você está na versão 0.0.1a."
    print "[+]  Este programa foi desenvolvido por @LinconD, em caso de dúvida"
    print "viste o !ajuda ou entre em contato comigo."
    print "[+]  Você pode visitar o !sobre para mais informações sobre o programa!"
    print "[!]  Em caso de bugs ou falhas, favor reportar no GitHub com screenshot!"
    print "O GitHub está disponivel em !sobre"
    print "[+]  Console Inciado."
    print "[!]Aguardando Instruções."

    self.isRunning = True

    while self.isRunning:
      self.core(self.getNext())

    sys.exit()

  def getNext(self):
    self.next = raw_input("(Menu Inicial)> ")
    return self.next

  def core(self, firstArgument):
    self.next = firstArgument

    if self.next == "!ajuda":
      os.system('cls' if os.name == 'nt' else 'clear')
      print "[!]Você está em: Ajuda"
      print "   Abaixo estão listado os comando disponiveis no programa:"
      print "       !ajuda - mostra esse menu."
      print "       !servidor - inicia uma instância de servidor."
      print "       !cliente - inicia uma instância de cliente."
      print "       !sobre  - mostra os comentarios do dev."
      print "       !sair - sai do programa e fecha as dependências."
      print "[!]Aguardando instruções."

    elif self.next == "!servidor":
        os.system('cls' if os.name == 'nt' else 'clear')
        print "[+]  Inciando servidor..."
        self.servidor = Servidor()

    elif self.next == "!cliente":
        print "[?]  Entre com o IP:"
        self.ip = raw_input("(IP)>")
        os.system('cls' if os.name == 'nt' else 'clear')
        print "[+]  Inciando conexão..."
        self.cliente = Cliente(self.ip)

    elif self.next == "!sobre":
        os.system('cls' if os.name == 'nt' else 'clear')
        print "LNEx é um programa desenvolvido por LinconD, com a função de"
        print "executar comandos bash em várias máquinas ao mesmo tempo dentro de"
        print "uma rede local."
        print "Por enquanto o programa está disponível para a plataforma Linux."
        print "Outras plataformas virão no futuro."
        print "Caso necessite de ajuda consulte nosso github."
        print "http://github.com/LinconD/LNEx"
        print ""
        print "[!]Aguardando instruções."

    elif self.next == "!sair":
        os.system('cls' if os.name == 'nt' else 'clear')
        print "[!]  Encerrando as dependências e saindo..."
        self.isRunning = False

    elif self.next != "!ajuda" and \
         self.next != "!sobre" and \
         self.next != "!servidor" and \
         self.next != "!cliente" and \
         self.next != "!sair":
            print "[-]  Comando não encontrado! Verifique a ortografia ou se não esqueceu do '!'"

    def directConnect(self, IP):
        print "Direct connect!"


class Servidor():
    def __init__(self):
        #Várivéis para o servidor
        self.HOST = "127.0.0.1"
        self.PORT = 5056

        self.CONNECTION_LIST = []
        self.SERVER_LIST = []

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.HOST, self.PORT))
    	self.server_socket.listen(5)

        self.SERVER_LIST.append(self.server_socket)

        print "[+]  Servidor iniciado na porta " + str(self.PORT)
        print "[+]  Inciando engine..."

        self.isRunning = True

        print "[+]  Tudo pronto."
        print "[!]  Aguardando instruções."

        thread.start_new_thread(self.svUpdate, ())

        while self.isRunning:
            self.svEngine(self.getNext())

    def svEngine(self, argument):
        self.next = argument

        if self.next == "!ajuda":
            os.system('cls' if os.name == 'nt' else 'clear')
            print "[!]Você está em Servidor -> ajuda."
            print " Os seguintes comandos estão disponíveis para o servidor:"
            print "         !ajuda - mostra esse menu."
            print "         !sair - para o servidor e volta para o menu principal."
            print "         !limpar - limpa a janela."
            print " Ou simplesmente digite algum comando shell para enviar!"
            print "[!]Aguardando instruções."

        elif self.next == "!sair":
            print "[!]  Fechando o servidor e desconectando."
            self.server_socket.close()
            #Sai de tudo para evitar erro de Adress already in use.
            thread.exit()

        elif self.next == "!limpar":
            os.system('cls' if os.name == 'nt' else 'clear')

        elif self.next != "!ajuda" and self.next != "!sair" and self.next != "!limpar":
            self.svDistBash(self.next)

    def svDistBash(self, bash):
        for socket in self.CONNECTION_LIST:
            try:
                print "[+]  Enviando para (%s)...!" %socket
                socket.sendall(bash)
            except:
                #Zicou a conexão
                socket.close()
    	        self.CONNECTION_LIST.remove(socket)
                print "[-]  Cliente (%s, %s) desconectado" %self.addr


    def svUpdate(self):
        while self.isRunning:
            self.read_sockets, self.write_sockets, self.error_sockets = select.select(self.SERVER_LIST, self.CONNECTION_LIST, [])

            for sock in self.read_sockets:
                if sock == self.server_socket:
                    #Alguem tentando entrar! OMG!
                    self.sockfd, self.addr = self.server_socket.accept()
                    self.CONNECTION_LIST.append(self.sockfd)
                    print "[+]  Cliente (%s, %s) conectado" %self.addr
                    print "[!]  Pronto para receber comando:"

    def getNext(self):
      self.next = raw_input("(Servidor)> ")
      return self.next


class Cliente():
    def __init__(self, ip):
        #Várivéis para o cliente
        self.HOST = ip
        self.PORT = 5056

        self.clsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.isRunning = True

        print "[+]  Cliente criado."
        print "[+]  Tentando conectar ao servidor %s" %self.HOST
        try:
            self.clsock.connect((self.HOST, self.PORT))
        except:
            print "[-] Não foi possível conectar ao servidor, cheque sua conexão."
            self.isRunning = False

        if self.isRunning:
            print "[+]  Inciando a engine..."
            print "[+]  Tudo certo. Apartir desse momento não há comandos disponíveis."

            print "[+]  Conectado com %s, pronto para receber comandos" %self.HOST

            while self.isRunning:
                self.clEngine()



    def clEngine(self):
        try:
            self.bash = self.clsock.recv(1024)
            print "(Recebido)> %s" %self.bash
            self.clBash(self.bash)
            if not self.bash:
                self.clsock.close()
        except:
            self.clsock.close()
            print "[-]  Desconectado do servidor!"
            print "[+]  De volta ao menu principal! Para reconectar digite !cliente"
            self.isRunning = False

    def clBash(self, bash):
        self.shell = subprocess.Popen(bash, shell=True, executable="/bin/bash")

    def getNext(self):
      self.next = raw_input("(Cliente)> ")
      return self.next

if __name__ == "__main__":

    if len(sys.argv) > 1:
        run = Main().directConnect()
    else:
        run = Main();
