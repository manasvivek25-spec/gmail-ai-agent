
from database import get_db_connection
import psycopg2.extras
from datetime import datetime


def email_exists(email_id):

    try:

        with get_db_connection() as conn:

            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT email_id
                FROM emails
                WHERE email_id=%s
                """,
                (email_id,)
            )

            result = cursor.fetchone()

            return result is not None

    except Exception as e:

        print(
            f"Database Error: {e}"
        )

        return False


def save_email(
    email_id,
    subject,
    body,
    category,
    summary,
    deadline,
    relevance,
    importance,
    received_time,
    adaptive_action
):

    import json
    if isinstance(summary, list):
        try:
            summary_str = "\n".join([str(item) if not isinstance(item, dict) else json.dumps(item) for item in summary])
        except Exception:
            summary_str = str(summary)
    else:
        summary_str = str(summary)

    try:

        with get_db_connection() as conn:

            cursor = conn.cursor()

            cursor.execute("""
INSERT INTO emails (
    email_id,
    subject,
    body,
    category,
    summary,
    deadline,
    relevance,
    importance,
    received_time,
    adaptive_action
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (email_id) DO UPDATE SET
    subject = EXCLUDED.subject,
    body = EXCLUDED.body,
    category = EXCLUDED.category,
    summary = EXCLUDED.summary,
    deadline = EXCLUDED.deadline,
    relevance = EXCLUDED.relevance,
    importance = EXCLUDED.importance,
    received_time = EXCLUDED.received_time,
    adaptive_action = EXCLUDED.adaptive_action
""",
(
    email_id,
    subject,
    body,
    category,
    summary_str,
    deadline,
    relevance,
    importance,
    received_time,
    adaptive_action
))

            conn.commit()

            print(
                f"SAVED TO DATABASE: {subject}"
            )

    except Exception as e:

        print(
            f"Database Save Error: {e}"
        )


def get_email_count():

    try:

        with get_db_connection() as conn:

            cursor = conn.cursor()

            cursor.execute("""
            SELECT COUNT(*)
            FROM emails
            """)

            count = cursor.fetchone()[0]

            return count

    except Exception as e:

        print(
            f"Database Count Error: {e}"
        )

        return 0
def create_label(label_name):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO user_labels (
        label_name
    )
    VALUES (%s)
    ON CONFLICT (label_name) DO NOTHING
    """, (label_name,))

    conn.commit()
    conn.close()
def delete_label(label_name):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM user_labels
    WHERE label_name=%s
    """, (label_name,))

    cursor.execute("""
    DELETE FROM label_rules
    WHERE label_name=%s
    """, (label_name,))

    conn.commit()
    conn.close()
def get_labels():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT label_name
    FROM user_labels
    ORDER BY label_name
    """)

    labels = cursor.fetchall()

    conn.close()

    return [row[0] for row in labels]
def add_rule(
    label_name,
    keyword
):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT 1
    FROM label_rules
    WHERE label_name=%s
    AND keyword=%s
    """,
    (
        label_name,
        keyword.lower()
    ))

    exists = cursor.fetchone()

    if not exists:

        cursor.execute("""
        INSERT INTO label_rules (
            label_name,
            keyword
        )
        VALUES (%s, %s)
        """,
        (
            label_name,
            keyword.lower()
        ))

        conn.commit()

    conn.close()
def get_rules(label_name):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT keyword
    FROM label_rules
    WHERE label_name=%s
    """, (label_name,))

    rows = cursor.fetchall()

    conn.close()

    return [
        row[0]
        for row in rows
    ]
def assign_label(email_id, label_name):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO email_labels (
        email_id,
        label_name
    )
    VALUES (%s, %s)
    ON CONFLICT (email_id, label_name) DO NOTHING
    """, (
        email_id,
        label_name
    ))

    conn.commit()
    conn.close()
def get_emails_for_label(label_name):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT email_id
    FROM email_labels
    WHERE label_name=%s
    """, (label_name,))

    rows = cursor.fetchall()

    conn.close()

    return [row[0] for row in rows]

def get_all_labels():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT label_name
    FROM user_labels
    """)

    rows = cursor.fetchall()

    conn.close()

    return [row[0] for row in rows]

def save_tag(
    email_id,
    tag
):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO email_tags (
        email_id,
        tag
    )
    VALUES (%s, %s)
    ON CONFLICT (email_id, tag) DO NOTHING
    """,
    (
        email_id,
        tag
    ))
    

    conn.commit()
    conn.close()
def record_action(
    email_id,
    action
):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO user_actions (
        email_id,
        action,
        action_time
    )
    VALUES (
        %s,
        %s,
        CURRENT_TIMESTAMP
    )
    """,
    (
        email_id,
        action
    ))

    conn.commit()
    conn.close()


def get_action_score(
    email_id
):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM user_actions
    WHERE email_id=%s
    """,
    (
        email_id,
    ))

    score = cursor.fetchone()[0]

    conn.close()

    return score


