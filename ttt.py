import requests
import random

# 初始化棋盘
def init_board():
    return [' ' for _ in range(9)]

# 打印棋盘
def print_board(board):
    print(f"{board[0]}|{board[1]}|{board[2]}")
    print("-+-+-")
    print(f"{board[3]}|{board[4]}|{board[5]}")
    print("-+-+-")
    print(f"{board[6]}|{board[7]}|{board[8]}")

# 判断胜负
def check_winner(board, player):
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # 行
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # 列
        [0, 4, 8], [2, 4, 6]  # 对角线
    ]
    for combo in winning_combinations:
        if all(board[i] == player for i in combo):
            return True
    return False

# 检查平局
def is_full(board):
    return ' ' not in board

# 调用 Ollama 模型获取决策
def get_move(model, board):
    prompt = f"当前井字过三关棋盘状态：{board}。请给出你的落子位置（0-8）。"
    data = {
        "model": model,
        "prompt": prompt
    }
    response = requests.post("http://localhost:11434/api/generate", json=data)
    if response.status_code == 200:
        result = response.json()["response"]
        try:
            move = int(result.strip())
            if 0 <= move <= 8 and board[move] == ' ':
                return move
        except ValueError:
            pass
    # 如果模型返回无效结果，随机选择一个可用位置
    available_moves = [i for i, x in enumerate(board) if x == ' ']
    return random.choice(available_moves)

# 进行一场比赛
def play_game(model1, model2):
    board = init_board()
    players = [model1, model2]
    current_player = 0
    symbols = ['X', 'O']

    while True:
        model = players[current_player]
        symbol = symbols[current_player]
        move = get_move(model, board)
        board[move] = symbol

        if check_winner(board, symbol):
            return players[current_player]
        elif is_full(board):
            return None

        current_player = 1 - current_player

# 进行多场比赛并统计结果
def play_multiple_games(model1, model2, num_games):
    wins = {model1: 0, model2: 0, None: 0}
    for _ in range(num_games):
        winner = play_game(model1, model2)
        wins[winner] += 1

    print(f"比赛场数: {num_games}")
    print(f"{model1} 获胜次数: {wins[model1]}")
    print(f"{model2} 获胜次数: {wins[model2]}")
    print(f"平局次数: {wins[None]}")

if __name__ == "__main__":
    model1 = "deepseek-r1:1.5b"
    model2 = "qwen2.5:1.5b"
    num_games = 5  # 设置比赛场数
    play_multiple_games(model1, model2, num_games)
