import socket
import threading

# 서버 설정
HOST = '127.0.0.1'
PORT = 12345

# 클라이언트 관리를 위한 리스트
clients = []

# 락 객체 생성
lock = threading.Lock()

def handle_client(client_socket, address):
    with lock:
        print(f"[+] 연결됨: {address[0]}:{address[1]}")

    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break

            with lock:
                print(f"수신된 데이터 ({address[0]}:{address[1]}): {data.decode('utf-8')}")

    except Exception as e:
        print(f"에러 발생: {e}")

    finally:
        with lock:
            print(f"[-] 연결 종료: {address[0]}:{address[1]}")
            clients.remove(client_socket)
            client_socket.close()

def client_accept():
    while True:
        client_socket, address = server_socket.accept()
        clients.append(client_socket)

        # 새로운 클라이언트를 위한 스레드 시작
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
        client_thread.start()

def broadcast_message(message):
    with lock:
        print(f"서버에서 메시지: {message}")
        for client in clients:
            try:
                client.send(message.encode('utf-8'))
            except Exception as e:
                print(f"에러 발생: {e}")
                clients.remove(client)

def main():
    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    print(f"[*] 서버 리스닝 중: {HOST}:{PORT}")

    # 클라이언트 연결을 처리하는 스레드 시작
    accept_thread = threading.Thread(target=client_accept)
    accept_thread.start()

    try:
        while True:
            # 서버에서 메시지를 입력하면 모든 클라이언트에게 브로드캐스트
            server_message = input("서버에서 전송할 메시지를 입력하세요: ")
            broadcast_message(server_message)

    except KeyboardInterrupt:
        print("\n서버를 종료합니다.")

    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
