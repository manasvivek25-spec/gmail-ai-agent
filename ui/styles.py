
STYLE_SHEET = """
QWidget {
    background-color: #FFFFFF;
    color: #333333;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 14px;
}

/* Sidebar */
#sidebar {
    background-color: #F8F9FA;
    border-right: 1px solid #E1E4E8;
    min-width: 250px;
}

#sidebar_header {
    font-size: 20px;
    font-weight: 800;
    color: #2E8B57;
    margin-bottom: 20px;
    padding: 10px;
}

#sidebar_label {
    font-weight: 700;
    color: #6A737D;
    text-transform: uppercase;
    font-size: 11px;
    letter-spacing: 1px;
    margin-top: 20px;
    margin-bottom: 5px;
    padding-left: 10px;
}

/* Navigation Buttons in Sidebar */
QPushButton.nav_btn {
    text-align: left;
    background-color: transparent;
    color: #333333;
    border: none;
    border-radius: 6px;
    padding: 10px 15px;
    font-weight: 500;
}

QPushButton.nav_btn:hover {
    background-color: #F1F8FF;
    color: #0047AB;
}

QPushButton.nav_btn[active="true"] {
    background-color: #E1F5FE;
    color: #0047AB;
    font-weight: bold;
}

/* Main Panels */
#inbox_panel, #details_panel, #recommendations_panel, #deadlines_panel, #analytics_panel {
    background-color: #FFFFFF;
}

/* Communication Card (Inbox Item) */
#email_card {
    background-color: #FFFFFF;
    border: 1px solid #E1E4E8;
    border-radius: 10px;
    margin-bottom: 10px;
    padding: 15px;
}

#email_card:hover {
    border-color: #0047AB;
    background-color: #F1F8FF;
}

#email_card[selected="true"] {
    border: 2px solid #0047AB;
    background-color: #E1F5FE;
}

#card_sender {
    font-weight: bold;
    font-size: 15px;
    color: #0047AB;
}

#card_subject {
    font-weight: 600;
    font-size: 14px;
    margin-top: 5px;
}

#card_summary {
    color: #586069;
    font-size: 13px;
    margin-top: 5px;
}

#card_time {
    color: #6A737D;
    font-size: 12px;
}

/* Priority Indicators */
#priority_critical { color: #D73A49; font-weight: bold; }
#priority_high { color: #F66A0A; font-weight: bold; }
#priority_medium { color: #FFD33D; font-weight: bold; }
#priority_low { color: #28A745; font-weight: bold; }

/* Right Panel / Details */
#details_header {
    font-size: 22px;
    font-weight: 800;
    color: #0047AB;
    margin-bottom: 15px;
}

#details_section_title {
    font-weight: 700;
    color: #2E8B57;
    text-transform: uppercase;
    font-size: 12px;
    margin-top: 20px;
    margin-bottom: 5px;
}

#details_content {
    line-height: 1.6;
    font-size: 14px;
}

/* Generic Components */
QPushButton.primary_btn {
    background-color: #0047AB;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 10px 20px;
    font-weight: 600;
}

QPushButton.primary_btn:hover {
    background-color: #0056b3;
}

QLineEdit {
    border: 2px solid #E1E4E8;
    border-radius: 8px;
    padding: 10px 15px;
    background-color: #F6F8FA;
}

QLineEdit:focus {
    border-color: #0047AB;
    background-color: #FFFFFF;
}

/* Analytics Cards */
#stat_card {
    background-color: #FFFFFF;
    border: 1px solid #E1E4E8;
    border-radius: 12px;
    padding: 20px;
}

#stat_value {
    font-size: 28px;
    font-weight: 800;
    color: #0047AB;
}

#stat_label {
    color: #6A737D;
    font-size: 14px;
}
"""
