import tkinter as tk
from tkinter import ttk, scrolledtext
import socket
import threading
import webbrowser

class ClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Socket Client")

        # 에러메세지용 라벨
        self.warning_label = ttk.Label(root, text="서버 IP와 포트를 입력하고 연결하세요", anchor="center")
        self.warning_label.grid(row=0, column=0, columnspan=2, pady=10, sticky=tk.W)

        # 서버 IP와 포트 입력
        self.server_ip_label = ttk.Label(root, text="서버 IP:")
        self.server_ip_label.grid(row=1, column=0, sticky=tk.W)
        self.server_ip_entry = ttk.Entry(root)
        self.server_ip_entry.grid(row=1, column=1, pady=5)

        self.port_label = ttk.Label(root, text="포트:")
        self.port_label.grid(row=2, column=0, sticky=tk.W)
        self.port_entry = ttk.Entry(root)
        self.port_entry.grid(row=2, column=1, pady=5)

        # 연결/연결 해제 버튼
        self.connect_button = ttk.Button(root, text="연결", command=self.toggle_connection)
        self.connect_button.grid(row=3, column=0, columnspan=2, pady=10)

        # 데이터 입력란
        self.input_text_label = ttk.Label(root, text="데이터 입력:")
        self.input_text_label.grid(row=4, column=0, sticky=tk.W)
        self.input_text_entry = ttk.Entry(root)
        self.input_text_entry.grid(row=4, column=1, pady=5)

        # 데이터 전송 버튼
        self.send_button = ttk.Button(root, text="데이터 전송", command=self.send_data, state=tk.DISABLED)
        self.send_button.grid(row=5, column=0, columnspan=2, pady=10)

        # 소켓 관련 변수 초기화
        self.server_ip = ""
        self.port = 0
        self.client_socket = None
        self.client_socket_timeout = 5
        self.connected = False
        self.new_window = None

    def toggle_connection(self):
        if self.connected:
            self.disconnect()
        else:
            self.connect()

    def connect(self):
        self.server_ip = self.server_ip_entry.get()
        self.port = int(self.port_entry.get())

        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.settimeout(self.client_socket_timeout)
            self.client_socket.connect((self.server_ip, self.port))
            self.connected = True
            self.connect_button.config(text="연결 해제")
            self.send_button.config(state=tk.NORMAL)
            
            # 새로운 창 생성
            self.create_new_window()
            
            # 새로운 창에 연결된 소켓을 전달
            # self.new_window.client_socket = self.client_socket

            # 서버로부터 수신한 데이터를 처리할 쓰레드 시작
            threading.Thread(target=self.receive_data).start()
        
        except socket.timeout as e:
            self.warning_label.config(text=f"연결 시간 초과: {e}")
            print(f"연결 시간 초과: {e}")
        
        except Exception as e:
            self.warning_label.config(text=f"연결 오류: {e}")
            print(f"연결 오류: {e}")

    def disconnect(self):
        if self.client_socket:
            self.client_socket.close()
        self.connected = False
        self.connect_button.config(text="연결")
        self.send_button.config(state=tk.DISABLED)
        self.close_new_window()

    def send_data(self):
        data = self.input_text_entry.get()
        try:
            if len(data)>0: self.client_socket.send(data.encode())
        except Exception as e:
            print(f"데이터 전송 오류: {e}")
            
    def receive_data(self):
        while self.connected:
            try:
                data = self.client_socket.recv(1024).decode()
                # 서버로부터 수신한 데이터를 새로운 창에 추가
                if data and self.new_window:
                    self.add_received_data(f"받은 데이터: {data}")
                elif not data:
                    self.disconnect()
                    return 0
            except TimeoutError as e: pass
            except Exception as e2:
                print(f"데이터 수신 오류: {e2}")
                pass
            
    def create_new_window(self):
        # 수신된 데이터를 표시할 새로운 창 생성
        self.new_window = tk.Toplevel(self.root)
        self.new_window.title("수신된 데이터")

        # scrolledtext 위젯 생성
        self.received_data_text = scrolledtext.ScrolledText(self.new_window, wrap=tk.WORD, width=40, height=10)
        self.received_data_text.pack(padx=10, pady=10)

        # 새로운 창이 닫힐 때 연결 해제
        self.new_window.protocol("WM_DELETE_WINDOW", self.on_new_window_close)

    def close_new_window(self):
        # 새로운 창이 닫힐 때 호출되는 함수
        if self.new_window:
            self.new_window.destroy()
            self.new_window = None

    def on_new_window_close(self):
        # 새로운 창이 닫힐 때 연결 해제
        self.disconnect()
        
    def add_received_data(self, data):
        # 수신된 데이터를 텍스트 위젯에 추가
        self.received_data_text.insert(tk.END, data + "\n")
        # 스크롤을 항상 가장 아래로 이동
        self.received_data_text.yview(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    root.config(padx=20,pady=10)
    app = ClientApp(root)
    root.mainloop()