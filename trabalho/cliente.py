import socket
import threading
import tkinter as tk
import select
import random
from tkinter import scrolledtext

class ChatUI:
    def __init__(self, client_socket):
        self.client_socket = client_socket
        self.running = True  # Sinalizador para controlar o loop principal
        self.nickname_colors = {}  # Dicionário para armazenar as cores dos nicknames

        self.root = tk.Tk()
        self.root.title('Chat')
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)  # Lidar com o evento de fechamento da janela

        self.nickname_entry = tk.Entry(self.root, width=30)
        self.nickname_entry.pack(pady=10)

        self.nickname_button = tk.Button(self.root, text="Entrar no Chat", command=self.join_chat)
        self.nickname_button.pack()

        self.chat_text = scrolledtext.ScrolledText(self.root)
        self.chat_text.pack(side=tk.TOP)

        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(side=tk.BOTTOM)

        self.input_label = tk.Label(self.input_frame, text='Digite sua mensagem:')
        self.input_label.pack(side=tk.LEFT)

        self.input_entry = tk.Entry(self.input_frame, width=50)
        self.input_entry.pack(side=tk.LEFT)
        self.input_entry.bind('<Return>', self.handle_enter)

        self.send_button = tk.Button(self.input_frame, text="Enviar", command=self.send_message)
        self.send_button.pack(side=tk.LEFT)

        self.quit_button = tk.Button(self.input_frame, text="Sair", command=self.on_close)
        self.quit_button.pack(side=tk.LEFT)

        self.update_chat()  # Iniciar atualização da interface gráfica

    def join_chat(self):
        nickname = self.nickname_entry.get().strip()
        if nickname:
            self.nickname_entry.config(state=tk.DISABLED)
            self.nickname_button.config(state=tk.DISABLED)
            self.nickname = nickname
            self.client_socket.send(nickname.encode())

    def send_message(self, event=None):
        message = self.input_entry.get().strip()
        if message:
            self.add_message(f'<{self.nickname}>: {message}', nickname=True)
            self.client_socket.send(message.encode())
            if message == ':quit':
                self.running = False
        self.input_entry.delete(0, tk.END)

    def add_message(self, message, nickname=False):
        self.chat_text.configure(state=tk.NORMAL)
        if nickname:
            if self.nickname not in self.nickname_colors:
                # Gerar cor aleatória com base no hash do nome de usuário
                random.seed(self.nickname)
                r = lambda: random.randint(0, 255)
                nickname_color = '#%02X%02X%02X' % (r(), r(), r())
                self.nickname_colors[self.nickname] = nickname_color
            else:
                nickname_color = self.nickname_colors[self.nickname]
            self.chat_text.insert(tk.END, message + '\n', 'nickname')
            self.chat_text.tag_configure('nickname', foreground=nickname_color)
        else:
            self.chat_text.insert(tk.END, message + '\n')
        self.chat_text.configure(state=tk.DISABLED)
        self.chat_text.see(tk.END)

    def handle_enter(self, event):
        self.send_message()

    def on_close(self):
        self.running = False
        self.root.destroy()

    def update_chat(self):
        if self.running:
            try:
                readable, _, _ = select.select([self.client_socket], [], [], 0.1)
                for sock in readable:
                    data = sock.recv(1024).decode()
                    if not data:
                        self.running = False
                        break
                    if ':' in data:
                        sender_nickname, message = data.split(':', 1)
                        self.add_message(f'<{sender_nickname.strip()}>: {message.strip()}', nickname=True)
                    else:
                        self.add_message(f'{data.strip()}: Mensagem recebida')
            except socket.error as e:
                print(f"Erro ao receber dados: {str(e)}")

            self.root.after(100, self.update_chat)  # Agendar a próxima atualização

def main():
    host = '192.168.250.148'  # Insira o IP do servidor aqui
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    chat_ui = ChatUI(client_socket)

    chat_ui.root.mainloop()

    client_socket.close()

if __name__ == '__main__':
    main()
?