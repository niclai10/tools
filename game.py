import requests
import pygame
import time

# 初始化pygame
pygame.init()

# 棋盘设置
BOARD_SIZE = 19
GRID_SIZE = 30
WINDOW_WIDTH = GRID_SIZE * (BOARD_SIZE + 1)
WINDOW_HEIGHT = GRID_SIZE * (BOARD_SIZE + 1)
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Go Game")

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BOARD_COLOR = (204, 153, 102)

# 绘制棋盘
def draw_board():
    screen.fill(BOARD_COLOR)
    for i in range(BOARD_SIZE):
        pygame.draw.line(screen, BLACK, (GRID_SIZE, GRID_SIZE * (i + 1)), (GRID_SIZE * BOARD_SIZE, GRID_SIZE * (i + 1)), 2)
        pygame.draw.line(screen, BLACK, (GRID_SIZE * (i + 1), GRID_SIZE), (GRID_SIZE * (i + 1), GRID_SIZE * BOARD_SIZE), 2)
    pygame.draw.rect(screen, BLACK, (GRID_SIZE, GRID_SIZE, GRID_SIZE * BOARD_SIZE, GRID_SIZE * BOARD_SIZE), 4)
    pygame.display.flip()

# 绘制棋子
def draw_stone(x, y, color):
    pos_x = GRID_SIZE * (x + 1)
    pos_y = GRID_SIZE * (y + 1)
    pygame.draw.circle(screen, color, (pos_x, pos_y), GRID_SIZE // 2 - 2)
    pygame.display.flip()

# 与Ollama模型交互
def get_move(model, board_state):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": model,
        "prompt": f"当前围棋棋盘状态：{board_state}，请给出下一步落子位置（格式：x,y）",
        "stream": False
    }
    response = requests.post(url, json=data)
    result = response.json()
    move = result["response"].strip()
    try:
        x, y = map(int, move.split(','))
        return x, y
    except ValueError:
        print("模型返回的落子位置格式不正确。")
        return None, None

# 主函数
def main():
    draw_board()
    board_state = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    models = ["deepseek-r1:70b", "deepseek-r1:7b"]
    current_player = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        model = models[current_player]
        x, y = get_move(model, board_state)
        if x is not None and y is not None:
            if board_state[x][y] == 0:
                if current_player == 0:
                    draw_stone(x, y, BLACK)
                    board_state[x][y] = 1
                else:
                    draw_stone(x, y, WHITE)
                    board_state[x][y] = 2
                current_player = 1 - current_player
            else:
                print("该位置已有棋子，请重新选择。")
        time.sleep(1)

if __name__ == "__main__":
    main()
