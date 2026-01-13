import pygame
import numpy as np
from stable_baselines3 import PPO
from pong_Env import PingPongEnv

# Setup
pygame.init()
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong Agent")
clock = pygame.time.Clock()

# Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,50,50)   # AI Paddle
BLUE = (50,50,255)  # Player Paddle

# Load the Environment and Model
env = PingPongEnv()
env.enemy_mode = "human"
obs, _ = env.reset()

try:
    model = PPO.load("pong_champion_final")
    print("AI Model Loaded Successfully")
except:
    print("Model not found")
    exit()

# The GAME Loop
running = True
while running:
    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    action, _ = model.predict(obs)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        env.p2_y -= env.paddle_speed
    if keys[pygame.K_DOWN]:
        env.p2_y += env.paddle_speed

    # Clamp Human to screen
    env.p2_y = max(env.paddle_h/2, min(env.height - env.paddle_h/2, env.p2_y))

    obs, reward, terminated, truncated, info = env.step(action)

    if terminated:
        obs, _ = env.reset()

    screen.fill(BLACK)

    # Draw AI Paddle (Left)
    ai_rect = pygame.Rect(0, env.p1_y - env.paddle_h/2, env.paddle_w, env.paddle_h)
    pygame.draw.rect(screen, RED, ai_rect)
    
    # Draw Human Paddle (Right)
    human_rect = pygame.Rect(WIDTH - env.paddle_w, env.p2_y - env.paddle_h/2, env.paddle_w, env.paddle_h)
    pygame.draw.rect(screen, BLUE, human_rect)
    
    # Draw Ball
    pygame.draw.circle(screen, WHITE, (int(env.ball_x), int(env.ball_y)), 10)
    
    # Draw Center Line
    pygame.draw.aaline(screen, WHITE, (WIDTH/2, 0), (WIDTH/2, HEIGHT))

    pygame.display.flip()
    clock.tick(60) # Limit to 60 FPS

pygame.quit()