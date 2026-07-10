import os

with open('email_memory.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. save_tag
old_save_tag = """def save_tag(
    email_id,
    tag
):"""
new_save_tag = """def save_tag(
    user_id,
    email_id,
    tag
):"""
content = content.replace(old_save_tag, new_save_tag)

old_save_tag_insert = """    INSERT INTO email_tags (
        email_id,
        tag
    )
    VALUES (%s, %s)"""
new_save_tag_insert = """    INSERT INTO email_tags (
        user_id,
        email_id,
        tag
    )
    VALUES (%s, %s, %s)"""
content = content.replace(old_save_tag_insert, new_save_tag_insert)

old_save_tag_values = """    (
        email_id,
        tag
    ))"""
new_save_tag_values = """    (
        user_id,
        email_id,
        tag
    ))"""
content = content.replace(old_save_tag_values, new_save_tag_values)


# 2. record_action
old_record_action = """def record_action(
    email_id,
    action
):"""
new_record_action = """def record_action(
    user_id,
    email_id,
    action
):"""
content = content.replace(old_record_action, new_record_action)

old_record_insert = """    INSERT INTO user_actions (
        email_id,
        action,
        action_time
    )
    VALUES (
        %s,
        %s,"""
new_record_insert = """    INSERT INTO user_actions (
        user_id,
        email_id,
        action,
        action_time
    )
    VALUES (
        %s,
        %s,
        %s,"""
content = content.replace(old_record_insert, new_record_insert)

old_record_args = """    (
        email_id,
        action
    ))"""
new_record_args = """    (
        user_id,
        email_id,
        action
    ))"""
content = content.replace(old_record_args, new_record_args)


# 3. get_action_score
old_action_score = """def get_action_score(
    email_id
):"""
new_action_score = """def get_action_score(
    user_id,
    email_id
):"""
content = content.replace(old_action_score, new_action_score)

old_action_score_args = """    (
        email_id,
    ))"""
new_action_score_args = """    (
        user_id,
        email_id,
    ))"""
content = content.replace(old_action_score_args, new_action_score_args)


# 4. recalculate_email_importance
old_recalc_call = "interest_score += get_interest_score(tag)"
new_recalc_call = "interest_score += get_interest_score(user_id, tag)"
content = content.replace(old_recalc_call, new_recalc_call)


# 5. toggle_bookmark
old_toggle = "recalculate_email_importance(email_id)"
new_toggle = "recalculate_email_importance(user_id, email_id)"
content = content.replace(old_toggle, new_toggle)


# 6. delete_rule
old_del_rule = """def delete_rule(
    label_name,
    keyword
):"""
new_del_rule = """def delete_rule(
    user_id,
    label_name,
    keyword
):"""
content = content.replace(old_del_rule, new_del_rule)

old_del_rule_args = """    (
        label_name,
        keyword.lower()
    ))"""
new_del_rule_args = """    (
        user_id,
        label_name,
        keyword.lower()
    ))"""
content = content.replace(old_del_rule_args, new_del_rule_args)


# 7. count_emails_for_label
old_count = """def count_emails_for_label(
    label_name
):"""
new_count = """def count_emails_for_label(
    user_id,
    label_name
):"""
content = content.replace(old_count, new_count)

old_count_args = """    (
        label_name,
    ))"""
new_count_args = """    (
        user_id,
        label_name,
    ))"""
content = content.replace(old_count_args, new_count_args)


# 8. get_emails_metadata_by_ids
old_get_by_ids = """    WHERE email_id IN ({placeholders})
    ORDER BY received_time DESC
    """, email_ids)"""
new_get_by_ids = """    WHERE user_id=%s AND email_id IN ({placeholders})
    ORDER BY received_time DESC
    """, [user_id] + email_ids)"""
content = content.replace(old_get_by_ids, new_get_by_ids)


# 9. get_recommended_emails_metadata
old_get_rec = """    FROM emails
    ORDER BY importance DESC
    LIMIT %s
    """, (user_id, limit))"""
new_get_rec = """    FROM emails
    WHERE user_id=%s
    ORDER BY importance DESC
    LIMIT %s
    """, (user_id, limit))"""
content = content.replace(old_get_rec, new_get_rec)


# 10. get_all_deadlines
old_get_dead = """    WHERE deadline IS NOT NULL
      AND deadline != ''
      AND deadline != 'NONE'
      AND deadline >= %s
    """, (today_str,))"""
new_get_dead = """    WHERE user_id=%s
      AND deadline IS NOT NULL
      AND deadline != ''
      AND deadline != 'NONE'
      AND deadline >= %s
    """, (user_id, today_str))"""
content = content.replace(old_get_dead, new_get_dead)


# 11. get_category_counts
old_get_cat = """    SELECT category, COUNT(*)
    FROM emails
    WHERE category IS NOT NULL AND category != '' AND category != 'IGNORE'
    GROUP BY category
    ORDER BY COUNT(*) DESC
    """)"""
new_get_cat = """    SELECT category, COUNT(*)
    FROM emails
    WHERE user_id=%s AND category IS NOT NULL AND category != '' AND category != 'IGNORE'
    GROUP BY category
    ORDER BY COUNT(*) DESC
    """, (user_id,))"""
content = content.replace(old_get_cat, new_get_cat)

with open('email_memory.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: email_memory.py deep patched for multi-tenant")
