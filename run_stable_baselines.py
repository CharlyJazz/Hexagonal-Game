"""
Script to run Stable-Baselines3 approach
Execute this from the root directory: python run_stable_baselines.py
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'rl_approaches'))

from rl_approaches.stable_baselines_approach import StableBaselinesTrainer

def main():
    print("🚀 Starting Stable-Baselines3 Training - TURBO MODE")
    print("=" * 50)
    print("⚡ Modo rápido CON ventana visible")
    print("   - Sin límite de FPS (máxima velocidad)")
    print("   - Verás el juego corriendo súper rápido")
    print("=" * 50)
    
    # Create trainer
    trainer = StableBaselinesTrainer(algorithm='PPO')
    
    print("📦 Setting up TURBO environment (with window)...")
    # TURBO=True, HEADLESS=False = Ventana visible pero súper rápido
    trainer.setup_environment(n_envs=1, turbo=True, headless=False)
    
    print("🧠 Creating PPO model...")
    trainer.create_model(
        learning_rate=3e-4,
        n_steps=2048,
        batch_size=64,
        verbose=1
    )
    
    print("🎯 Starting TURBO training (you'll see it running fast)...")
    trainer.train(total_timesteps=10000000)  # Extended training
    
    print("📊 Evaluating model...")
    results = trainer.evaluate(n_episodes=5)
    
    print("\n🎉 Training Complete!")
    print(f"Results: {results}")

if __name__ == "__main__":
    main()
