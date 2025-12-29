"""
Base environment wrapper for the Hexagonal Game
Compatible with all RL approaches
"""
import numpy as np
import pygame
from typing import Tuple, Dict, Any
from superhexagon.surface import GameSurface
from superhexagon.settings import *

class HexagonGameEnv:
    """Base environment for the hexagonal game"""
    
    def __init__(self, headless=False, turbo=False):
        """
        Args:
            headless: No window display
            turbo: Fast training mode (no FPS limit, but can still show window)
        """
        self.turbo = turbo
        self.headless = headless
        
        if headless:
            # Set dummy video driver BEFORE pygame.init()
            import os
            os.environ['SDL_VIDEODRIVER'] = 'dummy'
        
        pygame.init()
        
        if not headless:
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
            caption = 'Hexagon RL Training - TURBO MODE' if turbo else 'Hexagon RL Training'
            pygame.display.set_caption(caption)
        else:
            # Use dummy display for headless mode
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
            
        self.clock = pygame.time.Clock()
        
        # Fixed deltatime for turbo mode (simulates ~60 FPS)
        self.fixed_dt = 1.0 / 60.0
        
        # Cache for obstacle distances
        self._cached_distances = [1.0] * 6
        self._cache_valid = False
        
        self.reset()
        
        # Action space: 0=nothing, 1=left, 2=right
        self.action_space_n = 3
        
        # State space dimensions
        self.observation_space_shape = (8,)  # [player_angle, player_vel, 6 obstacle distances]
        
    def reset(self) -> np.ndarray:
        """Reset environment to initial state"""
        self.game = GameSurface(self.screen)
        self.total_reward = 0
        self.steps = 0
        self.max_steps = 10000
        
        # Game variables from original main.py
        self.expansion_value = 0
        self.expansion_sign = 1
        self.variable = 0
        self.orientation = 1
        self.angle_per_orientation = 35
        
        # Set up pygame timers like in original
        pygame.time.set_timer(MOVING, 1000)
        pygame.time.set_timer(EXPANSION, 75)
        
        return self._get_state()
    
    def step(self, action: int) -> Tuple[np.ndarray, float, bool, bool, Dict]:
        """Execute one step in the environment"""
        self.steps += 1
        
        # Apply action
        if action == 1:  # Left
            self.game.move_left(ARROW_SPEED)
            self.game.move_right(0)
        elif action == 2:  # Right
            self.game.move_right(ARROW_SPEED)
            self.game.move_left(0)
        else:  # No action
            self.game.move_left(0)
            self.game.move_right(0)
        
        # Update game state
        if self.turbo:
            # TURBO MODE: Fixed deltatime, no FPS limit
            deltatime = self.fixed_dt
        else:
            deltatime = self.clock.tick(60) / 1000
        
        self.variable += self.orientation * (self.angle_per_orientation * deltatime)
        self.game.set_rotation(self.variable)
        self.game.set_expantion(self.expansion_value)
        
        # Handle pygame events (simplified in turbo mode)
        if self.turbo:
            # Simulate events deterministically for speed
            if self.steps % 5 == 0:  # Every 5 steps, update expansion
                self.expansion_value = self.expansion_sign + self.expansion_value
                if self.expansion_sign == 1 and self.expansion_value >= 10:
                    self.expansion_sign = -1    
                if self.expansion_sign == -1 and self.expansion_value <= 0:
                    self.expansion_sign = 1
            if self.steps % 60 == 0:  # Every ~1 second, maybe change orientation
                import random
                if bool(random.getrandbits(1)):
                    self.orientation = self.orientation * -1
                    self.angle_per_orientation = random.choice(ANGLES_PER_DELTATIME)
            # Clear event queue to prevent buildup
            pygame.event.clear()
        else:
            for event in pygame.event.get():
                if event.type == EXPANSION:
                    self.expansion_value = self.expansion_sign + self.expansion_value
                    if self.expansion_sign == 1 and self.expansion_value >= 10:
                        self.expansion_sign = -1    
                    if self.expansion_sign == -1 and self.expansion_value <= 0:
                        self.expansion_sign = 1
                elif event.type == MOVING:
                    import random
                    if bool(random.getrandbits(1)):
                        self.orientation = self.orientation * -1
                        self.angle_per_orientation = random.choice(ANGLES_PER_DELTATIME)
        
        # Invalidate distance cache
        self._cache_valid = False
        
        # Clear screen BEFORE updating game (so game draws on clean canvas)
        if not self.headless:
            self.screen.fill((0, 0, 0))
        
        # Update game (this draws everything)
        self.game.deltatime = deltatime
        self.game.update()
        
        # Display update for visual mode
        if not self.headless:
            pygame.display.update()
        
        # Calculate reward
        reward = self._calculate_reward()
        self.total_reward += reward
        
        # Check if done (Gymnasium API: terminated, truncated)
        terminated = self.game.game_over  # Game ended due to collision
        truncated = self.steps >= self.max_steps  # Episode truncated due to time limit
        
        # Get next state
        next_state = self._get_state()
        
        info = {
            'total_reward': self.total_reward,
            'steps': self.steps,
            'game_over': self.game.game_over
        }
        
        return next_state, reward, terminated, truncated, info
    
    def _get_state(self) -> np.ndarray:
        """Get current state representation"""
        # Player angle (normalized)
        player_angle = self.game.player.angle / (2 * np.pi)
        
        # Player velocity (approximated)
        player_vel = (self.game.left - self.game.right) / ARROW_SPEED
        
        # Obstacle distances in 6 directions (simplified)
        obstacle_distances = self._get_obstacle_distances()
        
        state = np.array([player_angle, player_vel] + obstacle_distances, dtype=np.float32)
        return state
    
    def _get_obstacle_distances(self) -> list:
        """Get distances to nearest obstacles in 6 hexagonal directions"""
        # Use cache if valid (turbo mode optimization)
        if self._cache_valid:
            return self._cached_distances
        
        # Get player position
        player_x = self.game.player.rect.centerx
        player_y = self.game.player.rect.centery
        
        # Use spawner progress directly instead of drawing trapezoids
        # This avoids expensive polygon creation
        distances = []
        angles_names = ["top", "top_right", "bottom_right", "bottom", "bottom_left", "top_left"]
        
        for angle_name in angles_names:
            min_distance = 1.0
            
            for pattern in self.game.spawner.progress:
                if angle_name in pattern:
                    # Get progress value (distance from center)
                    progress_y = pattern[angle_name]["y"]
                    # Normalize: LIMIT_PROGRESS is max, 0 is at center
                    normalized = 1.0 - (progress_y / LIMIT_PROGRESS) if LIMIT_PROGRESS > 0 else 1.0
                    normalized = max(0.0, min(1.0, normalized))
                    min_distance = min(min_distance, normalized)
            
            distances.append(min_distance)
        
        # Cache result
        self._cached_distances = distances
        self._cache_valid = True
        
        return distances
    
    def _calculate_reward(self) -> float:
        """Calculate reward for current step"""
        if self.game.game_over:
            return -100.0  # Large penalty for collision
        
        # Small positive reward for survival
        survival_reward = 1.0
        
        # TODO: For version 2 - Actually check if player is near center before giving bonus
        # Should verify: player_distance = self.game.player.r + self.game.player.pump
        center_bonus = 0.1
        
        return survival_reward + center_bonus
    
    def render(self):
        """Render the game (if not headless)"""
        # Rendering is now handled in step() method
        return None
    
    def close(self):
        """Close the environment"""
        pygame.quit()
