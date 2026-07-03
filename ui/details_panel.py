
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QScrollArea, QFrame, QPushButton, QHBoxLayout
from PyQt6.QtCore import pyqtSignal

class DetailsPanel(QWidget):
    bookmark_clicked = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setObjectName("details_panel")
        self.layout = QVBoxLayout(self)
        
        # Header + Bookmark Button
        header_container = QHBoxLayout()
        self.header = QLabel("Select an email to view details")
        self.header.setObjectName("details_header")
        self.header.setWordWrap(True)
        
        self.bookmark_btn = QPushButton("⭐")
        self.bookmark_btn.setFixedWidth(50)
        self.bookmark_btn.clicked.connect(self.bookmark_clicked.emit)
        
        header_container.addWidget(self.header, 1)
        header_container.addWidget(self.bookmark_btn)
        self.layout.addLayout(header_container)
        
        # Scroll area for details
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.container = QWidget()
        self.details_layout = QVBoxLayout(self.container)
        self.details_layout.setContentsMargins(0, 0, 0, 0)
        
        self.scroll.setWidget(self.container)
        self.layout.addWidget(self.scroll)
        
        # Placeholder for AI Info
        self.ai_summary = self.add_section("AI SUMMARY")
        self.ai_importance = self.add_section("WHY IT IS IMPORTANT")
        self.ai_action = self.add_section("SUGGESTED ACTION")
        self.ai_deadline = self.add_section("DEADLINE")
        
        # Original Content
        self.layout.addWidget(QLabel("ORIGINAL CONTENT", objectName="details_section_title"))
        self.body = QTextEdit()
        self.body.setReadOnly(True)
        self.body.setObjectName("details_content")
        self.layout.addWidget(self.body, 1)

    def add_section(self, title):
        self.details_layout.addWidget(QLabel(title, objectName="details_section_title"))
        label = QLabel("")
        label.setWordWrap(True)
        label.setObjectName("details_content")
        self.details_layout.addWidget(label)
        return label

    def update_details(self, email_data):
        self.header.setText(email_data.get("subject", "No Subject"))
        self.ai_summary.setText(email_data.get("summary", "N/A"))
        self.ai_importance.setText(email_data.get("importance_reason", "N/A"))
        self.ai_action.setText(email_data.get("suggested_action", "N/A"))
        self.ai_deadline.setText(email_data.get("deadline", "None"))
        self.body.setText(email_data.get("body", ""))
