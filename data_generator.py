import random
import string
from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")

db = client["student_analytics"]

students_collection = db["students"]

print("Connected to MongoDB!")
names = [
    "Aarav", "Rahul", "Priya", "Ananya", "Arjun",
    "Aditya", "Sneha", "Rohan", "Neha", "Vikram",
    "Ishita", "Karan", "Pooja", "Sahil", "Aisha"
]

departments = ["CSE", "ISE", "ECE", "EEE", "ME", "CIVIL"]

cities = [
    "Jammu", "Srinagar", "Delhi", "Bangalore",
    "Mumbai", "Hyderabad", "Pune", "Chennai"
]

genders = ["Male", "Female"]
def generate_student(student_number):
    mathematics = random.randint(40, 100)
    dbms = random.randint(40, 100)
    computer_networks = random.randint(40, 100)
    programming = random.randint(40, 100)

    total_marks = mathematics + dbms + computer_networks + programming
    percentage = total_marks / 4

    cgpa = round(percentage / 10, 2)

    student = {
        "student_id": f"STU{student_number:05d}",
        "name": random.choice(names),
        "age": random.randint(18, 24),
        "gender": random.choice(genders),
        "department": random.choice(departments),
        "semester": random.randint(1, 8),
        "city": random.choice(cities),
        "attendance": random.randint(60, 100),
        "mathematics_marks": mathematics,
        "dbms_marks": dbms,
        "computer_networks_marks": computer_networks,
        "programming_marks": programming,
        "total_marks": total_marks,
        "percentage": round(percentage, 2),
        "cgpa": cgpa,
        "placement_status": random.choice(["Placed", "Not Placed"])
    }

    return student
students = []

for i in range(1, 5001):
    student = generate_student(i)
    students.append(student)

print("Total students generated:", len(students))
students_collection.insert_many(students)

print("5000 students inserted into MongoDB successfully!")