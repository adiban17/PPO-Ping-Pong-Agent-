# import required libraries
import random
from numpy.random import rand
import gymnasium as gym
from gymnasium import spaces
import numpy as np

class PingPongEnv(gym.Env):
    def __init__(self):
        # define action, observation space
        
        super(PingPongEnv, self).__init__()

        # define the arena
        self.width = 800
        self.height = 400
        self.paddle_h = 80
        self.paddle_w = 20
        self.paddle_speed = 10  # pixels per frame
        self.max_ball_speed = 10

        self.enemy_mode = "computer"
        self.opponent_error_rate = 0.10

        self.action_space = spaces.Discrete(3)  # spaces.Discrete(3) ---> tells the agent that we have 3 controls
        self.observation_space = spaces.Box(    # spaces.Box() ---> used for continuous numbers
            low = -1.0,
            high = 2.0,
            shape = (6,),
            dtype = np.float32
        )

        self.state = None   # internal state (not normalized)


    def reset(self, seed = None):
        # reset the universe
        # return observation, info
        
        super().reset(seed=seed)

        # 1. Spawn paddles at random Y positions
        # 2. Spawn ball in center with random Y and random Velocity

        self.ball_x = self.width/2
        self.ball_y = self.height/2
        self.ball_vx = np.random.randint(1,2)*5*random.choice([1,-1])
        self.ball_vy = np.random.randint(1,2)* random.choice([1,-1])

        self.p1_y = self.height/2
        self.p2_y = self.height/2

        return self._get_obs(),{}

    def step(self, action):
        # 1. Update the physics
        # 2. Calculate Reward
        # 3. Check Termination
        # Return obs, reward, terminated, truncated, info
        
        # MOVE AGENT
        if action == 1:     # moves Up
            self.p1_y = max(self.p1_y - self.paddle_speed, self.paddle_h/2)
        elif action == 2:   # moves Down
            self.p1_y = min(self.p1_y + self.paddle_speed, self.height - self.paddle_h/2)
        
        # MOVE OPPONENT
        if self.enemy_mode == "computer":
            if random.random() > self.opponent_error_rate:
                if self.p2_y < self.ball_y:
                    self.p2_y += self.paddle_speed
                elif self.p2_y > self.ball_y:
                    self.p2_y -= self.paddle_speed

        # MOVE BALL
        self.ball_x += self.ball_vx
        self.ball_y += self.ball_vy

        # PHYSICS CHECKS
        if self.ball_y <=0 or self.ball_y >= self.height:
            self.ball_vy *= -1

        # Paddle Collision
        # Check if the ball crossed the left paddle (Agent)
        if self.ball_x <= self.paddle_w and abs(self.ball_y - self.p1_y) < self.paddle_h/2:
            self.ball_vx *= -1      # bounce
            # skill logic
            if abs(self.ball_y-self.p1_y)<1.0:   # ball hits center of padel
                self.ball_vx = min(self.max_ball_speed, self.ball_vx+5)
                self.ball_vy = 0
            elif abs(self.ball_y - self.p1_y) <= (self.paddle_h)/4:   # ball hits near the center area of the padel (H/4)
                self.ball_vx += min(self.max_ball_speed, self.ball_vx+2)
                self.ball_vy += min(self.max_ball_speed, self.ball_vy+2)
            else:   # ball hits edge of the padel
                self.ball_vx = max(1,self.ball_vx-3)
                self.ball_vy += 5 

        # Check if ball crossed the right paddle (Opponent)
        if self.ball_x >= self.width - self.paddle_w and abs(self.ball_y - self.p2_y) < self.paddle_h/2:
            self.ball_vx *= -1

        # Reward and Termination
        reward = 0.001  # small reward for survival
        terminated = False

        # Win Condition (Passes Opponent)
        if self.ball_x > self.width:
            reward = 1.0
            terminated = True
        
        # Lose Condition (Passes Agent)
        if self.ball_x <= 0:
            reward = -1.0
            terminated = True

        return self._get_obs(), reward, terminated, False, {}

    def _get_obs(self):
        # Normalize inputs to 0-1 range
        return np.array([
            self.ball_x / self.width,
            self.ball_y / self.height,
            self.ball_vx / self.max_ball_speed,
            self.ball_vy / self.max_ball_speed,
            self.p1_y / self.height,
            self.p2_y / self.height
        ], dtype=np.float32)

    def render(self):
        # visulaization logic
        pass