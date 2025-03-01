import pygame
import sys
from constants import *
from game_objects import Snake, Food

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('贪吃蛇')
        self.clock = pygame.time.Clock()
        
        # 使用系统默认中文字体
        try:
            self.font = pygame.font.Font('/System/Library/Fonts/PingFang.ttc', 36)
        except:
            # 如果找不到 PingFang 字体，尝试其他中文字体
            try:
                self.font = pygame.font.Font('/System/Library/Fonts/STHeiti Light.ttc', 36)
            except:
                # 如果都找不到，使用系统默认字体
                self.font = pygame.font.SysFont('arial', 36)
        
        self.reset_game()

    def reset_game(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.game_over = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                else:
                    if event.key == pygame.K_UP and self.snake.direction != DOWN:
                        self.snake.direction = UP
                    elif event.key == pygame.K_DOWN and self.snake.direction != UP:
                        self.snake.direction = DOWN
                    elif event.key == pygame.K_LEFT and self.snake.direction != RIGHT:
                        self.snake.direction = LEFT
                    elif event.key == pygame.K_RIGHT and self.snake.direction != LEFT:
                        self.snake.direction = RIGHT
        return True

    def update(self):
        if not self.game_over:
            if not self.snake.update():
                self.game_over = True
            # 在 update 方法中找到食物生成的部分，修改为：
            elif self.snake.get_head_position() == self.food.position:
                self.snake.length += 1
                self.score += 10
                self.food.randomize_position(self.snake.positions)

    def render(self):
        self.screen.fill(BLACK)
        self.snake.render(self.screen)
        self.food.render(self.screen)
        
        # 显示分数
        score_text = self.font.render(f'分数: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        if self.game_over:
            game_over_text = self.font.render('游戏结束! 按空格键重新开始', True, WHITE)
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
            self.screen.blit(game_over_text, text_rect)
        
        pygame.display.update()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.render()
            self.clock.tick(SNAKE_SPEED)
        
        pygame.quit()