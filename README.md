# 🏓 RL Pong Agent 

**An AI Agent trained using Proximal Policy Optimization (PPO) and Curriculum Learning.**

![Project Status](https://img.shields.io/badge/Status-Completed-success)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Library](https://img.shields.io/badge/Library-Stable--Baselines3-orange)
![Environment](https://img.shields.io/badge/Env-Gymnasium-green)

> **The Challenge:** Train an AI agent that plays Ping Pong using Reinforcement Learning from scratch and then deploy it for real-time play against a human.

---

## 📖 About The Project

This project implements a **Reinforcement Learning (RL)** agent capable of playing Pong at a basic level. Unlike standard tutorials that use pre-made environments, this project features a **custom-built Gymnasium environment** with physics-based mechanics (velocity, friction, collision angles).

The agent was trained using **Curriculum Learning**, a technique where the difficulty of the opponent gradually increases. This allowed the agent to overcome the "Sparse Reward" problem and learn complex strategies like corner shots and fast counters.

### Key Features
* **Custom Gymnasium Environment:** Built from scratch using Python & NumPy.
* **PPO Algorithm:** Utilizes Stable-Baselines3's Proximal Policy Optimization with a custom neural network architecture (256x256).
* **Curriculum Learning Pipeline:** Automated training stages moving from "Clumsy Opponent" (25% error rate) to "God Mode" (0% error rate).
* **Real-Time Inference:** A Pygame interface to play against the trained agent in real-time at 60 FPS.
* **Domain Randomization:** The agent is trained to handle random ball velocities and serving angles to prevent overfitting.

---

## 🛠️ Technical Architecture

### The Brain (Neural Network)
* **Algorithm:** PPO (Proximal Policy Optimization)
* **Policy:** MLP (Multi-Layer Perceptron)
* **Architecture:** 2 Hidden Layers (256 neurons each)
* **Entropy Coefficient:** `0.01` (To force exploration and creative shots)
* **Observation Space:** 6-dimensional vector `[ball_x, ball_y, ball_vx, ball_vy, player_y, enemy_y]`

### The Training Curriculum
To prevent the agent from getting stuck in local minima (Lazy Strategy), training was split into 3 stages:
1.  **Rookie Stage:** Opponent has a **25% error rate**. The agent learns the basics of hitting the ball.
2.  **Pro Stage:** Opponent has a **10% error rate**. The agent learns to aim and rally.
3.  **Grandmaster Stage:** Opponent has a **0% error rate** (Perfect Wall). The agent must find mathematical exploits in the physics engine to score.

---

## 🚀 Installation

1.  **Clone the Repo**
    ```bash
    git clone https://github.com/adiban17/PPO-Ping-Pong-Agent-
    cd PPO-Ping-Pong-Agent-
    ```

2.  **Install Dependencies**
    ```bash
    pip install gymnasium stable-baselines3 shimmy pygame numpy
    ```

---

## 🎮 How to Run

### 1. Play Against the AI (Pre-Trained)
If you just want to test your skills against the agent:
```bash
python play.py
```

* **Controls:** Use `UP` and `DOWN` arrow keys.
* **Goal:** Try to play some basic ping-pong moves against the agent.

### 2. Train the AI from Scratch
To replicate the training process and generate your own model:
```bash
python train_curriculum.py
```

* *Note: Training takes approximately 30 minutes - 1 hour on a local device depending on system capabilities.*
* The script will save checkpoints (e.g., `pong_stage1.zip`) as it progresses.

---

## 📂 File Structure

```text
RL-Pong-Champion/
├── ping_pong_env.py        # The Custom Gymnasium Environment (Physics & Rules)
├── play.py                 # Pygame script for Human vs. AI interaction
├── train_curriculum.py     # The automated training pipeline (Stages 1-3)
├── pong_champion_final.zip # The trained model weights (The Brain)
└── README.md               # Documentation
```

## 🧠 Lessons Learned
* **Sparse Rewards:** Without a curriculum, the agent failed to learn because beating a perfect opponent instantly is impossible. Lowering the difficulty initially was crucial.
* **Entropy Matters:** Training without an entropy coefficient led to "Premature Convergence," where the agent found a lazy strategy (standing still) and refused to learn further.
* **Sim vs. Real:** A model trained purely on math needs a "Wrapper" (in `play.py`) to interface with human inputs effectively.

---

## 📜 License
Distributed under the MIT License. See `LICENSE` for more information.

---

### 👤 Author
**Aditya Banerjee**
* [LinkedIn](https://www.linkedin.com/in/aditya-banerjee-08117b310/)
* [GitHub](https://github.com/adiban17)
* [Medium](https://medium.com/@YOUR_MEDIUM_USERNAME)
