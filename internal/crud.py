from . import models
from database.quiz_db import database
from internal.task import basic_task


async def getUsers():
    query = models.Users.select()
    return await database.fetch_all(query)


async def validate_email(email):
    query = models.Users.select().where(
        models.Users.c.email == f"{email}")
    return await database.fetch_all(query)


async def get_all_courses():
    query = models.Quiz.select()
    raw = await database.fetch_all(query)
    return basic_task.secure_id(raw)


async def get_modules(id: int):
    query = models.Modules.select().where(models.Modules.c.quiz_id == id)
    raw = await database.fetch_all(query)
    return basic_task.secure_id(raw)


async def get_questions(user, ids):
    query = models.Questions.select().where(
        models.Questions.c.modules_id == ids["module_id"])
    raw = await database.fetch_all(query)
    submitted = await get_submitted_questions(user, ids)

    ans = await get_answers()
    ans_converter = basic_task.segment_ans(ans)
    output = basic_task.question_object(raw, submitted, ans_converter)
    return output


async def get_submitted_questions(user, ids):
    query = models.user_tracking.select().where(
        (models.user_tracking.c.user_id == user) &
        (models.user_tracking.c.quiz_id == ids["quiz_id"]) &
        (models.user_tracking.c.module_id == ids["module_id"])
    )
    results = await database.fetch_all(query)
    return results


async def get_answers():
    query = models.Answers.select()
    raw = await database.fetch_all(query)
    return raw


async def insert_user_data(data):
    query = models.user_tracking.insert().values(**data)
    await database.execute(query)
    return


async def update_user_data(id, data):
    query = models.user_tracking.update().where(
        models.user_tracking.c.id == id).values(**data)
    await database.execute(query)
    return


async def insert_completed_modules(data):
    query = models.Modules_completed.insert().values(**data)
    await database.execute(query)
    return


'''
Tracking Functions Below
'''


async def duplicate_checker(data: dict):
    query = models.user_tracking.select().where(
        (models.user_tracking.c.quiz_id == int(data["quiz_id"])) &
        (models.user_tracking.c.module_id == int(data["module_id"])) &
        (models.user_tracking.c.question_id == int(data["question_id"]))
    )
    if await database.fetch_all(query) == []:
        return dict(status=False)
    else:
        data = await database.fetch_all(query)
        return dict(status=True, data=data[0])

# Check module completed table


async def get_completed_modules(uid: int, id: int):
    query = models.Modules_completed.select().where(
        (models.Modules_completed.c.uid == uid) &
        (models.Modules_completed.c.module_id == id) &
        (models.Modules_completed.c.score >= 50)
    )
    completed = await database.fetch_all(query)
    return basic_task.secure_id(completed)


async def remove_tracking_data(obj: dict):
    mod = models.user_tracking
    query = mod.delete().where(
        (mod.c.user_id == obj["uid"]) &
        (mod.c.module_id == obj["module_id"]) &
        (mod.c.quiz_id == obj["quiz_id"])
    )
    await database.execute(query)
    return


async def module_status_for_courses(uid: int, course_id:int): 
    query = models.Modules_completed.select().where(
        (models.Modules_completed.c.uid == uid) &
        (models.Modules_completed.c.quiz_id == course_id)

    )
    completed = await database.fetch_all(query)
    return completed