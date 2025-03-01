import random
from enum import Enum

""" 
    此package保存所使用的卡牌的抽象类和子类实现,
    以及保存了角色类的属性

"""

# ------------------------------------------------------------------------------------------------------


# 卡牌状态枚举
class CardStatus(Enum):
    IN_HAND = 0
    IN_DISCARD = 1
    IN_DRAW = 2


# 卡牌类型枚举
class CardType(Enum):
    ATTACK = 0
    SKILL = 1


# 抽象类
class Card:
    def __init__(self, name, card_type, cost):
        self.name = name
        self.card_type = card_type
        self.cost = cost
        self.status = CardStatus.IN_DRAW

    def play(self, user):
        if self.status != CardStatus.IN_HAND:
            raise RuntimeError("Card不在手牌")
        if user.energy < self.cost:
            raise RuntimeError("费不够")

        user.energy -= self.cost
        user.exhausted_energy += self.cost

        self.effect(user)

        self.status = CardStatus.IN_DISCARD
        user.discard_pile.append(self)

    def effect(self, user):
        """卡牌效果，由子类实现"""
        pass


# 具体卡牌实现


#  \ 肚皮+ \
class CardDuPi(Card):
    def __init__(self):
        super().__init__("肚皮+", CardType.ATTACK, cost=0)

    def effect(self, user):
        damage = user.armor
        user.total_damage += damage
        user.armor += user.buff


#  \ 剑柄+ \
class CardJianBing(Card):
    def __init__(self):
        super().__init__("剑柄+", CardType.ATTACK, cost=1)

    def effect(self, user):
        damage = 10
        user.total_damage += damage
        user.armor += user.buff

        for _ in range(2):
            if user.discard_pile:
                card = random.choice(user.discard_pile)
                user.discard_pile.remove(card)
                card.status = CardStatus.IN_HAND
                user.hand.append(card)


# \  契约+ \
class CardQiYue(Card):
    def __init__(self):
        super().__init__("契约+", CardType.SKILL, cost=1)

    def effect(self, user):
        for _ in range(3):
            if user.discard_pile:
                card = random.choice(user.discard_pile)
                user.discard_pile.remove(card)
                card.status = CardStatus.IN_HAND
                user.hand.append(card)


# \ 狂怒+ \
class CardKuangNu(Card):
    def __init__(self):
        super().__init__("狂怒+", CardType.SKILL, cost=0)

    def effect(self, user):
        user.buff += 5


# ------------------------------------------------------------------------------------------------------


# 角色（使用者）类
class User:
    def __init__(self, energy=4):
        self.energy = energy
        self.total_damage = 0
        self.buff = 0
        self.armor = 0
        self.hand = []
        self.draw_pile = []
        self.discard_pile = []
        self.exhausted_energy = 0

    def has_dupi(self):
        return any(isinstance(card, CardDuPi) for card in self.hand)
