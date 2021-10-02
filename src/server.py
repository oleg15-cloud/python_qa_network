import socket
from http import HTTPStatus

PORT = 2100
FORMAT = "utf-8"
HOST = socket.gethostbyname(socket.gethostname())

with socket.create_server((HOST, PORT)) as server:
    print(f"[STARTING] Server is starting on {HOST}:{PORT}")
    server.listen()

    while True:
        conn, address = server.accept()
        data = conn.recv(1024).decode(FORMAT).strip()

        for status in HTTPStatus:
            if f"status={status.value}" in data.split()[1]:
                status_value = status.value
                status_phrase = status.phrase
                break
            else:
                status_value = HTTPStatus.OK
                status_phrase = HTTPStatus(HTTPStatus.OK).phrase

        response_headers = \
            f"{data.split()[2]} {status_value} {status_phrase}" \
            f"\r\nContent-Type: text/html; charset=utf-8\r\n\r\n".encode(FORMAT)
        conn.send(response_headers + f"Request Method: {data.split()[0]}"
                                     f"\r\nRequest Source: ({HOST},{PORT})"
                                     f"\r\nResponse Status: {status_value} {status_phrase}"
                                     f"\r\n{data[4:]}".encode(FORMAT))
        conn.close()
