"""
OpenAI Gym-style environment wrapper for Kuhn Poker
"""

from typing import Tuple, Dict, Any, Optional
import numpy as np
from .game import KuhnPoker, Action


class KuhnPokerEnv:
    """
    Gym-style environment for Kuhn Poker.
    This allows agents to interact with the game in a standardized way.
    """
    
    def __init__(self):
        self.game = KuhnPoker()
        self.num_actions = 2  # PASS, BET
        self.num_cards = 3    # J, Q, K
    
    def reset(self) -> Dict[str, Any]:
        """
        Reset environment and return initial observation.
        
        Returns:
            obs: Dictionary with observation info
                - 'cards': tuple of (card_p0, card_p1)
                - 'current_player': player to act
                - 'history': action history list
                - 'info_set_p0': info set for player 0
                - 'info_set_p1': info set for player 1
        """
        cards = self.game.reset()
        
        obs = {
            'cards': cards,
            'current_player': self.game.get_current_player(),
            'history': self.game.history.copy(),
            'info_set_p0': self.game.get_info_set(0),
            'info_set_p1': self.game.get_info_set(1),
            'valid_actions': self.game.get_valid_actions()
        }
        return obs
    
    def step(self, action: int) -> Tuple[Dict[str, Any], Optional[np.ndarray], bool, Dict[str, Any]]:
        """
        Take action in environment.
        
        Args:
            action: Action to take (0=PASS, 1=BET)
        
        Returns:
            obs: Updated observation dictionary
            rewards: Array [reward_p0, reward_p1] if terminal, else None
            done: Whether episode is finished
            info: Additional info dictionary
        """
        is_terminal, payoffs = self.game.step(action)
        
        obs = {
            'cards': tuple(self.game.cards),
            'current_player': self.game.get_current_player() if not is_terminal else None,
            'history': self.game.history.copy(),
            'info_set_p0': self.game.get_info_set(0),
            'info_set_p1': self.game.get_info_set(1),
            'valid_actions': self.game.get_valid_actions()
        }
        
        rewards = np.array(payoffs) if payoffs else None
        
        info = {
            'terminal': is_terminal,
            'history_str': self.game.get_history_str()
        }
        
        return obs, rewards, is_terminal, info
    
    def render(self, mode='human'):
        """Display current game state"""
        if mode == 'human':
            print(f"Cards: P0={KuhnPoker.card_to_str(self.game.cards[0])}, "
                  f"P1={KuhnPoker.card_to_str(self.game.cards[1])}")
            print(f"History: {self.game.get_history_str()}")
            print(f"Pot: P0={self.game.pot[0]}, P1={self.game.pot[1]}")
            if self.game.is_terminal:
                print(f"Terminal. Payoffs: {self.game.payoff}")
            else:
                print(f"Current player: {self.game.current_player}")
    
    def get_observation(self, player: int) -> Dict[str, Any]:
        """
        Get observation from perspective of specific player.
        Player only sees their own card.
        """
        return {
            'card': self.game.cards[player],
            'history': self.game.history.copy(),
            'info_set': self.game.get_info_set(player),
            'valid_actions': self.game.get_valid_actions(),
            'is_current_player': self.game.current_player == player
        }