def get_deadline_score(deadline):
    if deadline == "NONE" or deadline == "":
        return 0
    try:
        deadline_date = datetime.strptime(deadline, "%Y-%m-%d").date()
        today = datetime.today().date()
        days = (deadline_date - today).days
        if days <= 0: return 20
        elif days <= 1: return 15
        elif days <= 3: return 10
        elif days <= 7: return 5
        return 0
    except:
        return 0

def calculate_importance(
    relevance,
    deadline_score,
    interest_score,
    action_score,
    received_time,
    is_bookmarked=0
):
    # Recency score (time decay)
    recency_score = 0
    if received_time:
        try:
            ts = float(received_time)
            if ts > 10**11: ts = ts / 1000
            email_date = datetime.fromtimestamp(ts).date()
            today = datetime.today().date()
            days_old = (today - email_date).days
            if days_old <= 1: recency_score = 10
            elif days_old <= 3: recency_score = 5
            elif days_old <= 7: recency_score = 2
            else: recency_score = -min(5, int(days_old / 7)) # Decay over time
        except Exception:
            pass

    importance = (
        (relevance * 5) +
        (deadline_score * 3) +
        interest_score +
        (action_score * 2) +
        recency_score +
        (50 if is_bookmarked else 0)
    )
    return importance

def recalculate_email_importance(email_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT relevance, deadline, received_time, is_bookmarked FROM emails WHERE email_id=%s", (email_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return
    relevance, deadline, received_time, is_bookmarked = row

    # Get interest score from tags
    cursor.execute("SELECT tag_name FROM email_tags WHERE email_id=%s", (email_id,))
    tags = [t[0] for t in cursor.fetchall()]
    interest_score = 0
    for tag in tags:
        interest_score += get_interest_score(tag)
        
    deadline_score = get_deadline_score(deadline)
    
    new_importance = calculate_importance(
        relevance=relevance,
        deadline_score=deadline_score,
        interest_score=interest_score,
        action_score=0, # Can be expanded later
        received_time=received_time,
        is_bookmarked=is_bookmarked
    )
    
    cursor.execute("UPDATE emails SET importance=%s WHERE email_id=%s", (new_importance, email_id))
    conn.commit()
    conn.close()

def toggle_bookmark(email_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE emails
    SET is_bookmarked = 1 - is_bookmarked
    WHERE email_id=%s
    """, (email_id,))

    conn.commit()
    conn.close()
    
    recalculate_email_importance(email_id)
def delete_rule(
    label_name,
    keyword
):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM label_rules
    WHERE label_name=%s
    AND keyword=%s
    """,
    (
        label_name,
        keyword.lower()
    ))

    conn.commit()
    conn.close()
def count_emails_for_label(
    label_name
):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM email_labels
    WHERE label_name=%s
    """,
    (
        label_name,
    ))

    count = cursor.fetchone()[0]

    conn.close()

    return count
def get_email_tags(email_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT tag
    FROM email_tags
    WHERE email_id=%s
    """,
    (email_id,))

    rows = cursor.fetchall()

    conn.close()

    return [
        row[0]
        for row in rows
    ]
def get_email_labels(email_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT label_name
    FROM email_labels
    WHERE email_id=%s
    """,
    (email_id,))

    rows = cursor.fetchall()

    conn.close()

    return [
        row[0]
        for row in rows
    ]
def update_interest(tag):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO user_interests(
        keyword,
        score
    )
    VALUES(%s,1)

    ON CONFLICT(keyword)
    DO UPDATE SET
    score = user_interests.score + 1
    """,
    (tag,))

    conn.commit()
    conn.close()
def get_interest_score(tag):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT score
    FROM user_interests
    WHERE keyword=%s
    """,
    (tag,))

    row = cursor.fetchone()

    conn.close()

    return row[0] if row else 0
def get_top_interests(limit=5):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT keyword,
           score
    FROM user_interests
    ORDER BY score DESC
    LIMIT %s
    """, (limit,))

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_top_tags(limit=10):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT tag,
           COUNT(*) as count
    FROM email_tags
    GROUP BY tag
    ORDER BY count DESC
    LIMIT %s
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]


def get_all_emails_metadata(limit=50):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT email_id,
           subject,
           summary,
           received_time,
           relevance,
           importance,
           is_bookmarked,
           category
    FROM emails
    WHERE category != 'PHD_SEMINAR'
    ORDER BY received_time DESC
    LIMIT %s
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    emails = []
    for row in rows:
        ts = row[3]
        time_str = str(ts)
        if isinstance(ts, (int, float)):
            try:
                # Gmail timestamps are often in milliseconds
                if ts > 10**11:
                    ts = ts / 1000
                time_str = datetime.fromtimestamp(ts).strftime("%d %b, %H:%M")
            except Exception as e:
                print(f"Timestamp error: {e} for value {ts}")
        
        emails.append({
            "email_id": row[0],
            "subject": row[1],
            "summary": row[2],
            "time": time_str,
            "relevance": row[4],
            "importance": row[5],
            "is_starred": bool(row[6]),
            "category": row[7],
            "priority": "Critical" if row[5] >= 25 else "High" if row[5] >= 15 else "Medium" if row[5] >= 8 else "Low"
        })
    return emails


