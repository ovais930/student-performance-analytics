from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["student_analytics"]

students_collection = db["students"]

print("Connected to MongoDB!")
cse_count = students_collection.count_documents(
    {"department": "CSE"}
)

print("Total CSE students:", cse_count)
high_cgpa_students = students_collection.find(
    {"cgpa": {"$gt": 8.0}}
)

count = 0

for student in high_cgpa_students:
    count += 1

print("Students with CGPA > 8.0:", count)
top_students = students_collection.find().sort(
    "percentage", -1
).limit(10)

print("\nTop 10 Students:")

for student in top_students:
    print(
        student["student_id"],
        "-",
        student["name"],
        "-",
        student["percentage"],
        "%"
    )
department_analysis = students_collection.aggregate([
    {
        "$group": {
            "_id": "$department",
            "total_students": {"$sum": 1}
        }
    },
    {
        "$sort": {
            "total_students": -1
        }
    }
])

print("\nDepartment-wise Student Count:")

for result in department_analysis:
    print(
        result["_id"],
        "→",
        result["total_students"]
    )
average_cgpa = students_collection.aggregate([
    {
        "$group": {
            "_id": "$department",
            "average_cgpa": {"$avg": "$cgpa"}
        }
    },
    {
        "$sort": {
            "average_cgpa": -1
        }
    }
])

print("\nAverage CGPA by Department:")

for result in average_cgpa:
    print(
        result["_id"],
        "→",
        round(result["average_cgpa"], 2)
    )
placement_analysis = students_collection.aggregate([
    {
        "$group": {
            "_id": "$placement_status",
            "total_students": {"$sum": 1}
        }
    },
    {
        "$sort": {
            "total_students": -1
        }
    }
])

print("\nPlacement Analysis:")

for result in placement_analysis:
    print(
        result["_id"],
        "→",
        result["total_students"]
    )