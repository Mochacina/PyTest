import requests

def get_request(url):
    # GET ��û ������
    response = requests.get(url)
    print("GET Response:")
    print(response.text)

def post_request(url, data):
    # POST ��û ������ (JSON ������ ���� ����)
    payload = {"key1": "value1", "key2": "value2"}
    response = requests.post(url, json=payload)
    print("\nPOST Response:")
    print(response.text)

if __name__ == "__main__":
    while 1:
        types = ["get","post"]
        
        url = input("Request URL�� �Է��Ͻʽÿ�: ")
        type = input("Request Type�� �Է��Ͻʽÿ�(get/post): ")
        count = int(input("�ݺ� Ƚ���� �Է��Ͻʽÿ�: "))
        
        if not type in types:
            print("�ùٸ��� ���� Request Type�� �Է��߽��ϴ�.")
        
    
    