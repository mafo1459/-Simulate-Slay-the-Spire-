import random
import sys
from enum import Enum

import Package_Card as PC
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QStackedWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

"""  
    此package保存界面的布局以及一些控件的实现
"""


# 页面A：随机模拟出牌
class PageA(QWidget):
    def __init__(self):
        super().__init__()
        self.text = QTextEdit(self)
        self.text.setReadOnly(True)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # 能量输入
        self.energy_input = QLineEdit(self)
        energy_layout = QHBoxLayout()
        energy_layout.addWidget(QLabel("Energy(费用):"))
        energy_layout.addWidget(self.energy_input)

        # 模拟次数输入
        self.attempts_input = QLineEdit(self)
        attempts_layout = QHBoxLayout()
        attempts_layout.addWidget(QLabel("Attempts(模拟次数):"))
        attempts_layout.addWidget(self.attempts_input)

        # 运行按钮
        self.run_button = QPushButton("Run Simulate", self)
        self.run_button.clicked.connect(self.runSimulate)

        # 添加到布局
        layout.addLayout(energy_layout)
        layout.addLayout(attempts_layout)
        layout.addWidget(self.text)
        layout.addWidget(self.run_button)

        self.setLayout(layout)

    def runSimulate(self):
        try:
            energy = int(self.energy_input.text())
            attempts = int(self.attempts_input.text())
            self.text.clear()

            for _ in range(attempts):
                self.text.append("---------------------------------------------------")
                self.simulate(energy)
        except ValueError:
            QMessageBox.warning(self, "错误", "请输入有效的数字")

    def simulate(self, energy):
        user = PC.User(energy=energy)
        cards = [PC.CardDuPi(), PC.CardJianBing(), PC.CardQiYue(), PC.CardKuangNu()]
        user.draw_pile = cards.copy()
        random.shuffle(user.draw_pile)

        for _ in range(4):
            if user.draw_pile:
                card = user.draw_pile.pop()
                card.status = PC.CardStatus.IN_HAND
                user.hand.append(card)

        while user.energy > 0 or user.has_dupi():
            if not user.hand:
                break

            hand_names = [card.name for card in user.hand]
            discard_names = [card.name for card in user.discard_pile]
            self.text.append(f"手牌中：{hand_names} ,    弃牌中：{discard_names}")

            card = random.choice(user.hand)
            try:
                card.play(user)
                user.hand.remove(card)
                self.text.append(
                    f"打出 {card.name},   费用: {user.energy},     总伤: {user.total_damage},    护甲: {user.armor},     狂怒Buff: {user.buff}"
                )
            except RuntimeError as e:
                self.text.append(f"无法打出 {card.name}: {e}")


# 页面B：手动出牌
class PageB(QWidget):
    def __init__(self):
        super().__init__()
        self.user = PC.User()
        self.info_text = QTextEdit(self)
        self.info_text.setReadOnly(True)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        buttonLayout = QHBoxLayout()

        # 初始化手牌
        cards = [PC.CardDuPi(), PC.CardJianBing(), PC.CardQiYue(), PC.CardKuangNu()]
        self.user.hand = cards.copy()

        for card in self.user.hand:
            card.status = PC.CardStatus.IN_HAND

        self.card_buttons = []
        for card in self.user.hand:
            btn = QPushButton(card.name)
            btn.setFixedSize(80, 80)
            btn.clicked.connect(lambda _, c=card: self.play_card(c))
            buttonLayout.addWidget(btn)
            self.card_buttons.append(btn)

        self.reset_button = QPushButton("重置", self)
        self.reset_button.clicked.connect(self.reset)
        layout.addWidget(self.reset_button)
        layout.addWidget(self.info_text)
        layout.addLayout(buttonLayout)

        self.setLayout(layout)

    def play_card(self, card):
        try:

            if card not in self.user.hand:
                raise RuntimeError(f"{card.name} 不在手牌中")

            card.play(self.user)
            self.user.hand.remove(card)
            self.update_info_text(card)

            # 更新按钮状态
            self.update_button_states()
        except RuntimeError as e:
            QMessageBox.warning(self, "错误", str(e))

    def update_info_text(self, card):
        hand_names = [c.name for c in self.user.hand]
        discard_names = [c.name for c in self.user.discard_pile]
        info = (
            f"打出牌: {card.name}\n"
            f"手牌剩余: {hand_names}\n"
            f"弃牌堆剩余: {discard_names}\n"
            f"护甲: {self.user.armor}\n"
            f"Buff: {self.user.buff}\n"
            f"总伤害: {self.user.total_damage}\n"
            f"已消耗能量: {self.user.exhausted_energy}"
        )
        self.info_text.append("---------------------------------------------------")
        self.info_text.append(info)

    def update_button_states(self):
        """更新按钮状态，根据卡牌状态启用或禁用按钮"""
        for btn in self.card_buttons:
            card_name = btn.text()

            target_card = None
            for card in self.user.hand + self.user.discard_pile:
                if card.name == card_name:
                    target_card = card
                    break

            if target_card is None or target_card.status != PC.CardStatus.IN_HAND:
                btn.setEnabled(False)
            else:
                btn.setEnabled(True)

    def reset(self):
        """重置用户状态和界面"""

        self.user = PC.User()
        self.info_text.clear()

        self.cards = [
            PC.CardDuPi(),
            PC.CardJianBing(),
            PC.CardQiYue(),
            PC.CardKuangNu(),
        ]
        self.user.hand = self.cards.copy()

        for card in self.user.hand:
            card.status = PC.CardStatus.IN_HAND

        # 重新绑定按钮的点击事件
        for btn, card in zip(self.card_buttons, self.user.hand):
            btn.clicked.disconnect()
            btn.clicked.connect(lambda _, c=card: self.play_card(c))

        # 重新启用所有按钮
        for btn in self.card_buttons:
            btn.setEnabled(True)
