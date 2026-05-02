import sys
import os
from datetime import datetime, date, timedelta
from twilio.rest import Client

TWILIO_ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN  = os.environ["TWILIO_AUTH_TOKEN"]
TWILIO_PHONE       = "whatsapp:+14155238886"
TWILIO_CALL_FROM   = os.environ["TWILIO_PHONE_NUMBER"]   # your Twilio number for calls
YOUR_WHATSAPP      = "whatsapp:+918500613315"
YOUR_PHONE         = "+918500613315"

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

START_DATE = date(2026, 5, 3)

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

def send_whatsapp(message):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(body=message, from_=TWILIO_PHONE, to=YOUR_WHATSAPP)
    print("WhatsApp message sent!")

def make_call(subject, topic):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    call_text = (
        f"Hello Alivelu! This is your study reminder. "
        f"It is time to start your {subject} session. "
        f"Today's topic is {topic}. "
        f"Please open your study material and start now. "
        f"Remember, consistency is the key to success. "
        f"Good luck! Start studying now!"
    )
    twiml = f"<Response><Say voice='alice' language='en-IN'>{call_text}</Say></Response>"
    call = client.calls.create(twiml=twiml, from_=TWILIO_CALL_FROM, to=YOUR_PHONE)
    print(f"Call made! SID: {call.sid}")

# Get action from command line: DevOps, Python, SQL, Evening, call-DevOps, call-Python, call-SQL
action = sys.argv[1] if len(sys.argv) > 1 else "DevOps"
devops, python, sql = get_topics()
today_str = datetime.now().strftime("%A, %d %b")

# Handle CALLS
if action == "call-DevOps":
    make_call("DevOps", devops)

elif action == "call-Python":
    make_call("Python", python)

elif action == "call-SQL":
    make_call("SQL", sql)

elif action == "call-Evening":
    make_call("evening revision", "DevOps, Python and SQL topics from today")

# Handle WHATSAPP MESSAGES
elif action == "DevOps":
    msg = (f"🔧 *Time to study DevOps!* — {today_str}\n\n"
           f"Today's topic:\n*{devops}*\n\n"
           f"📺 Open your study material and start now!\n"
           f"⏱️ Target: 2 hours of focused study\n\n"
           f"_(No reply? I will CALL you in 15 mins!)_ 📞")
    send_whatsapp(msg)

elif action == "Python":
    msg = (f"🐍 *Time to study Python!* — {today_str}\n\n"
           f"Today's topic:\n*{python}*\n\n"
           f"📺 Open your study material and start now!\n"
           f"⏱️ Target: 2 hours of focused study\n\n"
           f"_(No reply? I will CALL you in 15 mins!)_ 📞")
    send_whatsapp(msg)

elif action == "SQL":
    msg = (f"🗄️ *Time to study SQL!* — {today_str}\n\n"
           f"Today's topic:\n*{sql}*\n\n"
           f"📺 Open your study material and start now!\n"
           f"⏱️ Target: 2 hours of focused study\n\n"
           f"_(No reply? I will CALL you in 15 mins!)_ 📞")
    send_whatsapp(msg)

elif action == "Evening":
    msg = (f"📚 *Evening Revision* — {today_str}\n\n"
           f"🔧 DevOps: {devops}\n"
           f"🐍 Python: {python}\n"
           f"🗄️ SQL: {sql}\n\n"
           f"Revise all 3 topics for 30 mins! 💪")
    send_whatsapp(msg)
