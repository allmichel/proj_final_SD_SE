import socket
import threading
import logging

def handle_client(client_socket, client_address, client_id, clients, nicknames, logger):
    nickname = nicknames[client_id]

    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            break

        if data.strip() == ":quit":
            break

        if data.strip() != "":
            logger.info('Cliente {} (nickname: {}) enviou: {}'.format(client_id, nickname, data))

            # Encaminhar a mensagem para o outro cliente
            if client_id == 1:
                receiver_id = 2
            else:
                receiver_id = 1

            try:
                receiver_socket = clients[receiver_id]
                message = '{}: {}'.format(nickname, data)  # Adiciona o nickname do remetente à mensagem
                receiver_socket.send(message.encode())
            except KeyError:
                logger.info('Cliente {} não encontrado. Mensagem não enviada.'.format(receiver_id))

    client_socket.close()
    logger.info('Conexão encerrada com: {}'.format(client_address))


def main():
    host = '0.0.0.0'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(2)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Manipulador para o arquivo de log
    file_handler = logging.FileHandler('server.log')
    file_handler.setLevel(logging.INFO)

    # Manipulador para o console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter('[%(asctime)s] %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.info('Aguardando conexões...')

    clients = {}
    nicknames = {}

    while len(clients) < 2:
        client_socket, client_address = server_socket.accept()
        logger.info('Conexão estabelecida com: {}'.format(client_address))

        client_id = len(clients) + 1

        nickname = client_socket.recv(1024).decode()
        nicknames[client_id] = nickname.strip()

        clients[client_id] = client_socket

        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address, client_id, clients, nicknames, logger))
        client_thread.start()

    server_socket.close()

if __name__ == '__main__':
    main()
