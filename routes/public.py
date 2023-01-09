from fastapi import APIRouter, Depends
from internal import schemas, crud
from internal.task import auth_task, basic_task
import logging


from dependencies.auth.auth_dp import user_authentication
route = APIRouter()

# Logging Info
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter(
    'Timestamp: %(asctime)s \n%(levelname)s: %(message)s \n\n', datefmt='%m/%d/%Y %I:%M:%S %p')
ch.setFormatter(formatter)
logger.addHandler(ch)


# Authenticate user
@route.post("/authenticate")
async def __home__(user_data: schemas.User_validation):
    try:
        token = await auth_task.login_validation(user_data)
        return token
    except Exception as e:
        logging.error(e)
        raise e


@route.get("/courses")
async def __get_courses__(auth=Depends(user_authentication)):
    if auth['status'] != 200:
        return auth['data']

    user = int(auth['data']['iduser'])
    courses = await crud.get_all_courses()
    id_ls = basic_task.Id.multi_decode(courses)
    crs_mod_count = {}
    courses_completed={}
    for id in id_ls: 
        module_obj = await crud.get_modules(id)
        crs_mod_count[id] = len(module_obj)
        get_completed_modules = await crud.module_status_for_courses(user, id)
        courses_completed[id] = len(get_completed_modules)
    
    result = basic_task.validate_completed_courses(courses_completed, crs_mod_count, courses)

    return result


    # # t = basic_task.get_complete_courses(user, id_ls)
    # return t
    # # return id_ls



@route.post("/modules:id={course_id}")
async def __get_modules__(course_id: str, auth=Depends(user_authentication)):
    if auth['status'] != 200:
        return auth['data']

    user = int(auth['data']['iduser'])
    decoded_id = basic_task.Id.decode(course_id)
    completed_modules = await crud.get_completed_modules(user, int(decoded_id))
    # return completed_modules
    modules = await crud.get_modules(int(decoded_id))
    not_completed_mods = basic_task.return_modules(
        completed_modules, modules)

    return not_completed_mods
    return auth


@route.post('/questions')
async def __questions__(ids: schemas.question_ids, auth=Depends(user_authentication)):
    if auth['status'] != 200:
        return auth['data']

    user = int(auth["data"]["iduser"])
    cids = basic_task.convert_tracking_ids(ids)
    raw_questions = await crud.get_questions(user, cids)
    return raw_questions


@route.post("/module-tracking")
async def __quiz_submission__(data: schemas.tracking_modules, auth=Depends(user_authentication)):
    if auth['status'] != 200:
        return auth['data']

    base64convert_data = basic_task.convert_tracking_ids(data)
    base64convert_data["user_id"] = int(auth["data"]["iduser"])
    duplicate = await crud.duplicate_checker(base64convert_data)
    try:
        if not duplicate['status']:
            await crud.insert_user_data(base64convert_data)
            return dict(status=200, msg="Submitted")
        else:
            await crud.update_user_data(duplicate["data"]["id"], base64convert_data)
            return dict(status=200, msg="Updated")
    except Exception as e:
        return dict(status=422, error=e)


@route.post("/module-submission")
async def __module_submission__(payload: schemas.Completed_Module, auth=Depends(user_authentication)):
    if auth['status'] != 200:
        return auth['data']


    data = dict(payload)
    data["uid"] = int(auth["data"]["iduser"])
    data_ = basic_task.convert_tracking_ids(data)
    if payload.score >= 50:
        try:
            await crud.insert_completed_modules(data_)
            await crud.remove_tracking_data(data_)
            return data_
        except Exception as e:
            return e
    else:
        await crud.remove_tracking_data(data_)
        # remove data from user tracking Table ONLY!
        return "deleted only"
