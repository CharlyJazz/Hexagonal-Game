"""
Approach 1: Stable-Baselines3 Implementation
High-level, production-ready RL with minimal code
"""
import gymnasium as gym
from gymnasium import spaces
import numpy as np
from stable_baselines3 import PPO, SAC, DQN
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.callbacks import EvalCallback
from base_env import HexagonGameEnv

class StableBaselinesWrapper(gym.Env):
    """Gymnasium wrapper for Stable-Baselines3"""
    
    def __init__(self, headless=False, turbo=False):
        super().__init__()
        self.env = HexagonGameEnv(headless=headless, turbo=turbo)
        
        # Define action and observation spaces
        self.action_space = spaces.Discrete(3)  # 0=nothing, 1=left, 2=right
        self.observation_space = spaces.Box(
            low=-1.0, high=1.0, 
            shape=self.env.observation_space_shape, 
            dtype=np.float32
        )
    
    def reset(self, seed=None, options=None):
        if seed is not None:
            np.random.seed(seed)
        obs = self.env.reset()
        return obs, {}
    
    def step(self, action):
        return self.env.step(action)
    
    def render(self):
        return self.env.render()
    
    def close(self):
        self.env.close()

class StableBaselinesTrainer:
    """Trainer for multiple SB3 algorithms"""
    
    def __init__(self, algorithm='PPO'):
        self.algorithm = algorithm
        self.model = None
        self.env = None
        
    def setup_environment(self, n_envs=1, turbo=False, headless=False):
        """Setup vectorized environment
        
        Args:
            n_envs: Number of parallel environments
            turbo: Fast training mode (no rendering, no FPS limit)
            headless: No window but normal speed
        """
        self.turbo = turbo
        
        # If we want to see the window (not headless) and only 1 env, don't vectorize
        # because make_vec_env creates subprocesses that can't show windows
        if n_envs == 1 and not headless:
            from stable_baselines3.common.vec_env import DummyVecEnv
            self.env = DummyVecEnv([lambda: StableBaselinesWrapper(headless=False, turbo=turbo)])
        else:
            self.env = make_vec_env(
                StableBaselinesWrapper, 
                n_envs=n_envs,
                env_kwargs={'headless': headless or turbo, 'turbo': turbo}
            )
    
    def create_model(self, learning_rate=3e-4, n_steps=2048, batch_size=64, verbose=1, save_path="models/"):
        """Create the RL model or load from checkpoint"""
        import os
        
        # Check for existing best model
        model_path = f"{save_path}best_{self.algorithm.lower()}_model.zip"
        
        if os.path.exists(model_path):
            print(f"📁 Loading existing best {self.algorithm} model from {model_path}")
            if self.algorithm == 'PPO':
                self.model = PPO.load(model_path, env=self.env)
            elif self.algorithm == 'SAC':
                self.model = SAC.load(model_path, env=self.env)
            elif self.algorithm == 'DQN':
                self.model = DQN.load(model_path, env=self.env)
            else:
                raise ValueError(f"Algorithm {self.algorithm} not supported")
            
            # Update learning rate if specified
            if learning_rate != 3e-4:
                print(f"🔧 Updating learning rate to {learning_rate}")
                self.model.learning_rate = learning_rate
                
        else:
            print(f"🆕 Creating new {self.algorithm} model")
            default_kwargs = {
                'learning_rate': learning_rate,
                'verbose': verbose,
                'tensorboard_log': "./tensorboard_logs/"
            }
            
            if self.algorithm == 'PPO':
                default_kwargs.update({
                    'n_steps': n_steps,
                    'batch_size': batch_size,
                })
                self.model = PPO("MlpPolicy", self.env, **default_kwargs)
            elif self.algorithm == 'SAC':
                self.model = SAC("MlpPolicy", self.env, **default_kwargs)
            elif self.algorithm == 'DQN':
                self.model = DQN("MlpPolicy", self.env, **default_kwargs)
            else:
                raise ValueError(f"Algorithm {self.algorithm} not supported")
    
    def train(self, total_timesteps=100000, save_path="models/"):
        """Train the model"""
        # Setup evaluation callback
        eval_env = StableBaselinesWrapper(headless=True)
        eval_callback = EvalCallback(
            eval_env, 
            best_model_save_path=f"{save_path}best_{self.algorithm.lower()}_model",
            log_path=f"{save_path}logs/",
            eval_freq=10000,
            deterministic=True,
            render=False
        )
        
        # Train
        self.model.learn(
            total_timesteps=total_timesteps,
            callback=eval_callback,
            tb_log_name=f"{self.algorithm}_hexagon"
        )
        
        # Save final model
        self.model.save(f"{save_path}{self.algorithm.lower()}_final_model")
    
    def evaluate(self, n_episodes=10):
        """Evaluate trained model"""
        env = StableBaselinesWrapper(headless=False)
        
        episode_rewards = []
        episode_lengths = []
        
        for episode in range(n_episodes):
            obs, _ = env.reset()
            episode_reward = 0
            episode_length = 0
            done = False
            
            while not done:
                action, _ = self.model.predict(obs, deterministic=True)
                obs, reward, terminated, truncated, info = env.step(action)
                done = terminated or truncated
                episode_reward += reward
                episode_length += 1
                env.render()
            
            episode_rewards.append(episode_reward)
            episode_lengths.append(episode_length)
            print(f"Episode {episode + 1}: Reward = {episode_reward:.2f}, Length = {episode_length}")
        
        env.close()
        
        return {
            'mean_reward': np.mean(episode_rewards),
            'std_reward': np.std(episode_rewards),
            'mean_length': np.mean(episode_lengths),
            'std_length': np.std(episode_lengths)
        }
    
    def compare_algorithms(self, algorithms=['PPO', 'SAC', 'DQN'], timesteps=50000):
        """Compare multiple algorithms"""
        results = {}
        
        for algo in algorithms:
            print(f"\nTraining {algo}...")
            trainer = StableBaselinesTrainer(algorithm=algo)
            trainer.setup_environment()
            trainer.create_model()
            trainer.train(total_timesteps=timesteps)
            
            # Evaluate
            eval_results = trainer.evaluate(n_episodes=5)
            results[algo] = eval_results
            print(f"{algo} Results: {eval_results}")
        
        return results

# Usage example
if __name__ == "__main__":
    # Quick training example
    trainer = StableBaselinesTrainer(algorithm='PPO')
    trainer.setup_environment()
    trainer.create_model(learning_rate=4e-4)
    trainer.train(total_timesteps=10000000)
    
    # Evaluate
    results = trainer.evaluate()
    print(f"Final Results: {results}")
