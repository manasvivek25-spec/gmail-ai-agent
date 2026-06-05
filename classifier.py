def classify(subject):

    subject = subject.lower()

    if "mess" in subject:
        return "MESS"

    elif "intern" in subject:
        return "INTERNSHIP"

    elif "hackathon" in subject:
        return "INTERNSHIP"

    elif "library" in subject:
        return "ADMIN"

    elif "guest house" in subject:
        return "ADMIN"

    elif "yoga" in subject:
        return "EVENT"

    elif "bicycle" in subject:
        return "EVENT"

    else:
        return "OTHER"