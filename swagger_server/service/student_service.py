import os
import tempfile
from functools import reduce

import pymongo.mongo_client
from tinydb import TinyDB, Query
import pymongo
from bson.objectid import ObjectId

mongo_client = pymongo.MongoClient(host='localhost', port=27017)
db = mongo_client['student']
student_collection = db['student_collection']

db_dir_path = tempfile.gettempdir()
db_file_path = os.path.join(db_dir_path, "students.json")
student_db = TinyDB(db_file_path)


def add(student=None):
    data = {
        'first_name': student.first_name,
        'last_name': student.first_name
    }

    res = student_collection.find_one(data)

    if res:
        return 'already exists', 409

    doc_id = student_collection.insert_one(data)

    student.student_id = doc_id
    return student.student_id

# def add(student=None):
#     queries = []
#     query = Query()
#     queries.append(query.first_name == student.first_name)
#     queries.append(query.last_name == student.last_name)
#     query = reduce(lambda a, b: a & b, queries)
#     res = student_db.search(query)
#     if res:
#         return 'already exists', 409

#     print(student.to_dict())
#     doc_id = student_db.insert(student.to_dict())
#     student.student_id = doc_id
#     return student.student_id


def get_by_id(student_id=None, subject=None):
    try:
        student = student_collection.find_one({'_id': ObjectId(student_id)})
        if not student:
            return 'not found', 404
        
        student['student_id'] = str(student['_id'])
        return student
    except Exception as e:
        print(str(e))

# def get_by_id(student_id=None, subject=None):
#     student = student_db.get(doc_id=int(student_id))
#     if not student:
#         return 'not found', 404
#     student['student_id'] = student_id

#     print(student)
#     return student

def delete(student_id=None):
    try:
        student = student_db.get(doc_id=int(student_id))
        res = student_collection.delete_one({'_id': ObjectId(student_id)})
        if res.deleted_count == 0:
            return 'not found', 404
        
        return student_id
    except Exception as e:
        print(str(e))
# def delete(student_id=None):
#     student = student_db.get(doc_id=int(student_id))
#     if not student:
#         return 'not found', 404
#     student_db.remove(doc_ids=[int(student_id)])
#     return student_id