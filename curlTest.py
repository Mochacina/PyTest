import requests

def get_request(url):
    # GET 요청 보내기
    response = requests.get(url)
    print("GET Response:")
    print(response.text)

def post_request(url, data):
    # POST 요청 보내기 (JSON 데이터 전송 예제)
    payload = {"key1": "value1", "key2": "value2"}
    response = requests.post(url, json=payload)
    print("\nPOST Response:")
    print(response.text)

if __name__ == "__main__":
    while 1:
        types = ["get","post"]
        
        url = input("Request URL을 입력하십시오: ")
        type = input("Request Type을 입력하십시오(get/post): ")
        count = int(input("반복 횟수를 입력하십시오: "))
        
        if not type in types:
            print("올바르지 않은 Request Type을 입력했습니다.")
        
    
    