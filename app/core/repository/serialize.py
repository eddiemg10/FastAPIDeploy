
def serializeDict(a) -> dict:
    id_object = "_id"
    return {**{i: str(a[i]) for i in a if id_object in i}, **{i: a[i] for i in a if id_object not in i} }

def serializeList(items) -> list:
    return [serializeDict(a) for a in items]
