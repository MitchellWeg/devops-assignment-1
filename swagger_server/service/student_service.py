import os
import tempfile
from functools import reduce

import pymongo.mongo_client
from tinydb import TinyDB, Query
from flask import jsonify
import pymongo
from bson.objectid import ObjectId
import json

mongo_client = pymongo.MongoClient(host='mongo', port=27017)
db = mongo_client['student']
student_collection = db['student_collection']

# db_dir_path = tempfile.gettempdir()
# db_file_path = os.path.join(db_dir_path, "students.json")
# student_db = TinyDB(db_file_path)


def add(student=None):
    data = {
        'first_name': str(student.first_name),
        'last_name': str(student.last_name),
    }

    res = student_collection.find_one(data)

    if res:
        return 'already exists', 409

    doc_id = student_collection.insert_one(student.to_dict())

    student.student_id = str(doc_id.inserted_id)
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
        if not ObjectId.is_valid(student_id):
            return jsonify({'error': 'Invalid ObjectId'}), 400

        student = student_collection.find_one({'_id': ObjectId(student_id)})
        if not student:
            return jsonify({'message': 'not found'}), 404

        student['student_id'] = str(student['_id'])
        del student['_id']
        grade_records = student['grade_records']

        return jsonify(student)

    except Exception as e:
        print('Error:', str(e))
        return jsonify({'error': 'Internal Server Error'}), 500

# def get_by_id(student_id=None, subject=None):
#     student = student_db.get(doc_id=int(student_id))
#     if not student:
#         return 'not found', 404
#     student['student_id'] = student_id

#     print(student)
#     return student

def delete(student_id=None):
    try:
        res = student_collection.delete_one({'_id': ObjectId(student_id)})
        if res.deleted_count == 0:
            return 'not found', 404
        
        return json.dumps(student_id)
    except Exception as e:
        print(str(e))
# def delete(student_id=None):
#     student = student_db.get(doc_id=int(student_id))
#     if not student:
#         return 'not found', 404
#     student_db.remove(doc_ids=[int(student_id)])
#     return student_id