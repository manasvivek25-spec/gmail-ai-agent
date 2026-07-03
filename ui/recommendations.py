
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QFrame
from .inbox_panel import EmailCard
from PyQt6.QtCore import pyqtSignal
import email_memory

class RecommendationsView(QWidget):
    email_selected = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.setObjectName("recommendations_panel")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        
        self.layout.addWidget(QLabel("RECOMMENDED FOR YOU", objectName="details_header"))
        self.layout.addWidget(QLabel("AI-prioritized communications based on your interests and upcoming deadlines."))
        
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.container = QWidget()
        self.cards_layout = QVBoxLayout(self.container)
        self.cards_layout.setContentsMargins(0, 20, 0, 0)
        self.cards_layout.setSpacing(10)
        self.cards_layout.addStretch()
        self.scroll.setWidget(self.container)
        self.layout.addWidget(self.scroll)
        
    def refresh(self):
        # Clear existing
        for i in reversed(range(self.cards_layout.count())):
            item = self.cards_layout.itemAt(i)
            if item.widget():
                item.widget().setParent(None)
                
        emails = email_memory.get_recommended_emails_metadata()
        for email in emails:
            card = EmailCard(email)
            card.clicked.connect(self.email_selected.emit)
            self.cards_layout.insertWidget(self.cards_layout.count() - 1, card)
