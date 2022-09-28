# def serializeDict(item) -> dict:
#     return {
#         "id": str(item["_id"]),
#         "firstname": item["firstname"],
#         "lastname": item["lastname"],
#         "email": item["email"],
#         "password": item["password"],
#         "sub": item["sub"],
#         "program": item["program"],
#         "statistic": item["statistic"],
#         "form": item["form"],
#     }


def serializeList(entity) ->list:
    return [serializeDict(item) for item in entity]

def serializeDict(a) -> dict:
    result = {}
    for i in a:
        if i == '_id':
            result['_id'] = str(a[i])
        else:
            result[i] = a[i]
    return result
