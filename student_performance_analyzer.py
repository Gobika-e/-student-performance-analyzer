
import json
import csv
import os

DATA_FILE = "student_data.json"
students = []

def load_data():
    global students
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                students = json.load(file)
            print("Student records loaded!")
        except (json.JSONDecodeError, OSError):
            students = []

def save_data():
    with open(DATA_FILE, "w") as file:
        json.dump(students, file, indent=4)

def calculate_result(marks):
    total = sum(marks)
    average = total / 5

    if min(marks) < 35:
        grade, result = "F", "Fail"
    elif average >= 90:
        grade, result = "A", "Pass"
    elif average >= 75:
        grade, result = "B", "Pass"
    elif average >= 60:
        grade, result = "C", "Pass"
    else:
        grade, result = "D", "Pass"

    return total, round(average, 2), grade, result

def enter_marks():
    marks = []
    for i in range(1, 6):
        while True:
            try:
                mark = int(input(f"Subject {i} mark (0-100): "))
                if 0 <= mark <= 100:
                    marks.append(mark)
                    break
                print("Enter marks between 0 and 100.")
            except ValueError:
                print("Enter a valid number.")
    return marks

def add_student():
    name = input("Enter student name: ").strip()

    if not name:
        print("Name cannot be empty!")
        return

    if any(s["name"].lower() == name.lower() for s in students):
        print("Student already exists!")
        return

    marks = enter_marks()
    total, average, grade, result = calculate_result(marks)

    students.append({
        "name": name,
        "marks": marks,
        "total": total,
        "average": average,
        "grade": grade,
        "result": result
    })

    save_data()
    print("Student added successfully!")

def view_report():
    if not students:
        print("No student records available!")
        return

    for s in students:
        print("\nName:", s["name"])
        print("Marks:", s["marks"])
        print("Total:", s["total"], "/ 500")
        print("Average:", s["average"])
        print("Grade:", s["grade"])
        print("Result:", s["result"])

def search_student():
    name = input("Enter student name: ").strip().lower()

    for s in students:
        if s["name"].lower() == name:
            print("\nName:", s["name"])
            print("Marks:", s["marks"])
            print("Total:", s["total"])
            print("Average:", s["average"])
            print("Grade:", s["grade"])
            print("Result:", s["result"])
            return

    print("Student not found!")

def update_marks():
    name = input("Enter student name to update: ").strip().lower()

    for s in students:
        if s["name"].lower() == name:
            print("Enter new marks:")
            marks = enter_marks()
            total, average, grade, result = calculate_result(marks)

            s.update({
                "marks": marks,
                "total": total,
                "average": average,
                "grade": grade,
                "result": result
            })

            save_data()
            print("Marks updated successfully!")
            return

    print("Student not found!")

def delete_student():
    name = input("Enter student name to delete: ").strip().lower()

    for s in students:
        if s["name"].lower() == name:
            confirm = input("Confirm deletion? (yes/no): ").lower()

            if confirm == "yes":
                students.remove(s)
                save_data()
                print("Student deleted!")
            else:
                print("Deletion cancelled!")
            return

    print("Student not found!")

def class_summary():
    if not students:
        print("No student records available!")
        return

    avg = sum(s["average"] for s in students) / len(students)
    topper = max(students, key=lambda s: s["average"])
    passed = sum(s["result"] == "Pass" for s in students)

    print("\n--- CLASS SUMMARY ---")
    print("Total students:", len(students))
    print("Class average:", round(avg, 2))
    print("Topper:", topper["name"])
    print("Passed:", passed)
    print("Failed:", len(students) - passed)

def show_ranking():
    if not students:
        print("No student records available!")
        return

    ranked = sorted(
        students,
        key=lambda s: s["average"],
        reverse=True
    )

    print("\n===== STUDENT RANKING =====")
    print(f"{'Rank':<8}{'Name':<20}{'Average':<10}{'Grade':<8}")

    for rank, s in enumerate(ranked, start=1):
        print(
            f"{rank:<8}{s['name']:<20}"
            f"{s['average']:<10}{s['grade']:<8}"
        )

def save_report():
    with open("student_report.csv", "w", newline="") as file:
        fields = [
            "name", "marks", "total",
            "average", "grade", "result"
        ]
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()

        for s in students:
            row = s.copy()
            row["marks"] = ", ".join(map(str, s["marks"]))
            writer.writerow(row)

    print("CSV report saved successfully!")

load_data()

while True:
    print("\n===== STUDENT PERFORMANCE ANALYZER =====")
    print("1. Add Student")
    print("2. View Student Report")
    print("3. Search Student")
    print("4. Update Student Marks")
    print("5. Delete Student")
    print("6. Class Summary")
    print("7. Student Ranking")
    print("8. Save CSV Report")
    print("9. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_student()
    elif choice == "2":
        view_report()
    elif choice == "3":
        search_student()
    elif choice == "4":
        update_marks()
    elif choice == "5":
        delete_student()
    elif choice == "6":
        class_summary()
    elif choice == "7":
        show_ranking()
    elif choice == "8":
        save_report()
    elif choice == "9":
        print("Thank you for using Student Performance Analyzer!")
        break
    else:
        print("Invalid choice! Try again.")
