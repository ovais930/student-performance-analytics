from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["student_analytics"]

students_collection = db["students"]
new_student = {
    "student_id": "STU99999",
    "name": "Test Student",
    "age": 21,
    "gender": "Male",
    "department": "CSE",
    "semester": 7,
    "city": "Jammu",
    "attendance": 90,
    "mathematics_marks": 85,
    "dbms_marks": 88,
    "computer_networks_marks": 82,
    "programming_marks": 91,
    "total_marks": 346,
    "percentage": 86.5,
    "cgpa": 8.65,
    "placement_status": "Not Placed"
}

result = students_collection.insert_one(new_student)

print("Student inserted successfully!")
print("Inserted ID:", result.inserted_id)
student = students_collection.find_one(
    {"student_id": "STU99999"}
)

print("\nStudent found:")
print(student)
result = students_collection.update_one(
    {"student_id": "STU99999"},
    {"$set": {"attendance": 95}}
)

print("\nStudent updated!")
print("Documents modified:", result.modified_count)
result = students_collection.delete_one(
    {"student_id": "STU99999"}
)

print("\nStudent deleted!")
print("Documents deleted:", result.deleted_count)