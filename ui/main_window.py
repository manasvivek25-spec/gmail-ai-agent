
import sys
import subprocess
from PyQt6.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QStackedWidget, QInputDialog, QMessageBox
from .sidebar import Sidebar
from .inbox_panel import InboxPanel
from .details_panel import DetailsPanel
from .recommendations import RecommendationsView
from .deadlines import DeadlinesView
from .styles import STYLE_SHEET
import email_memory
from nl_search import execute_nl_query
from ai_assistant import ask_assistant

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Communication OS")
        self.resize(1400, 900)
        self.setStyleSheet(STYLE_SHEET)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        self.init_ui()
        self.load_initial_data()
        
    def init_ui(self):
        # 1. Sidebar
        self.sidebar = Sidebar()
        self.main_layout.addWidget(self.sidebar)
        
        # 2. Main Content Area (Center + Right)
        self.content_stack = QStackedWidget()
        self.main_layout.addWidget(self.content_stack, 1)
        
        # View 1: Inbox (Three Panel)
        self.inbox_view = QWidget()
        self.inbox_layout = QHBoxLayout(self.inbox_view)
        self.inbox_layout.setContentsMargins(0, 0, 0, 0)
        self.inbox_layout.setSpacing(0)
        
        self.inbox_panel = InboxPanel()
        self.details_panel = DetailsPanel()
        
        self.inbox_layout.addWidget(self.inbox_panel, 1)
        self.inbox_layout.addWidget(self.details_panel, 2)
        
        self.content_stack.addWidget(self.inbox_view)
        
        # Other Views
        self.recs_view = RecommendationsView()
        self.deadlines_view = DeadlinesView()
        
        self.content_stack.addWidget(self.recs_view)
        self.content_stack.addWidget(self.deadlines_view)
        
        # Connect Signals
        self.sidebar.nav_clicked.connect(self.handle_navigation)
        self.inbox_panel.email_selected.connect(self.load_email_details)
        self.recs_view.email_selected.connect(self.load_email_details)
        self.deadlines_view.email_selected.connect(self.load_email_details)
        
        self.inbox_panel.ai_search_clicked.connect(self.run_ai_search)
        self.inbox_panel.ai_ask_clicked.connect(self.run_ai_assistant)
        self.details_panel.bookmark_clicked.connect(self.toggle_bookmark)
        self.current_email_id = None
        
    def load_initial_data(self):
        # Load Labels
        labels = email_memory.get_labels()
        self.sidebar.update_labels(labels)
        
        # Load Categories
        category_counts = email_memory.get_category_counts()
        self.sidebar.update_categories(category_counts)
        
        # Load Inbox
        emails = email_memory.get_all_emails_metadata()
        self.inbox_panel.update_emails(emails)
        
    def handle_navigation(self, name):
        if name == "Inbox":
            self.content_stack.setCurrentWidget(self.inbox_view)
            self.load_initial_data()
        elif name == "Starred":
            self.content_stack.setCurrentWidget(self.inbox_view)
            from database import get_db_connection
import psycopg2.extras
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT email_id FROM emails WHERE is_bookmarked = 1 ORDER BY received_time DESC")
            email_ids = [row[0] for row in cursor.fetchall()]
            conn.close()
            emails = email_memory.get_emails_metadata_by_ids(email_ids)
            self.inbox_panel.update_emails(emails)
        elif name == "Recommended":
            self.recs_view.refresh()
            self.content_stack.setCurrentWidget(self.recs_view)
        elif name == "Deadlines":
            self.deadlines_view.refresh()
            self.content_stack.setCurrentWidget(self.deadlines_view)
        elif name == "🔄 Refresh Emails":
            self.refresh_emails()
        elif name.startswith("label:"):
            label_name = name.split(":")[1]
            self.load_label_emails(label_name)
            self.content_stack.setCurrentWidget(self.inbox_view)
        elif name.startswith("category:"):
            category_name = name.split(":")[1]
            self.load_category_emails(category_name)
            self.content_stack.setCurrentWidget(self.inbox_view)
            
    def load_label_emails(self, label_name):
        email_ids = email_memory.get_emails_for_label(label_name)
        emails = email_memory.get_emails_metadata_by_ids(email_ids)
        self.inbox_panel.update_emails(emails)

    def load_category_emails(self, category_name):
        email_ids = email_memory.get_emails_by_category(category_name)
        emails = email_memory.get_emails_metadata_by_ids(email_ids)
        self.inbox_panel.update_emails(emails)

    def load_email_details(self, email_id):
        self.current_email_id = email_id
        email_data = email_memory.get_email_details(email_id)
        if email_data:
            # Fetch tags and labels
            email_data["tags"] = email_memory.get_email_tags(email_id)
            email_data["labels"] = email_memory.get_email_labels(email_id)
            
            # Record action
            email_memory.record_action(email_id, "opened")
            for tag in email_data["tags"]:
                email_memory.update_interest(tag)
                
            self.details_panel.update_details(email_data)
            # Switch to inbox view to show the details
            self.content_stack.setCurrentWidget(self.inbox_view)

    def run_ai_search(self, query):
        if not query:
            return
        
        self.details_panel.header.setText(f"🤖 AI is searching for: '{query}'...")
        results = execute_nl_query(query)
        
        if not results:
            self.details_panel.header.setText("No results found or AI failed to understand.")
            self.inbox_panel.update_emails([])
            return
            
        email_ids = [row[0] for row in results]
        emails = email_memory.get_emails_metadata_by_ids(email_ids)
        self.inbox_panel.update_emails(emails)
        self.details_panel.header.setText(f"Found {len(results)} results.")

    def run_ai_assistant(self, query):
        if not query:
            return
        
        # Show a "thinking" message in the details panel
        self.details_panel.header.setText(f"🤖 AI Assistant is thinking about: '{query}'...")
        
        # Get response from the conversational assistant
        response = ask_assistant(query)
        
        # Display the response in a message box for now (cleanest conversational UI)
        QMessageBox.information(self, "AI Assistant", response)
        self.details_panel.header.setText("AI Assistant response provided.")

    def toggle_bookmark(self):
        if self.current_email_id:
            email_memory.toggle_bookmark(self.current_email_id)
            # Give a small visual feedback
            self.details_panel.header.setText("⭐ Bookmark Toggled")
            # If in "Starred" view, refreshing might remove it, but generally good to refresh
            # self.load_initial_data() 

    def refresh_emails(self):
        self.details_panel.header.setText("Refreshing emails from Gmail...")
        try:
            subprocess.run([sys.executable, "main.py"])
            self.load_initial_data()
            self.details_panel.header.setText("Refresh completed.")
        except Exception as e:
            self.details_panel.header.setText(f"Refresh failed: {e}")
