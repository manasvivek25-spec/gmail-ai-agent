
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QScrollArea
from PyQt6.QtCore import pyqtSignal

class Sidebar(QWidget):
    nav_clicked = pyqtSignal(str) # Emits the name of the section or label
    
    def __init__(self):
        super().__init__()
        self.setObjectName("sidebar")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 20, 10, 20)
        self.layout.setSpacing(5)
        
        self.init_ui()
        
    def init_ui(self):
        # App Title
        header = QLabel("AI GMAIL OS")
        header.setObjectName("sidebar_header")
        self.layout.addWidget(header)
        
        # Communication Section
        self.layout.addWidget(QLabel("COMMUNICATION", objectName="sidebar_label"))
        self.add_nav_btn("Inbox")
        self.add_nav_btn("Starred")
        
        # AI Features Section
        self.layout.addWidget(QLabel("AI FEATURES", objectName="sidebar_label"))
        self.add_nav_btn("Recommended")
        self.add_nav_btn("Deadlines")
        
        # AI Categories Section
        self.layout.addWidget(QLabel("AI CATEGORIES", objectName="sidebar_label"))
        self.categories_container = QWidget()
        self.categories_layout = QVBoxLayout(self.categories_container)
        self.categories_layout.setContentsMargins(0, 0, 0, 0)
        self.categories_layout.setSpacing(5)
        self.layout.addWidget(self.categories_container)
        
        # Labels Section
        self.layout.addWidget(QLabel("USER LABELS", objectName="sidebar_label"))
        self.labels_container = QWidget()
        self.labels_layout = QVBoxLayout(self.labels_container)
        self.labels_layout.setContentsMargins(0, 0, 0, 0)
        self.labels_layout.setSpacing(5)
        self.layout.addWidget(self.labels_container)
        
        # Management Section
        self.layout.addWidget(QLabel("MANAGEMENT", objectName="sidebar_label"))
        self.add_nav_btn("🔄 Refresh Emails")
        
        self.layout.addStretch()
        
    def add_nav_btn(self, name):
        btn = QPushButton(name)
        btn.setProperty("class", "nav_btn")
        btn.clicked.connect(lambda: self.nav_clicked.emit(name))
        self.layout.addWidget(btn)
        
    def update_labels(self, labels):
        # Clear existing labels
        for i in reversed(range(self.labels_layout.count())): 
            self.labels_layout.itemAt(i).widget().setParent(None)
            
        for label in labels:
            btn = QPushButton(label)
            btn.setProperty("class", "nav_btn")
            btn.clicked.connect(lambda checked, l=label: self.nav_clicked.emit(f"label:{l}"))
            self.labels_layout.addWidget(btn)

    def update_categories(self, category_counts):
        # Clear existing categories
        for i in reversed(range(self.categories_layout.count())): 
            self.categories_layout.itemAt(i).widget().setParent(None)
            
        for category, count in category_counts.items():
            btn = QPushButton(f"{category} ({count})")
            btn.setProperty("class", "nav_btn")
            btn.clicked.connect(lambda checked, c=category: self.nav_clicked.emit(f"category:{c}"))
            self.categories_layout.addWidget(btn)
