import socket
import argparse

from urllib.parse import urlparse, parse_qs
from http import HTTPStatus


def handle_request(request, client_address):
    # Разбиваем запрос на строки
    lines = request.splitlines()

    # Получаем первую строку (метод и путь)
    request_line = lines[0]
    method, path, _ = request_line.split()

    # Извлекаем параметры из URL
    parsed_url = urlparse(path)
    query_params = parse_qs(parsed_url.query)

    # Получаем статус из параметров запроса
    status_code = query_params.get('status', ['200'])[0]
    try:
        status = HTTPStatus(int(status_code))
    except ValueError:
        status = HTTPStatus(500)

    # Формируем ответ
    response_status = f"{status.value} {status.phrase}"

    # Заголовки запроса
    headers = "\n".join(lines[1:])  # Все строки после первой

    # Формируем тело ответа
    response_body = (
        f"Request Method: {method}\n"
        f"Request Source: {client_address}\n"
        f"Response Status: {response_status}\n"
        f"{headers}"
    )

    # Формируем полный HTTP-ответ
    response = (
        f"HTTP/1.1 {response_status}\r\n"
        f"Content-Type: text/plain\r\n"
        f"Content-Length: {len(response_body)}\r\n"
        f"\r\n"
        f"{response_body}"
    )

    return response

def write_config(host, port):
    with open('.env','w',encoding='utf-8') as config:
        config.write(
            f'HOST={host}\n'
            f'PORT={port}'
        )

def run_server(host='127.0.0.1', port=8080):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Сервер запущен на http://{host}:{port}")

        while True:
            client_socket, client_address = server_socket.accept()
            with client_socket:
                print(f"Подключение от {client_address}")
                request = client_socket.recv(1024).decode('utf-8')
                print("Полученный запрос:\n", request)

                response = handle_request(request, client_address)
                client_socket.sendall(response.encode('utf-8'))
                print("Ответ отправлен клиенту.\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=8080, help='Порт для запуска сервера (по умолчанию 8080)')
    parser.add_argument('-H', '--host', type=str, default='127.0.0.1', help='Хост для запуска сервера')
    args = parser.parse_args()
    write_config(host=args.host, port=args.port)
    run_server(host=args.host, port=args.port)


