import sys
from database import get_db_connection
import psycopg2.extras
import subprocess
from PyQt6.QtWidgets import QListWidget
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QListWidget,
    QTextEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QInputDialog,
    QMessageBox,
    QLabel,
    QFrame
)
from email_memory import (
    create_label,
    get_labels,
    get_emails_for_label,
    add_rule,
    delete_rule,
    get_rules,
    count_emails_for_label,
    record_action,
    get_email_tags,
    get_email_labels,
    update_interest,
    get_top_interests,
    get_recommended_emails_metadata,
    toggle_bookmark
)
from nl_search import execute_nl_query
# ----------------------------
# Database Initialization
# ----------------------------

def initialize_database():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS emails (
    email_id TEXT PRIMARY KEY,
    subject TEXT,
    body TEXT,
    category TEXT,
    summary TEXT,
    deadline TEXT,
    relevance REAL,
    importance REAL DEFAULT 0,
    received_time INTEGER,
    is_bookmarked INTEGER DEFAULT 0
)
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS calendar_events (
        email_id TEXT PRIMARY KEY,
        event_name TEXT
    )
    """)

    conn.commit()
    conn.close()


initialize_database()

# ----------------------------
# Styles & Theme (White, Blue, Green)
# ----------------------------

STYLE_SHEET = """
QWidget {
    background-color: #FFFFFF;
    color: #333333;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 14px;
}

/* Sidebar */
#sidebar {
    background-color: #F0F4F8;
    border-right: 1px solid #D0D7DE;
}

#header_label {
    font-size: 22px;
    font-weight: 800;
    color: #2E8B57; /* Green Branding */
    margin-bottom: 20px;
    letter-spacing: 1px;
}

QLabel {
    font-weight: 700;
    color: #0047AB; /* Navy Blue Branding */
    text-transform: uppercase;
    font-size: 11px;
    letter-spacing: 0.5px;
    margin-top: 10px;
}

/* Lists */
QListWidget {
    border: 1px solid #E1E4E8;
    border-radius: 8px;
    background-color: #FFFFFF;
    outline: none;
}

QListWidget::item {
    padding: 12px;
    border-bottom: 1px solid #F6F8FA;
    border-radius: 4px;
}

QListWidget::item:hover {
    background-color: #F1F8FF;
}

QListWidget::item:selected {
    background-color: #E1F5FE;
    color: #0047AB;
    font-weight: bold;
    border-left: 5px solid #0047AB;
}

/* Buttons */
QPushButton {
    background-color: #0047AB;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 10px 16px;
    font-weight: 600;
    font-size: 13px;
}

QPushButton:hover {
    background-color: #0056b3;
}

QPushButton:pressed {
    background-color: #003d80;
}

/* Secondary Buttons (Green) */
QPushButton#ai_button {
    background-color: #2E8B57;
}

QPushButton#ai_button:hover {
    background-color: #3CB371;
}

/* Text Inputs */
QLineEdit {
    border: 2px solid #E1E4E8;
    border-radius: 8px;
    padding: 10px 15px;
    background-color: #F6F8FA;
    font-size: 14px;
}

QLineEdit:focus {
    border: 2px solid #0047AB;
    background-color: #FFFFFF;
}

QTextEdit {
    border: 1px solid #E1E4E8;
    border-radius: 8px;
    padding: 15px;
    line-height: 1.6;
    font-size: 14px;
    background-color: #FFFFFF;
}

