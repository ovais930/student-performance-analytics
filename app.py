import streamlit as st
from pymongo import MongoClient


# =========================================================
# MONGODB CONNECTION
# =========================================================

client = MongoClient("mongodb://localhost:27017/")

db = client["student_analytics"]

students_collection = db["students"]


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Student Performance Analytics",
    page_icon="📊",
    layout="wide"
)


# =========================================================
# TITLE
# =========================================================

st.title("📊 Student Performance Analytics System")

st.write(
    "MongoDB-based application for storing, processing "
    "and analyzing student data."
)


# =========================================================
# BASIC STATISTICS
# =========================================================

total_students = students_collection.count_documents({})


# Average CGPA
average_cgpa = students_collection.aggregate([
    {
        "$group": {
            "_id": None,
            "average": {"$avg": "$cgpa"}
        }
    }
])

average_cgpa_result = list(average_cgpa)

if average_cgpa_result:
    avg_cgpa = round(
        average_cgpa_result[0]["average"], 2
    )
else:
    avg_cgpa = 0


# Average Percentage
average_percentage = students_collection.aggregate([
    {
        "$group": {
            "_id": None,
            "average": {"$avg": "$percentage"}
        }
    }
])

average_percentage_result = list(average_percentage)

if average_percentage_result:
    avg_percentage = round(
        average_percentage_result[0]["average"], 2
    )
else:
    avg_percentage = 0


# =========================================================
# DASHBOARD METRICS
# =========================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Students",
        total_students
    )

with col2:
    st.metric(
        "Average CGPA",
        avg_cgpa
    )

with col3:
    st.metric(
        "Average Percentage",
        f"{avg_percentage}%"
    )


# =========================================================
# STUDENT SEARCH
# =========================================================

st.subheader("🔎 Search Student")

student_id = st.text_input(
    "Enter Student ID",
    placeholder="Example: STU02500"
)

if student_id:

    student = students_collection.find_one(
        {"student_id": student_id},
        {"_id": 0}
    )

    if student:

        st.success("Student found!")

        col1, col2 = st.columns(2)

        with col1:

            st.write("### Student Information")

            st.write(
                f"**Student ID:** {student['student_id']}"
            )

            st.write(
                f"**Name:** {student['name']}"
            )

            st.write(
                f"**Age:** {student['age']}"
            )

            st.write(
                f"**Gender:** {student['gender']}"
            )

            st.write(
                f"**Department:** {student['department']}"
            )

            st.write(
                f"**Semester:** {student['semester']}"
            )

            st.write(
                f"**City:** {student['city']}"
            )

        with col2:

            st.write("### Academic Information")

            st.write(
                f"**Attendance:** {student['attendance']}%"
            )

            st.write(
                f"**Mathematics:** "
                f"{student['mathematics_marks']}"
            )

            st.write(
                f"**DBMS:** "
                f"{student['dbms_marks']}"
            )

            st.write(
                f"**Computer Networks:** "
                f"{student['computer_networks_marks']}"
            )

            st.write(
                f"**Programming:** "
                f"{student['programming_marks']}"
            )

            st.write(
                f"**Total Marks:** "
                f"{student['total_marks']}"
            )

            st.write(
                f"**Percentage:** "
                f"{student['percentage']}%"
            )

            st.write(
                f"**CGPA:** "
                f"{student['cgpa']}"
            )

            st.write(
                f"**Placement Status:** "
                f"{student['placement_status']}"
            )

    else:

        st.error(
            "Student not found. Please check the Student ID."
        )


# =========================================================
# DEPARTMENT + SEMESTER FILTER
# =========================================================

st.subheader("🎓 Student Filters")

col1, col2 = st.columns(2)


with col1:

    departments = [
        "All",
        "CSE",
        "ISE",
        "ECE",
        "EEE",
        "ME",
        "CIVIL"
    ]

    selected_department = st.selectbox(
        "Select Department",
        departments
    )


