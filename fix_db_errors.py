from database import get_db_connection

def clear_ai_errors():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Reset the summary for any email that has the decommissioned error or any AI error
        cursor.execute("""
            UPDATE emails
            SET summary = 'AI Analysis Pending / Skipped'
            WHERE summary LIKE 'AI Error:%' OR summary LIKE '%llama3-8b-8192%'
        """)
        
        rows_updated = cursor.rowcount
        conn.commit()
        conn.close()
        
        print(f"SUCCESS: Reset {rows_updated} emails with AI Errors.")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    clear_ai_errors()
