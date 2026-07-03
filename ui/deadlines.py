
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QFrame
from PyQt6.QtCore import pyqtSignal
import email_memory
from .inbox_panel import EmailCard

class DeadlinesView(QWidget):
    email_selected = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.setObjectName("deadlines_panel")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        
        self.layout.addWidget(QLabel("UPCOMING DEADLINES", objectName="details_header"))
        
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.container = QWidget()
        self.cards_layout = QVBoxLayout(self.container)
        self.cards_layout.setContentsMargins(0, 20, 0, 0)
        self.cards_layout.setSpacing(15)
        self.cards_layout.addStretch()
        self.scroll.setWidget(self.container)
        self.layout.addWidget(self.scroll)
        
    def refresh(self):
        # Clear existing
        for i in reversed(range(self.cards_layout.count())):
            item = self.cards_layout.itemAt(i)
            if item.widget():
                item.widget().setParent(None)
                
        deadlines = email_memory.get_all_deadlines()
        
        # Categories
        today = []
        tomorrow = []
        this_week = []
        later = []
        
        for d in deadlines:
            if d["days_left"] == 0: today.append(d)
            elif d["days_left"] == 1: tomorrow.append(d)
            elif d["days_left"] <= 7: this_week.append(d)
            else: later.append(d)
            
        self.add_section("TODAY", today)
        self.add_section("TOMORROW", tomorrow)
        self.add_section("THIS WEEK", this_week)
        self.add_section("LATER", later)
        
    def add_section(self, title, emails):
        if not emails:
            return
            
        label = QLabel(title)
        label.setObjectName("details_section_title")
        self.cards_layout.insertWidget(self.cards_layout.count() - 1, label)
        
        for email in emails:
            card = EmailCard(email)
            card.clicked.connect(self.email_selected.emit)
            self.cards_layout.insertWidget(self.cards_layout.count() - 1, card)
