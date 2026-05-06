import json
import os
import sys
from datetime import datetime, date

DATA_FILE = "data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {
        "streak": 0,
        "last_study_date": None,
        "monthly_wa_count": 0,
        "monthly_call_count": 0,
        "reminders": [],
        "weekly": {}
    }

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def update_streak(data):
    today = str(date.today())
    last = data.get("last_study_date")
    if last == today:
        return
    if last:
        from datetime import timedelta
        last_date = date.fromisoformat(last)
        if (date.today() - last_date).days == 1:
            data["streak"] = data.get("streak", 0) + 1
        elif (date.today() - last_date).days > 1:
            data["streak"] = 1
    else:
        data["streak"] = 1
    data["last_study_date"] = today

def log_reminder(reminder_type, channel):
    """
    reminder_type: devops | python | sql | evening
    channel: whatsapp | call
    """
    data = load_data()
    today = str(date.today())
    now = datetime.now().strftime("%H:%M")

    # Update streak on any WhatsApp reminder (first of the day)
    if channel == "whatsapp":
        update_streak(data)
        data["monthly_wa_count"] = data.get("monthly_wa_count", 0) + 1
    elif channel == "call":
        data["monthly_call_count"] = data.get("monthly_call_count", 0) + 1

    # Weekly tracking
    week_key = date.today().strftime("%Y-W%W")
    if week_key not in data["weekly"]:
        data["weekly"][week_key] = {}
    if today not in data["weekly"][week_key]:
        data["weekly"][week_key][today] = {
            "devops": {"whatsapp": False, "call": False},
            "python": {"whatsapp": False, "call": False},
            "sql": {"whatsapp": False, "call": False},
            "evening": {"whatsapp": False, "call": False}
        }
    data["weekly"][week_key][today][reminder_type][channel] = True

    # Recent reminders log (keep last 50)
    data["reminders"].append({
        "date": today,
        "time": now,
        "type": reminder_type,
        "channel": channel
    })
    data["reminders"] = data["reminders"][-50:]

    save_data(data)
    print(f"Logged: {reminder_type} / {channel} at {now}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python update_data.py <reminder_type> <channel>")
        print("Example: python update_data.py devops whatsapp")
        sys.exit(1)
    log_reminder(sys.argv[1], sys.argv[2])
