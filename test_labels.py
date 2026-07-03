from email_memory import *

create_label("Career")

add_rule(
    "Career",
    "internship"
)

add_rule(
    "Career",
    "placement"
)

print(
    get_labels()
)

print(
    get_rules(
        "Career"
    )
)