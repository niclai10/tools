import requests

# 定义与 Ollama 模型交互的函数
def get_response(model, prompt):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        result = response.json()
        return result["response"].strip()
    except requests.RequestException as e:
        print(f"网络请求出错：{e}")
        return None
    except KeyError:
        print("API 返回的 JSON 数据结构异常，缺少 'response' 字段。")
        return None

# 主函数，实现两个模型的对话
def main():
    models = ["deepseek-r1:1.5b", "qwen2.5:1.5b"]

    # 让用户输入初始化问题
    initial_prompt = input("请输入初始化问题：")

    # 让用户输入对话轮数
    while True:
        try:
            num_turns = int(input("请输入对话轮数："))
            break
        except ValueError:
            print("输入无效，请输入一个整数。")

    current_prompt = initial_prompt
    current_speaker = 0

    # 打开日志文件以追加模式写入
    with open('log.txt', 'a', encoding='utf-8') as log_file:
        log_entry = f"{models[current_speaker]} 发起对话：{current_prompt}\n"
        print(log_entry.strip())
        log_file.write(log_entry)

        for _ in range(num_turns):
            current_model = models[current_speaker]
            response = get_response(current_model, current_prompt)
            if response:
                log_entry = f"{current_model} 回复：{response}\n"
                print(log_entry.strip())
                log_file.write(log_entry)
                # 将对方的回复作为下一轮的输入
                current_prompt = response
                # 切换发言模型
                current_speaker = 1 - current_speaker
            else:
                log_entry = "无法获取有效的回复，对话结束。\n"
                print(log_entry.strip())
                log_file.write(log_entry)
                break

if __name__ == "__main__":
    main()