def get_emails_metadata_by_ids(email_ids):

    if not email_ids:
        return []

    conn = get_db_connection()
    cursor = conn.cursor()

    placeholders = ",".join(["%s"] * len(email_ids))
    cursor.execute(f"""
    SELECT email_id,
           subject,
           summary,
           received_time,
           relevance,
           importance,
           is_bookmarked,
           category
    FROM emails
    WHERE email_id IN ({placeholders})
    ORDER BY received_time DESC
    """, email_ids)

    rows = cursor.fetchall()
    conn.close()

    emails = []
    for row in rows:
        ts = row[3]
        time_str = str(ts)
        if isinstance(ts, (int, float)):
            try:
                # Gmail timestamps are often in milliseconds
                if ts > 10**11:
                    ts = ts / 1000
                time_str = datetime.fromtimestamp(ts).strftime("%d %b, %H:%M")
            except Exception as e:
                print(f"Timestamp error: {e} for value {ts}")
        
        emails.append({
            "email_id": row[0],
            "subject": row[1],
            "summary": row[2],
            "time": time_str,
            "relevance": row[4],
            "importance": row[5],
            "is_starred": bool(row[6]),
            "category": row[7],
            "priority": "Critical" if row[5] >= 25 else "High" if row[5] >= 15 else "Medium" if row[5] >= 8 else "Low"
        })
    return emails


def get_recommended_emails_metadata(limit=20):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT email_id,
           subject,
           summary,
           received_time,
           relevance,
           importance,
           is_bookmarked,
           category
    FROM emails
    ORDER BY importance DESC
    LIMIT %s
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    emails = []
    for row in rows:
        ts = row[3]
        time_str = str(ts)
        if isinstance(ts, (int, float)):
            try:
                # Gmail timestamps are often in milliseconds
                if ts > 10**11:
                    ts = ts / 1000
                time_str = datetime.fromtimestamp(ts).strftime("%d %b, %H:%M")
            except Exception as e:
                print(f"Timestamp error: {e} for value {ts}")
        
        emails.append({
            "email_id": row[0],
            "subject": row[1],
            "summary": row[2],
            "time": time_str,
            "relevance": row[4],
            "importance": row[5],
            "is_starred": bool(row[6]),
            "category": row[7],
            "priority": "Critical" if row[5] >= 25 else "High" if row[5] >= 15 else "Medium" if row[5] >= 8 else "Low"
        })
    return emails


def get_email_details(email_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT subject,
           summary,
           body,
           deadline,
           importance,
           relevance,
           category
    FROM emails
    WHERE email_id=%s
    """, (email_id,))

    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "subject": row[0],
        "summary": row[1],
        "body": row[2],
        "deadline": row[3],
        "importance": row[4],
        "relevance": row[5],
        "category": row[6] or 'Unknown'
    }


def get_all_deadlines():

    conn = get_db_connection()
    cursor = conn.cursor()

    today_str = datetime.today().strftime("%Y-%m-%d")

    cursor.execute("""
    SELECT email_id,
           subject,
           deadline,
           received_time,
           summary,
           importance
    FROM emails
    WHERE deadline IS NOT NULL
      AND deadline != ''
      AND deadline != 'NONE'
      AND deadline >= %s
    """, (today_str,))

    rows = cursor.fetchall()
    conn.close()

    today = datetime.today().date()
    deadlines = []

    for row in rows:
        email_id, subject, deadline_str, received_time, summary, importance = row
        
        # Clean the deadline string
        deadline_str = deadline_str.strip()
        
        formats = ["%Y-%m-%d", "%d/%m/%y", "%d/%m/%Y", "%d-%m-%Y"]
        deadline_date = None

        for fmt in formats:
            try:
                deadline_date = datetime.strptime(deadline_str, fmt).date()
                break
            except:
                pass

        if deadline_date and deadline_date >= today:
            days_left = (deadline_date - today).days
            deadlines.append({
                "email_id": email_id,
                "subject": subject,
                "deadline": deadline_str,
                "days_left": days_left,
                "received_time": received_time,
                "summary": summary,
                "importance": importance,
                "priority": "Critical" if importance >= 25 else "High" if importance >= 15 else "Medium" if importance >= 8 else "Low"
            })

    deadlines.sort(key=lambda x: x["days_left"])
    return deadlines


def get_category_counts():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT category, COUNT(*)
    FROM emails
    WHERE category IS NOT NULL AND category != '' AND category != 'IGNORE'
    GROUP BY category
    ORDER BY COUNT(*) DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return {row[0]: row[1] for row in rows}

def get_emails_by_category(category):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT email_id
    FROM emails
    WHERE category=%s
    ORDER BY received_time DESC
    """, (category,))
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]
