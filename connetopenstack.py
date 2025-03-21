import requests
import json

# GPUSTACK连接信息
API_KEY = "gpustack_8d5638345a994cc8_f9947ebbf37ae045ca55d89f3e7bfc29"
API_BASE = "http://172.16.155.61/v1-openai"
# 构建请求头
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

# 定义对话函数
def generate_response(prompt):
    # 修改为正确的端点
    url = f"{API_BASE}/new-chat"
    data = {
        "model": "gwen2.5-7b",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        result = response.json()
        # 提取回复内容
        message = result["choices"][0]["message"]["content"]
        return message
    except requests.exceptions.RequestException as e:
        print(f"请求出错: {e}")
    except (KeyError, IndexError) as e:
        print(f"解析响应出错: {e}")
    return None

# 进行对话
if __name__ == "__main__":
    while True:
        user_input = input("你: ")
        if user_input.lower() in ['退出', 'quit', 'exit']:
            break
        response = generate_response(user_input)
        if response:
            print(f"GPUSTACK: {response}")