with col2:

    semesters = [
        "All",
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8
    ]

    selected_semester = st.selectbox(
        "Select Semester",
        semesters
    )


# Build MongoDB filter

query = {}

if selected_department != "All":
    query["department"] = selected_department

if selected_semester != "All":
    query["semester"] = selected_semester


# Get filtered students

filtered_students = list(
    students_collection.find(
        query,
        {"_id": 0}
    )
)


st.write(
    f"Students found: **{len(filtered_students)}**"
)


if filtered_students:

    st.dataframe(
        filtered_students,
        use_container_width=True
    )

else:

    st.warning(
        "No students found for the selected filters."
    )


# =========================================================
# PERFORMANCE ANALYSIS
# =========================================================

st.subheader("📈 Performance Analysis")


# ---------- CGPA > 8 ----------

high_cgpa_count = students_collection.count_documents(
    {
        "cgpa": {
            "$gt": 8
        }
    }
)


# ---------- Attendance >= 75 ----------

good_attendance_count = students_collection.count_documents(
    {
        "attendance": {
            "$gte": 75
        }
    }
)


col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Students with CGPA > 8",
        high_cgpa_count
    )

with col2:

    st.metric(
        "Students with Attendance ≥ 75%",
        good_attendance_count
    )


# =========================================================
# AVERAGE CGPA BY SEMESTER
# =========================================================

st.subheader("📚 Average CGPA by Semester")

semester_analysis = students_collection.aggregate([
    {
        "$group": {
            "_id": "$semester",
            "average_cgpa": {
                "$avg": "$cgpa"
            }
        }
    },
    {
        "$sort": {
            "_id": 1
        }
    }
])


semester_data = list(
    semester_analysis
)


if semester_data:

    semester_chart_data = {
        "Semester": [
            f"Semester {item['_id']}"
            for item in semester_data
        ],

        "Average CGPA": [
            round(item["average_cgpa"], 2)
            for item in semester_data
        ]
    }

    st.line_chart(
        semester_chart_data,
        x="Semester",
        y="Average CGPA"
    )


# =========================================================
# DEPARTMENT-WISE STUDENT COUNT
# =========================================================

st.subheader("👨‍🎓 Students by Department")

department_analysis = students_collection.aggregate([
    {
        "$group": {
            "_id": "$department",
            "total_students": {
                "$sum": 1
            }
        }
    },
    {
        "$sort": {
            "total_students": -1
        }
    }
])


department_data = list(
    department_analysis
)


if department_data:

    department_chart_data = {
        "Department": [
            item["_id"]
            for item in department_data
        ],

        "Students": [
            item["total_students"]
            for item in department_data
        ]
    }

    st.bar_chart(
        department_chart_data,
        x="Department",
        y="Students"
    )


# =========================================================
# PLACEMENT ANALYSIS
# =========================================================

st.subheader("💼 Placement Analysis")

placement_analysis = students_collection.aggregate([
    {
        "$group": {
            "_id": "$placement_status",
            "total_students": {
                "$sum": 1
            }
        }
    }
])


placement_data = list(
    placement_analysis
)


if placement_data:

    placement_chart_data = {
        "Status": [
            item["_id"]
            for item in placement_data
        ],

        "Students": [
            item["total_students"]
            for item in placement_data
        ]
    }

    st.bar_chart(
        placement_chart_data,
        x="Status",
        y="Students"
    )


# =========================================================
# TOP 10 STUDENTS
# =========================================================

st.subheader("🏆 Top 10 Students")

top_students = students_collection.find(
    {},
    {
        "_id": 0,
        "student_id": 1,
        "name": 1,
        "department": 1,
        "percentage": 1,
        "cgpa": 1,
        "placement_status": 1
    }
).sort(
    "percentage",
    -1
).limit(10)


top_students_list = list(
    top_students
)


if top_students_list:

    st.dataframe(
        top_students_list,
        use_container_width=True
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Student Performance Analytics System | "
    "Python + MongoDB + PyMongo + Streamlit"
)