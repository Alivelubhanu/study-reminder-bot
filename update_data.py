import json
import os
import sys
from datetime import datetime, date, timedelta

DATA_FILE = "data.json"
START_DATE = date(2026, 5, 3)

DEVOPS_TOPICS = [
    "Demo1 — Introduction","Demo2 — Introduction","Introduction class",
    "Cloud and AWS introduction","AWS Account creation, plans",
    "IAM introduction, MFA, users, policies","IAM roles, Customer managed policy, Inline policy",
    "Introduction class and Cloud introduction (Revision)","AWS introduction and Account creation (Revision)",
    "IAM — Users, Policies, Groups, Permission boundaries, MFA, Customer signin URL",
    "Amazon S3 — ACLs, Public/Private access, Bucket policy, Presigned URL, Static website hosting",
    "LINUX CLASS-1","LINUX CLASS-2","LINUX CLASS-3","LINUX CLASS-4","LINUX CLASS-5",
    "S3 — Versioning, Storage classes, Lifecycle management, CORS",
    "AWS CLI","VPC Architecture, CIDR, Subnets, Route tables, Internet Gateway, VPC Lab",
    "NAT Gateways, Security groups, Elastic IPs","VPC Peering",
    "RDS — What is a database, AWS RDS, Launch RDS instance (Lab)","No class — revise RDS",
    "EC2 — Types, Benefits, Purchasing options, Launch EC2 (Lab)","AMI, EBS Volumes",
    "Load balancers, Lambda with EC2","GIT: Intro","GIT: Ignore, Reset, Ammend",
    "GIT: Revert, Branches, Merge, Stash","GIT: Cherry-pick, Rebase & GitHub","GITHUB",
    "No class — revise Git","MAVEN","JENKINS: Intro & Integration Git with Jenkins",
    "JENKINS: Parameters, Free Style Job options","No class — revise Jenkins",
    "JENKINS: Free Style Deployment","JENKINS: Master-Slave & User Management",
    "JENKINS Integration with NEXUS","JENKINS: Pipeline Jobs Part-1","JENKINS: Pipeline Jobs Part-2",
    "JENKINS: End to End Project","ANSIBLE: Intro and Basics of Playbooks",
    "ANSIBLE: Playbooks using YUM, ACTION, COMMAND, VARIABLES, TAGS, FILE, COPY, USER, GROUP",
    "ANSIBLE: Service, Conditions, Handlers, App Server, Vault, Git",
    "ANSIBLE: Jenkins Integration with Ansible, Debug & Setup modules",
    "No class — revise Ansible","No class — revise Ansible",
    "ANSIBLE: Adhoc Commands, Host Patterns","No class — revise Ansible",
    "ANSIBLE: Jinja2, Asynchronous & Poll, Strategies + Docker Intro",
    "DOCKER: Containers & Images","DOCKER: Dockerfile Part-1",
    "DOCKER: Dockerfile Part-2 & Integrate Docker with Jenkins","DOCKER: Docker Volumes",
    "DOCKER: Registry & Networks","DOCKER: Swarm","No class — revise Docker",
    "DOCKER: Compose","DOCKER: Dockerfiles for NodeJS, Java & Database",
    "DOCKER: ECS, Docker Directory Data & Stack","DOCKER: End to End Project",
    "KUBERNETES: Intro, Minikube & Pods","KUBERNETES: Labels, Selectors & KOPS",
    "KUBERNETES: Services","KUBERNETES: RC & RS",
    "KUBERNETES: Deployments, Namespaces & DaemonSet","No class — revise Kubernetes",
    "KUBERNETES: Volumes","KUBERNETES: Config Maps & Secrets","KUBERNETES: Jobs",
    "KUBERNETES: RBAC","Kubernetes self-revision","ELASTIC BEANSTALK",
    "KUBERNETES: Resource Quota","KUBERNETES: Helm & Stateful Applications",
    "No class — revise Helm","KUBERNETES: End to End Project",
    "TERRAFORM (class 1)","TERRAFORM (class 2)","TERRAFORM (class 3)","TERRAFORM (class 4)",
    "TERRAFORM (class 5)","TERRAFORM (class 6)","RESUME SESSION",
    "No class","No class","SCRIPTING PART-1","SCRIPTING PART-2",
    "MONOLITHIC PROJECT","No class","CLOUD WATCH",
]

