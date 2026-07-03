
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QScrollArea, QFrame, QPushButton
from PyQt6.QtCore import pyqtSignal, Qt

class EmailCard(QFrame):
    clicked = pyqtSignal(str) # Emits email_id
    
    def __init__(self, email_data):
        super().__init__()
        self.setObjectName("email_card")
        self.email_id = email_data.get("email_id")
        self.layout = QVBoxLayout(self)
        
        # Header: Sender and Time
        header_layout = QHBoxLayout()
        sender = QLabel(email_data.get("sender", "Unknown"))
        sender.setObjectName("card_sender")
        time = QLabel(email_data.get("time", ""))
        time.setObjectName("card_time")
        header_layout.addWidget(sender)
        header_layout.addStretch()
        header_layout.addWidget(time)
        self.layout.addLayout(header_layout)
        
        # Subject and Priority
        subj_layout = QHBoxLayout()
        subject = QLabel(email_data.get("subject", "(No Subject)"))
        subject.setObjectName("card_subject")
        subject.setWordWrap(True)
        
        priority_val = email_data.get("priority", "Low").lower()
        priority_icon = "📄"
        priority_id = "priority_low"
        if priority_val == "critical": priority_icon, priority_id = "🚨", "priority_critical"
        elif priority_val == "high": priority_icon, priority_id = "🔥", "priority_high"
        elif priority_val == "medium": priority_icon, priority_id = "⚡", "priority_medium"
        
        priority = QLabel(f"{priority_icon} {priority_val.upper()}")
        priority.setObjectName(priority_id)
        
        subj_layout.addWidget(subject, 1)
        subj_layout.addWidget(priority)
        self.layout.addLayout(subj_layout)
        
        # Summary
        summary = QLabel(email_data.get("summary", ""))
        summary.setObjectName("card_summary")
        summary.setWordWrap(True)
        summary.setMaximumHeight(40)
        self.layout.addWidget(summary)
        
    def mousePressEvent(self, event):
        self.clicked.emit(self.email_id)

class InboxPanel(QWidget):
    email_selected = pyqtSignal(str)
    ai_search_clicked = pyqtSignal(str)
    ai_ask_clicked = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.setObjectName("inbox_panel")
        self.layout = QVBoxLayout(self)
        
        # Search Bar Area
        search_container = QHBoxLayout()
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search communications or ask AI...")
        
        self.ai_search_btn = QPushButton("🔍 AI Search")
        self.ai_search_btn.setObjectName("ai_button")
        self.ai_search_btn.clicked.connect(lambda: self.ai_search_clicked.emit(self.search_box.text()))
        
        self.ai_ask_btn = QPushButton("🤖 Ask AI")
        self.ai_ask_btn.setObjectName("ai_button")
        self.ai_ask_btn.clicked.connect(lambda: self.ai_ask_clicked.emit(self.search_box.text()))
        
        search_container.addWidget(self.search_box, 1)
        search_container.addWidget(self.ai_search_btn)
        search_container.addWidget(self.ai_ask_btn)
        self.layout.addLayout(search_container)
        
        # Scroll Area for Cards
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.container = QWidget()
        self.cards_layout = QVBoxLayout(self.container)
        self.cards_layout.setContentsMargins(0, 0, 0, 0)
        self.cards_layout.setSpacing(10)
        self.cards_layout.addStretch()
        self.scroll.setWidget(self.container)
        self.layout.addWidget(self.scroll)
        
    def update_emails(self, emails):
        # Clear existing
        for i in reversed(range(self.cards_layout.count())):
            item = self.cards_layout.itemAt(i)
            if item.widget():
                item.widget().setParent(None)
        
        for email in emails:
            card = EmailCard(email)
            card.clicked.connect(self.email_selected.emit)
            self.cards_layout.insertWidget(self.cards_layout.count() - 1, card)
