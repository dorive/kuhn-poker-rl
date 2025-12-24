"""
Kuhn Poker Game Rules Implementation

Kuhn Poker is a simplified poker game:
- 3 cards: Jack (0), Queen (1), King (2)
- 2 players, each antes 1 chip
- Each player gets 1 card
- Player 0 acts first
- Actions: Pass (0) or Bet (1)
- Betting costs 1 chip

Action sequences:
- Pass, Pass: Showdown
- Pass, Bet, Pass: Player 1 wins (fold)
- Pass, Bet, Bet: Showdown (pot = 4)
- Bet, Pass: Player 0 wins (fold)
- Bet, Bet: Showdown (pot = 4)
"""

import random
from typing import List, Tuple, Optional
from enum import IntEnum


class Action(IntEnum):
    PASS = 0
    BET = 1


class KuhnPoker:
    """
    Kuhn Poker game logic
    """
    
    CARDS = [0, 1, 2]  # Jack, Queen, King
    CARD_NAMES = ['J', 'Q', 'K']
    NUM_PLAYERS = 2
    ANTE = 1
    BET_SIZE = 1
    
    def __init__(self):
        self.reset()
    
    def reset(self) -> Tuple[int, int]:
        """
        Reset game and deal cards. Returns (card_p0, card_p1)
        """
        deck = self.CARDS.copy()
        random.shuffle(deck)
        self.cards = deck[:2]
        self.history = []
        self.current_player = 0
        self.pot = [self.ANTE, self.ANTE]
        self.is_terminal = False
        self.payoff = None
        return tuple(self.cards)
    
    def get_valid_actions(self) -> List[int]:
        """
        Returns list of valid actions
        """
        if self.is_terminal:
            return []
        return [Action.PASS, Action.BET]
    
    def step(self, action: int) -> Tuple[bool, Optional[List[int]]]:
        """
        Execute action. Returns (is_terminal, payoffs)
        payoffs is None if game continues, else [payoff_p0, payoff_p1]
        """
        if self.is_terminal:
            raise ValueError("Game is already terminal")
        
        if action not in [Action.PASS, Action.BET]:
            raise ValueError(f"Invalid action: {action}")
        
        self.history.append(action)
        
        # Check terminal conditions
        if len(self.history) == 1:
            if action == Action.BET:
                # Player 0 bets, now player 1's turn
                self.current_player = 1
                self.pot[0] += self.BET_SIZE
            else:
                # Player 0 passes, now player 1's turn
                self.current_player = 1
        elif len(self.history) == 2:
            if self.history[0] == Action.PASS and action == Action.PASS:
                # Pass, Pass -> Showdown
                self.is_terminal = True
                self.payoff = self._showdown()
            elif self.history[0] == Action.PASS and action == Action.BET:
                # Pass, Bet -> Player 0 decides
                self.current_player = 0
                self.pot[1] += self.BET_SIZE
            elif self.history[0] == Action.BET and action == Action.PASS:
                # Bet, Pass -> Player 0 wins (fold)
                self.is_terminal = True
                self.payoff = [self.pot[1], -self.pot[1]]
            elif self.history[0] == Action.BET and action == Action.BET:
                # Bet, Bet -> Showdown
                self.pot[1] += self.BET_SIZE
                self.is_terminal = True
                self.payoff = self._showdown()
        elif len(self.history) == 3:
            # Pass, Bet, X
            if action == Action.PASS:
                # Pass, Bet, Pass -> Player 1 wins (fold)
                self.is_terminal = True
                self.payoff = [-self.pot[0], self.pot[0]]
            else:
                # Pass, Bet, Bet -> Showdown
                self.pot[0] += self.BET_SIZE
                self.is_terminal = True
                self.payoff = self._showdown()
        
        return self.is_terminal, self.payoff
    
    def _showdown(self) -> List[int]:
        """Determine winner at showdown. Returns [payoff_p0, payoff_p1]"""
        if self.cards[0] > self.cards[1]:
            # Player 0 wins
            return [self.pot[1], -self.pot[1]]
        else:
            # Player 1 wins
            return [-self.pot[0], self.pot[0]]
    
    def get_info_set(self, player: int) -> str:
        """
        Returns information set string for given player.
        Format: "card-action_history"
        """
        card_name = self.CARD_NAMES[self.cards[player]]
        history_str = ''.join(['p' if a == Action.PASS else 'b' for a in self.history])
        return f"{card_name}-{history_str}"
    
    def get_current_player(self) -> int:
        """Returns current player to act (0 or 1)"""
        return self.current_player
    
    def get_history_str(self) -> str:
        """Returns action history as string"""
        return ''.join(['p' if a == Action.PASS else 'b' for a in self.history])
    
    @staticmethod
    def card_to_str(card: int) -> str:
        """Convert card number to string"""
        return KuhnPoker.CARD_NAMES[card]