PYTHON_TOPICS = [
    "Python intro, installation, print(), comments",
    "Variables & data types — int, float, str, bool",
    "Operators — arithmetic, comparison, logical",
    "String methods & f-string formatting",
    "Lists & list methods","Tuples & sets","Dictionaries",
    "If / elif / else conditions","For loops","While loops",
    "Functions — defining & calling","Function arguments & return values",
    "Lambda functions","File handling — read & write",
    "Exception handling — try / except","Modules & imports",
    "Standard library — math, random, datetime","List comprehensions",
    "Nested functions & scope","OOP — classes & objects",
    "OOP — attributes & methods","OOP — inheritance","OOP — encapsulation",
    "Regular expressions basics","Working with JSON","Working with CSV files",
    "Virtual environments & pip","Mini project: number guessing game",
    "Mini project: to-do list app","Python recap & practice",
]

SQL_TOPICS = [
    "SQL intro — databases & RDBMS concept",
    "Installing MySQL / using online SQL editor",
    "CREATE DATABASE & CREATE TABLE","Data types in SQL",
    "INSERT INTO — adding rows","SELECT — querying data",
    "WHERE clause & conditions","AND, OR, NOT operators",
    "ORDER BY & LIMIT","UPDATE & DELETE",
    "ALTER TABLE — add / drop columns","Primary key & foreign key",
    "DISTINCT & aliases","COUNT, SUM, AVG, MIN, MAX",
    "GROUP BY & HAVING","JOINS — INNER JOIN","JOINS — LEFT & RIGHT JOIN",
    "JOINS — FULL OUTER JOIN","Subqueries","UNION & UNION ALL",
    "IN, BETWEEN, LIKE","NULL handling — IS NULL, COALESCE",
    "Indexes — what and why","Views — creating & using",
    "Stored procedures basics","Transactions — COMMIT, ROLLBACK",
    "Window functions — ROW_NUMBER, RANK","CTEs — WITH clause",
    "Mini project: employee database queries","SQL recap & practice",
]

def get_topics():
    today = date.today()
    if today < START_DATE:
        return "Not started yet", "Not started yet", "Not started yet"
    weekday_count = 0
    d = START_DATE
    while d < today:
        if d.weekday() < 5:
            weekday_count += 1
        d += timedelta(days=1)
    devops = DEVOPS_TOPICS[weekday_count] if weekday_count < len(DEVOPS_TOPICS) else "DevOps revision"
    python = PYTHON_TOPICS[weekday_count] if weekday_count < len(PYTHON_TOPICS) else "Python revision"
    sql    = SQL_TOPICS[weekday_count]    if weekday_count < len(SQL_TOPICS)    else "SQL revision"
    return devops, python, sql

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
        "weekly": {},
        "today_topics": {}
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
        last_date = date.fromisoformat(last)
        if (date.today() - last_date).days == 1:
            data["streak"] = data.get("streak", 0) + 1
        elif (date.today() - last_date).days > 1:
            data["streak"] = 1
    else:
        data["streak"] = 1
    data["last_study_date"] = today

def log_reminder(reminder_type, channel):
    data = load_data()
    today = str(date.today())
    now = datetime.now().strftime("%H:%M")

    # Save today's real topics from send_reminder.py logic
    devops, python, sql = get_topics()
    data["today_topics"] = {
        "date": today,
        "devops": devops,
        "python": python,
        "sql": sql,
        "evening": "Revise all 3 topics"
    }

    if channel == "whatsapp":
        update_streak(data)
        data["monthly_wa_count"] = data.get("monthly_wa_count", 0) + 1
    elif channel == "call":
        data["monthly_call_count"] = data.get("monthly_call_count", 0) + 1

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

    data["reminders"].append({
        "date": today,
        "time": now,
        "type": reminder_type,
        "channel": channel
    })
    data["reminders"] = data["reminders"][-50:]

    save_data(data)
    print(f"Logged: {reminder_type} / {channel} at {now}")
    print(f"Topics saved: DevOps={devops}, Python={python}, SQL={sql}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python update_data.py <reminder_type> <channel>")
        sys.exit(1)
    log_reminder(sys.argv[1], sys.argv[2])
