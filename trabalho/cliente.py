import socket
import tkinter as tk
import select
import random
from tkinter import scrolledtext

class ChatUI:
    def __init__(self):
        self.client_socket = None
        self.running = True  # Sinalizador para controlar o loop principal
        self.nickname_colors = {}  # Dicionário para armazenar as cores dos nicknames

        self.root = tk.Tk()
        self.root.title('PodPapo')
        #self.root.iconbitmap('icone256.ico')  # Substitua pelo caminho para o seu arquivo .ico
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)  # Lidar com o evento de fechamento da janela

        input_frame = tk.Frame(self.root)
        input_frame.pack(side=tk.TOP)

        self.user_label = tk.Label(input_frame, text="Usuário:")
        self.user_label.pack(side=tk.LEFT)
        self.nickname_entry = tk.Entry(input_frame, width=30)
        self.nickname_entry.pack(side=tk.LEFT)

        self.ip_label = tk.Label(input_frame, text="IP do Servidor:")
        self.ip_label.pack(side=tk.LEFT)
        self.ip_entry = tk.Entry(input_frame, width=30)
        self.ip_entry.pack(side=tk.LEFT)

        self.nickname_button = tk.Button(self.root, text="Entrar no Chat", command=self.join_chat)
        self.nickname_button.pack(pady=10)

        self.chat_text = scrolledtext.ScrolledText(self.root)
        self.chat_text.pack(side=tk.TOP, padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.input_frame = tk.Frame(self.root, bd=2, relief=tk.GROOVE, padx=10, pady=10)
        self.input_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.input_label = tk.Label(self.input_frame, text='Digite sua mensagem:')
        self.input_label.pack(side=tk.LEFT)

        self.input_entry = tk.Entry(self.input_frame, width=50)
        self.input_entry.pack(side=tk.LEFT, padx=(5, 0))
        self.input_entry.bind('<Return>', self.handle_enter)

        self.send_button = tk.Button(self.input_frame, text="Enviar", command=self.send_message, padx=20)
        self.send_button.pack(side=tk.LEFT)

        self.quit_button = tk.Button(self.input_frame, text="Sair", command=self.on_close, padx=20)
        self.quit_button.pack(side=tk.LEFT)

        self.update_chat()  # Iniciar atualização da interface gráfica

    def join_chat(self):
        ip = self.ip_entry.get().strip()
        nickname = self.nickname_entry.get().strip()
        if ip and nickname:
            self.ip_entry.config(state=tk.DISABLED)
            self.nickname_entry.config(state=tk.DISABLED)
            self.nickname_button.config(state=tk.DISABLED)

            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((ip, 12345))
            self.client_socket.send(nickname.encode())
            self.nickname = nickname

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
        self.chat_text.see(tk.END)
        self.chat_text.configure(state=tk.DISABLED)

    def update_chat(self):
        if self.client_socket:
            try:
                readable, _, _ = select.select([self.client_socket], [], [], 0)
                if readable:
                    message = self.client_socket.recv(4096).decode()
                    self.add_message(message)
            except ConnectionResetError:
                self.add_message('Você foi desconectado do chat.')
                self.on_close()
        if self.running:
            self.root.after(1000, self.update_chat)

    def handle_enter(self, event):
        self.send_message()

    def on_close(self):
        self.running = False
        if self.client_socket:
            self.client_socket.close()
        self.root.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    chat_ui = ChatUI()
    chat_ui.run()
