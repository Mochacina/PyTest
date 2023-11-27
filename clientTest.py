import tkinter as tk
from tkinter import ttk
import socket
import threading

class ClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Socket Client")

        # 서버 IP와 포트 입력
        self.server_ip_label = ttk.Label(root, text="서버 IP:")
        self.server_ip_label.grid(row=0, column=0, sticky=tk.W)
        self.server_ip_entry = ttk.Entry(root)
        self.server_ip_entry.grid(row=0, column=1, pady=5)

        self.port_label = ttk.Label(root, text="포트:")
        self.port_label.grid(row=1, column=0, sticky=tk.W)
        self.port_entry = ttk.Entry(root)
        self.port_entry.grid(row=1, column=1, pady=5)

        # 연결/연결 해제 버튼
        self.connect_button = ttk.Button(root, text="연결", command=self.toggle_connection)
        self.connect_button.grid(row=2, column=0, columnspan=2, pady=10)

        # 데이터 입력란
        self.input_text_label = ttk.Label(root, text="데이터 입력:")
        self.input_text_label.grid(row=3, column=0, sticky=tk.W)
        self.input_text_entry = ttk.Entry(root)
        self.input_text_entry.grid(row=3, column=1, pady=5)

        # 데이터 전송 버튼
        self.send_button = ttk.Button(root, text="데이터 전송", command=self.send_data, state=tk.DISABLED)
        self.send_button.grid(row=4, column=0, columnspan=2, pady=10)

        # 소켓 관련 변수 초기화
        self.server_ip = ""
        self.port = 0
        self.client_socket = None
        self.connected = False

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
            self.client_socket.connect((self.server_ip, self.port))
            self.connected = True
            self.connect_button.config(text="연결 해제")
            self.send_button.config(state=tk.NORMAL)
        except Exception as e:
            print(f"연결 오류: {e}")

    def disconnect(self):
        if self.client_socket:
            self.client_socket.close()
        self.connected = False
        self.connect_button.config(text="연결")
        self.send_button.config(state=tk.DISABLED)

    def send_data(self):
        data = self.input_text_entry.get()
        try:
            self.client_socket.send(data.encode())
        except Exception as e:
            print(f"데이터 전송 오류: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    root.config(padx=20,pady=10)
    app = ClientApp(root)
    root.mainloop()