/* Scrollbars */
QScrollBar:vertical {
    border: none;
    background: #F1F1F1;
    width: 8px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: #C1C1C1;
    min-height: 20px;
    border-radius: 4px;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
"""

# ----------------------------
# App
# ----------------------------

app = QApplication(sys.argv)
app.setStyleSheet(STYLE_SHEET)

window = QWidget()
window.setWindowTitle("AI Gmail OS - Professional Edition")
window.resize(1300, 800)

# ----------------------------
# Widgets
# ----------------------------
interest_list = QListWidget()
recommended_list = QListWidget()

recommended_list.setMaximumHeight(150)
interest_list.setMaximumHeight(120)
deadline_list = QListWidget()
deadline_list.setMaximumHeight(150)
search_box = QLineEdit()
search_box.setPlaceholderText("Search emails or ask AI...")

ai_search_button = QPushButton("🤖 AI Search")
ai_search_button.setObjectName("ai_button")

bookmark_button = QPushButton("⭐ Bookmark/Unbookmark")

show_bookmarks_button = QPushButton("📂 View Bookmarks")

refresh_button = QPushButton("Refresh Emails")
create_label_button = QPushButton("➕ Create Label")
add_rule_button = QPushButton("➕ Add Rule")
manage_rules_button = QPushButton("📋 Manage Rules")
all_labels_button = QPushButton("📧 All Emails")
email_list = QListWidget()

details = QTextEdit()
details.setReadOnly(True)

email_map = {}
deadline_map = {}
recommended_map = {}
interest_map = {}
label_buttons = []
label_layout = QVBoxLayout() # Changed to Vertical for Sidebar
current_filter = "ALL"

# ----------------------------
# Helper Functions
# ----------------------------

def show_email_by_id(email_id):
    if not email_id:
        return

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
SELECT subject,
       category,
       summary,
       deadline,
       relevance,
       body,
       importance
FROM emails
WHERE email_id=%s
""", (email_id,))

    email = cursor.fetchone()
    tags = get_email_tags(email_id)
    labels = get_email_labels(email_id)
    conn.close()

    if email is None:
        return

    text = f"""
SUBJECT
----------------------------------------
{email[0]}

CATEGORY
----------------------------------------
{email[1]}

LABELS
----------------------------------------
{", ".join(labels)}

TAGS
----------------------------------------
{", ".join(tags)}

SUMMARY
----------------------------------------
{email[2]}

DEADLINE
----------------------------------------
{email[3]}

RELEVANCE
----------------------------------------
{email[4]}

IMPORTANCE
----------------------------------------
{email[6]}

ORIGINAL EMAIL
----------------------------------------
{email[5]}
"""
    details.setText(text)
    
    # Record action and update interests
    record_action(email_id, "opened")
    for tag in tags:
        update_interest(tag)
# ----------------------------
# Load Emails
# ----------------------------

def load_emails():

    email_list.clear()
    email_map.clear()

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT email_id,
           subject,
           relevance,
           is_bookmarked
    FROM emails
    WHERE category != 'PHD_SEMINAR'
    ORDER BY importance DESC,
             received_time DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    for email_id, subject, relevance, is_bookmarked in rows:

        score = relevance if relevance else 0
        if score >= 9:
            prefix = "🚨"

        elif score >= 6:
            prefix = "🔥"

        elif score >= 3:
            prefix = "⚡"

        else:
            prefix = "📄"

        if is_bookmarked:
            prefix = "⭐"

        display_text = f"{prefix} {subject}"

        email_list.addItem(
            display_text
        )

        email_map[
            display_text
        ] = email_id


def run_ai_search():

    query = search_box.text().strip()

    if not query:
        return

    details.setText(f"🤖 AI is searching for: '{query}'...")

    results = execute_nl_query(query)

    email_list.clear()
    email_map.clear()

    if not results:
        details.setText("No results found or AI failed to understand.")
        return

    for row in results:
        # Assuming row[0] is email_id and row[1] is subject
        # We need to be careful about what columns execute_nl_query returns.
        # Let's assume it returns all columns if it's 'SELECT *' or similar.
        # But for the list we only need ID and Subject.
        
        email_id = row[0]
        subject = row[1]
        
        display_text = subject
        email_list.addItem(display_text)
        email_map[display_text] = email_id

    details.setText(f"Found {len(results)} results.")


def toggle_bookmark_ui():

    item = email_list.currentItem()

    if item is None:
        return

    subject = item.text()

    email_id = email_map[subject]

    toggle_bookmark(email_id)

    show_email()
    load_emails()


def filter_bookmarks():

    email_list.clear()
    email_map.clear()

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT email_id,
           subject
    FROM emails
    WHERE is_bookmarked = 1
    ORDER BY received_time DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    for email_id, subject in rows:

        display_text = f"⭐ {subject}"

        email_list.addItem(
            display_text
        )

        email_map[
            display_text
        ] = email_id

    details.setText("Showing bookmarked emails.")
# ----------------------------
# Search Emails
# ----------------------------

