# Database models done here
from sqlalchemy import Column, Integer, String, Table
from database.quiz_db import metadata

Users = Table(
    "user",
    metadata,
    Column("iduser", Integer, primary_key=True),
    Column("name", String(100)),
    Column("location", String(100)),
    Column("email", String(150)),
)


'''
Quiz Tables Below
'''

Quiz = Table(
    "courses",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(100)),
    Column("duration", String(100)),
    Column("about", String(100))
)

Modules = Table(
    "modules",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(100)),
    Column("duration", String(20)),
    Column("presenter", String(100)),
    Column("video_url", String(1000)),
    Column("quiz_id", Integer)
)

Questions = Table(
    "questions",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("questions", String(1000)),
    Column("description", String(2000)),
    Column("modules_id", Integer)
)

Answers = Table(
    "answers",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("answer", String(1000)),
    Column("Status", String(20)),
    Column("questions_id", Integer)
)


'''
Tracking models
'''
user_tracking = Table(
    "user_tracking",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer),
    Column("quiz_id", Integer),
    Column("module_id", Integer),
    Column("question_id", Integer),
    Column("ans_value", Integer)
)

Quiz_completed = Table(
    "quiz_completed",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("uid", Integer),
    Column("quiz_id", Integer)
)
Modules_completed = Table(
    "module_completed",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("uid", Integer),
    Column("quiz_id", Integer),
    Column("module_id", Integer),
    Column("score", Integer)
)
