import requests
import json

def get_request(url):
    # GET 요청 보내기
    response = requests.get(url)
    print("GET Response:")
    print(response.text)

def post_request(url, data):
    # POST 요청 보내기 (JSON 데이터 전송 예제)
    response = requests.post(url, json=data) # payload = {key1: value1, key2: value2}
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
            continue
        
        if type == "post":
            json_string = input("Post Type 요청의 data를 입력하십시오:\n")
            json_data = json.loads(json_string)
        
        for _ in range(count):
            if type == "get": get_request(url)
            if type == "post": post_request(url,json_data)
            
        exit()
        
# http://httpbin.org/post
