import random
import pygame
from constants import *

class Snake:
    def __init__(self):
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN
        
        for i in range(self.length - 1):
            self.positions.append((self.positions[0][0], self.positions[0][1]))

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = ((cur[0] + x), (cur[1] + y))
        
        # 检查是否撞墙
        if (new[0] < 0 or new[0] >= GRID_WIDTH or 
            new[1] < 0 or new[1] >= GRID_HEIGHT):
            return False
            
        # 检查是否撞到自己
        if new in self.positions[2:]:
            return False
            
        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()
        return True

    def render(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, self.color, 
                           (p[0] * GRID_SIZE, p[1] * GRID_SIZE, 
                            GRID_SIZE - 2, GRID_SIZE - 2))

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self, snake_positions=None):
        # 默认为空列表，避免初始化时的问题
        if snake_positions is None:
            snake_positions = []
            
        # 生成所有可能的位置
        all_positions = [(x, y) for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT)]
        
        # 移除蛇身占据的位置
        available_positions = [pos for pos in all_positions if pos not in snake_positions]
        
        # 如果没有可用位置，使用任意位置（极端情况）
        if not available_positions:
            self.position = (random.randint(0, GRID_WIDTH - 1),
                            random.randint(0, GRID_HEIGHT - 1))
        else:
            # 从可用位置中随机选择
            self.position = random.choice(available_positions)

    def render(self, surface):
        pygame.draw.rect(surface, self.color,
                        (self.position[0] * GRID_SIZE, 
                         self.position[1] * GRID_SIZE,
                         GRID_SIZE - 2, GRID_SIZE - 2))