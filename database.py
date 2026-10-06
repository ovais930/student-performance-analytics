from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["student_analytics"]

students_collection = db["students"]

print("Connected to MongoDB successfully!")
test_student = {
    "student_id": "TEST001",
    "name": "Ovais Nazir",
    "department": "CSE",
    "semester": 7,
    "city": "Jammu"
}

students_collection.insert_one(test_student)

print("Test student inserted successfully!")