import base64

byte_array = b'\x41\xD3\x1D\xD8\x65\xC0\x3E\x31\xD6\x8D\x2E\xD1\xA4\xEF\xCB\x33'

# Base64 ���ڵ�
base64_encoded = base64.b64encode(byte_array)
# ��� ���
print(base64_encoded.decode('utf-8'))