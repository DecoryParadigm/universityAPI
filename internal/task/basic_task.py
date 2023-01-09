import base64
from internal import crud


class Id:

    def encode(data) -> str:
        raw_data = str(data)
        data = raw_data.encode()
        byte_data = base64.b64encode(data)
        base64_str = byte_data.decode('ascii')
        return base64_str

    def decode(b64) -> str:
        data = b64.encode('ascii')
        byte_data = base64.b64decode(data)
        decoded_str = byte_data.decode('ascii')
        return decoded_str

    def multi_decode(obj): 
        course_ids = []
        for i in obj: 
            pure_id = Id.decode(i['id'])
            course_ids.append(int(pure_id))
        return course_ids


def secure_id(obj) -> list:
    registered_ids = ["id", "quiz_id", "module_id",
                      "user_id", "question_id", "uid", "iduser"]

    output: list = []
    for o in obj:
        conv = dict(o)
        conv['id'] = Id.encode(o['id'])
        for idSelection in registered_ids:
            if idSelection in conv:
                conv[idSelection] = Id.encode(o[idSelection])
        output.append(conv)
    return output


def convert_tracking_ids(obj: dict):
    registered_ids = ["id", "quiz_id", "module_id",
                      "user_id", "uid", "iduser"]
    data = dict(obj)
    for o in data:
        if o in registered_ids and (type(data[o]) is str) == True:
            data[o] = int(Id.decode(data[o]))
    return data


def question_object(raw_data, submitted, answers) -> list:
    output = []
    submitted_questions = {
        "submitted": []
    }
    for obj in raw_data:
        data = dict(obj)  # RAW DATA OBJ
        if data['id'] in answers:
            data['answers'] = answers[data['id']]
        for s in submitted:
            if data['id'] == s['question_id']:
                submitted_questions["submitted"].append(
                    {data['id']: s['ans_value']})
        output.append(data)

    # output.append(submitted_questions)
    total_questions = len(raw_data)
    return remove_submitted_data(output, submitted_questions, total_questions)


def remove_submitted_data(obj, submitted_obj, total_count):
    output = []
    key_list = []
    data = obj
    for k in submitted_obj["submitted"]:
        ky = list(k.keys())
        key_list.append(ky[0])

    for o in data:
        if o['id'] not in key_list:
            output.append(o)
    output.append({"count": total_count})
    output.append(submitted_obj)
    return output


def segment_ans(raw_data):
    output = {}
    for o in raw_data:
        ans_obj = dict(o)
        if ans_obj['questions_id'] not in output:
            output[ans_obj['questions_id']] = [ans_obj]
        else:
            output[ans_obj['questions_id']].append(ans_obj)
    return output


def return_modules(completed: list, rawModules: list):
    # need to refactor
    output_mods = []
    if completed == []:
        return rawModules
    else:
        for modules in completed:
            for rawData in rawModules:
                if modules["module_id"] == rawData["id"]:
                    if rawData in output_mods:
                        pass
                    else:
                        rawData['completed'] = True
                else: 
                    rawData['completed'] = False
                output_mods.append(rawData)
        return output_mods




def validate_completed_courses(cc, data_count, data):
    output = []
    for course in data: # Iterate through the obj
        crsId = int(Id.decode(course['id']))  # Collect data id
        if crsId in data_count and crsId in cc: 
           if data_count[crsId] == cc[crsId]:
                course['completed']= True
           else: 
                course['completed']=False

        output.append(course)
    return output



