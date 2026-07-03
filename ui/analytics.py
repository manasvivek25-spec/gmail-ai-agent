
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
import email_memory

class AnalyticsView(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("analytics_panel")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)
        
        self.layout.addWidget(QLabel("ANALYTICS", objectName="details_header"))
        
        self.stats_layout = QHBoxLayout()
        self.processed_card = self.create_stat_card("Total Emails", "0")
        self.deadlines_card = self.create_stat_card("Deadlines Found", "0")
        self.labels_card = self.create_stat_card("User Labels", "0")
        
        self.stats_layout.addWidget(self.processed_card)
        self.stats_layout.addWidget(self.deadlines_card)
        self.stats_layout.addWidget(self.labels_card)
        self.layout.addLayout(self.stats_layout)
        
        # Top Interests Section
        self.layout.addWidget(QLabel("TOP INTERESTS", objectName="details_section_title"))
        self.interests_container = QWidget()
        self.interests_layout = QVBoxLayout(self.interests_container)
        self.interests_layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.interests_container)
        
        self.layout.addStretch()

    def create_stat_card(self, label, value):
        card = QFrame()
        card.setObjectName("stat_card")
        layout = QVBoxLayout(card)
        
        val_label = QLabel(value)
        val_label.setObjectName("stat_value")
        layout.addWidget(val_label)
        
        lbl_label = QLabel(label)
        lbl_label.setObjectName("stat_label")
        layout.addWidget(lbl_label)
        
        # Save reference to update value later
        card.val_label = val_label
        return card

    def refresh(self):
        # Update Stats
        total_emails = email_memory.get_email_count()
        self.processed_card.val_label.setText(str(total_emails))
        
        deadlines = email_memory.get_all_deadlines()
        self.deadlines_card.val_label.setText(str(len(deadlines)))
        
        labels = email_memory.get_labels()
        self.labels_card.val_label.setText(str(len(labels)))
        
        # Update Interests
        for i in reversed(range(self.interests_layout.count())):
            item = self.interests_layout.itemAt(i)
            if item.widget():
                item.widget().setParent(None)
                
        interests = email_memory.get_top_interests(10)
        for keyword, score in interests:
            item = QLabel(f"🔥 {keyword}: {score} interactions")
            item.setObjectName("details_content")
            self.interests_layout.addWidget(item)