def load_deadlines():

    deadline_list.clear()
    deadline_map.clear()

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT DISTINCT
           email_id,
           subject,
           deadline
    FROM emails
    WHERE deadline IS NOT NULL
      AND deadline != ''
      AND deadline != 'NONE'
    """)

    rows = cursor.fetchall()

    conn.close()

    today = datetime.today().date()

    upcoming = []

    for email_id, subject, deadline in rows:

        formats = [
            "%Y-%m-%d",
            "%d/%m/%y",
            "%d/%m/%Y",
            "%d-%m-%Y"
        ]

        deadline_date = None

        for fmt in formats:

            try:

                deadline_date = datetime.strptime(
                    deadline.strip(),
                    fmt
                ).date()

                break

            except:
                pass

        if deadline_date is None:
            continue

        # Skip expired deadlines
        if deadline_date < today:
            continue

        days_left = (
            deadline_date - today
        ).days

        upcoming.append(
            (
                deadline_date,
                days_left,
                subject,
                deadline,
                email_id
            )
        )

    upcoming.sort(
        key=lambda x: x[0]
    )

    for _, days_left, subject, deadline, email_id in upcoming:

        display_text = f"[{days_left} days] {deadline} | {subject}"
        deadline_list.addItem(display_text)
        deadline_map[display_text] = email_id

def load_interests():

    interest_list.clear()
    interest_map.clear()

    interests = get_top_interests()

    for keyword, score in interests:

        display_text = f"🔥 {keyword} ({score})"
        interest_list.addItem(display_text)
        interest_map[display_text] = keyword

def filter_by_interest(display_text):
    keyword = interest_map.get(display_text)
    if not keyword:
        return

    email_list.clear()
    email_map.clear()

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT e.email_id, e.subject
    FROM emails e
    JOIN email_tags t ON e.email_id = t.email_id
    WHERE t.tag = %s
    ORDER BY e.importance DESC
    """, (keyword,))

    rows = cursor.fetchall()
    conn.close()

    for email_id, subject in rows:
        email_list.addItem(subject)
        email_map[subject] = email_id

    details.setText(f"Showing emails tagged with '{keyword}'")

