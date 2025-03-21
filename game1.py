import requests

# 棋盘设置
BOARD_SIZE = 19

# 打印棋盘
def print_board(board_state):
    print("  ", end="")
    for i in range(BOARD_SIZE):
        print(f"{i:2d}", end="")
    print()
    for i in range(BOARD_SIZE):
        print(f"{i:2d}", end="")
        for j in range(BOARD_SIZE):
            if board_state[i][j] == 0:
                print(" ·", end="")
            elif board_state[i][j] == 1:
                print(" ●", end="")
            else:
                print(" ○", end="")
        print()

# 与Ollama模型交互
def get_move(model, board_state):
    url = "http://localhost:11434/api/generate"
    board_str = ""
    for row in board_state:
        row_str = " ".join(map(str, row))
        board_str += row_str + "\n"
    data = {
        "model": model,
        "prompt": f"当前围棋棋盘状态（0表示空位，1表示黑子，2表示白子）：\n{board_str}请给出下一步落子位置（格式：x,y）",
        "stream": False
    }
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # 检查请求是否成功
        result = response.json()
        move = result["response"].strip()
        print(f"{model} 回复内容：{move}")  # 打印模型的完整回复
        try:
            x, y = map(int, move.split(','))
            return x, y
        except ValueError:
            print(f"模型返回的落子位置格式不正确，返回内容为：{move}")
            return None, None
    except requests.RequestException as e:
        print(f"网络请求出错：{e}，请求的 URL 是：{url}")
        return None, None
    except KeyError:
        print("API 返回的 JSON 数据结构异常，缺少 'response' 字段。")
        return None, None

# 主函数
def main():
    board_state = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    models = ["deepseek-r1:70b", "deepseek-r1:7b"]
    current_player = 0
    step = 1
    while True:
        print(f"第 {step} 步：")
        print_board(board_state)
        model = models[current_player]
        x, y = get_move(model, board_state)
        if x is not None and y is not None:
            if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and board_state[x][y] == 0:
                if current_player == 0:
                    board_state[x][y] = 1
                else:
                    board_state[x][y] = 2
                current_player = 1 - current_player
                step += 1
            else:
                print("该位置已有棋子或位置超出棋盘范围，请重新选择。")
        else:
            print("无法获取有效的落子位置，结束对弈。")
            break

if __name__ == "__main__":
    main()
