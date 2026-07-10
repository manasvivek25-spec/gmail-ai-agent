from database import get_db_connection

def clear_skipped_emails():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Delete emails that failed AI analysis
    cursor.execute("DELETE FROM emails WHERE summary = 'AI Analysis Pending / Skipped'")
    deleted = cursor.rowcount
    print(f"Deleted {deleted} skipped emails from database to force re-analysis.")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    clear_skipped_emails()