def load_recommendations():

    recommended_list.clear()
    recommended_map.clear()

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT email_id, subject, importance
    FROM emails
    ORDER BY importance DESC
    LIMIT 5
    """)
    rows = cursor.fetchall()
    conn.close()

    for email_id, subject, importance in rows:
        display_text = f"⭐ {subject} ({importance})"
        recommended_list.addItem(display_text)
        recommended_map[display_text] = email_id
# ----------------------------
# Show Email
# ----------------------------
def search_emails():

    query = search_box.text().lower().strip()

    email_list.clear()
    email_map.clear()

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT email_id,
           subject
    FROM emails
    ORDER BY importance DESC,
        received_time DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    for email_id, subject in rows:

        if query == "" or query in subject.lower():

            email_list.addItem(subject)

            display_text = subject

            email_map[
    display_text
] = email_id

def show_email():
    item = email_list.currentItem()
    if item is None:
        return
    
    subject = item.text()
    email_id = email_map.get(subject)
    show_email_by_id(email_id)
# ----------------------------
# Refresh Emails
# ----------------------------

def refresh_emails():

    details.setText("Refreshing emails...")

    try:

        subprocess.run(
            [sys.executable, "main.py"]
        )

        load_emails()
        load_deadlines()
        load_interests()
        load_recommendations()
        details.setText(
            "Refresh completed."
        )

    except Exception as e:

        details.setText(
            f"Refresh failed:\n{e}"
        )
def create_new_label():

    label_name, ok = QInputDialog.getText(
        window,
        "Create Label",
        "Enter label name:"
    )

    if not ok:
        return

    label_name = label_name.strip()

    if label_name == "":
        return

    create_label(label_name)

    QMessageBox.information(
        window,
        "Success",
        f"Label '{label_name}' created."
    )

    load_dynamic_labels()
def load_dynamic_labels():

    global label_buttons

    for btn in label_buttons:

        label_layout.removeWidget(btn)

        btn.deleteLater()

    label_buttons = []

    labels = get_labels()

    for label in labels:

        button = QPushButton(label)

        button.clicked.connect(
            lambda checked,
            lbl=label:
            filter_by_label(lbl)
        )

        label_layout.addWidget(button)

        label_buttons.append(button)
def filter_by_label(label_name):

    email_list.clear()
    email_map.clear()

    email_ids = get_emails_for_label(
        label_name
    )

    if not email_ids:

        details.setText(
            f"No emails found for '{label_name}'"
        )

        return

    conn = get_db_connection()
    cursor = conn.cursor()

    for email_id in email_ids:

        cursor.execute("""
        SELECT email_id,
               subject
        FROM emails
        WHERE email_id=%s
        """, (email_id,))

        row = cursor.fetchone()

        if row:

            email_list.addItem(
                row[1]
            )

            email_map[
                row[1]
            ] = row[0]

    conn.close()

    details.setText(
        f"Showing emails for '{label_name}'"
    )
def show_all_emails():

    load_emails()

    details.setText(
        "Showing all emails"
    )
def add_rule_ui():

    label_name, ok = QInputDialog.getText(
        window,
        "Label",
        "Enter label:"
    )

    if not ok:
        return

    keyword, ok = QInputDialog.getText(
        window,
        "Keyword",
        "Enter keyword:"
    )

    if not ok:
        return

    add_rule(
        label_name,
        keyword
    )

    QMessageBox.information(
        window,
        "Success",
        "Rule added."
    )
def manage_rules():

    labels = get_labels()

    text = ""

    for label in labels:

        count = count_emails_for_label(
            label
        )

        text += (
            f"{label} ({count})\n"
        )

        rules = get_rules(
            label
        )

        for rule in rules:

            text += (
                f"   - {rule}\n"
            )

        text += "\n"

    QMessageBox.information(
        window,
        "Label Rules",
        text
    )
# ----------------------------
# Events
# ----------------------------
add_rule_button.clicked.connect(add_rule_ui)
create_label_button.clicked.connect(create_new_label)
manage_rules_button.clicked.connect(manage_rules)
email_list.itemClicked.connect(show_email)
all_labels_button.clicked.connect(show_all_emails)
refresh_button.clicked.connect(refresh_emails)
search_box.textChanged.connect(search_emails)

ai_search_button.clicked.connect(lambda: run_ai_search())
bookmark_button.clicked.connect(lambda: toggle_bookmark_ui())
show_bookmarks_button.clicked.connect(lambda: filter_bookmarks())

# New Interaction Connections
deadline_list.itemClicked.connect(lambda item: show_email_by_id(deadline_map.get(item.text())))
recommended_list.itemClicked.connect(lambda item: show_email_by_id(recommended_map.get(item.text())))
interest_list.itemClicked.connect(lambda item: filter_by_interest(item.text()))

# ----------------------------
# Layout (Professional Sidebar)
# ----------------------------

main_layout = QHBoxLayout()
main_layout.setContentsMargins(0, 0, 0, 0)
main_layout.setSpacing(0)

# SIDEBAR
sidebar_widget = QWidget()
sidebar_widget.setObjectName("sidebar")
sidebar_widget.setFixedWidth(300)
sidebar_layout_main = QVBoxLayout(sidebar_widget)
sidebar_layout_main.setContentsMargins(15, 20, 15, 20)
sidebar_layout_main.setSpacing(15)

app_title = QLabel("AI GMAIL OS")
app_title.setObjectName("header_label")
sidebar_layout_main.addWidget(app_title)

# Quick Actions
sidebar_layout_main.addWidget(QLabel("QUICK ACTIONS"))
sidebar_layout_main.addWidget(refresh_button)
sidebar_layout_main.addWidget(show_bookmarks_button)
sidebar_layout_main.addWidget(all_labels_button)

# Labels Section
sidebar_layout_main.addWidget(QLabel("MY LABELS"))
sidebar_layout_main.addWidget(create_label_button)
sidebar_layout_main.addLayout(label_layout) # label_layout is QVBoxLayout

# Logic Section
sidebar_layout_main.addWidget(QLabel("AUTO-FILTERING"))
sidebar_layout_main.addWidget(add_rule_button)
sidebar_layout_main.addWidget(manage_rules_button)

# Stats Sections
sidebar_layout_main.addWidget(QLabel("TOP INTERESTS"))
sidebar_layout_main.addWidget(interest_list)

sidebar_layout_main.addStretch()

# MAIN CONTENT AREA
content_widget = QWidget()
content_main_layout = QVBoxLayout(content_widget)
content_main_layout.setContentsMargins(20, 20, 20, 20)
content_main_layout.setSpacing(15)

# Top Bar (Search & AI)
top_bar_layout = QHBoxLayout()
top_bar_layout.addWidget(search_box)
top_bar_layout.addWidget(ai_search_button)
content_main_layout.addLayout(top_bar_layout)

# Recommendation & Deadline Row
top_widgets_layout = QHBoxLayout()

rec_vbox = QVBoxLayout()
rec_vbox.addWidget(QLabel("RECOMMENDED FOR YOU"))
rec_vbox.addWidget(recommended_list)
top_widgets_layout.addLayout(rec_vbox, 1)

dead_vbox = QVBoxLayout()
dead_vbox.addWidget(QLabel("UPCOMING DEADLINES"))
dead_vbox.addWidget(deadline_list)
top_widgets_layout.addLayout(dead_vbox, 1)

content_main_layout.addLayout(top_widgets_layout)

# Email List and Details
email_details_layout = QHBoxLayout()

email_list_vbox = QVBoxLayout()
email_list_vbox.addWidget(QLabel("INBOX"))
email_list_vbox.addWidget(email_list)
email_details_layout.addLayout(email_list_vbox, 1)

details_vbox = QVBoxLayout()
details_vbox.addWidget(QLabel("EMAIL PREVIEW"))
details_vbox.addWidget(bookmark_button)
details_vbox.addWidget(details)
email_details_layout.addLayout(details_vbox, 2)

content_main_layout.addLayout(email_details_layout)

# Assemble
main_layout.addWidget(sidebar_widget)
main_layout.addWidget(content_widget)

window.setLayout(main_layout)

# ----------------------------
# Startup
# ----------------------------

load_emails()
load_deadlines()
load_interests()
load_recommendations()
load_dynamic_labels()
window.show()

sys.exit(app.exec())