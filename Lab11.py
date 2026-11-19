from pathlib import Path
import matplotlib.pyplot as plt

DATA_DIR = Path(__file__).resolve().parent / "data"

def load_students():
    students = {}
    with (DATA_DIR / "students.txt").open() as file:
        for line in file:
            line = line.strip()
            if line:
                student_id = line[:3]
                name = line[3:]
                students[student_id] = name
    return students

def load_assignments():
    assignments = {}
    lines = (DATA_DIR / "assignments.txt").read_text().splitlines()
    lines = [line.strip() for line in lines if line.strip()]
    for i in range(0, len(lines), 3):
        name = lines[i]
        assignment_id = lines[i + 1]
        points = int(lines[i + 2])
        assignments[assignment_id] = {"name": name, "points": points}
    return assignments

def load_submissions():
    submissions = []
    for path in DATA_DIR.rglob("*"):
        if not path.is_file() or path.name in {"students.txt", "assignments.txt"}:
            continue
        with path.open() as file:
            for line in file:
                parts = line.strip().split("|")
                if len(parts) == 3:
                    student_id, assignment_id, percent = parts
                    submissions.append((student_id, assignment_id, float(percent)))
    return submissions

def rounded_percent(value):
    return int(value + 0.5)

students = load_students()
assignments = load_assignments()
submissions = load_submissions()

print("1. Student grade")
print("2. Assignment statistics")
print("3. Assignment graph")
selection = input("\nEnter your selection: ")

if selection == "1":
    name = input("What is the student's name: ")
    student_id = next(
        (sid for sid, student_name in students.items()
         if student_name.casefold() == name.casefold()),
        None
    )
    if student_id is None:
        print("Student not found")
    else:
        earned_points = 0
        for sid, assignment_id, percent in submissions:
            if sid == student_id and assignment_id in assignments:
                points_possible = assignments[assignment_id]["points"]
                earned_points += points_possible * percent / 100
        course_percent = earned_points / 1000 * 100
        print(f"{rounded_percent(course_percent)}%")

elif selection in {"2", "3"}:
    name = input("What is the assignment name: ")
    assignment_id = next(
        (aid for aid, assignment in assignments.items()
         if assignment["name"].casefold() == name.casefold()),
        None
    )
    if assignment_id is None:
        print("Assignment not found")
    else:
        scores = [percent for _, aid, percent in submissions if aid == assignment_id]
        if selection == "2":
            if scores:
                print(f"Min: {rounded_percent(min(scores))}%")
                print(f"Avg: {int(sum(scores) / len(scores))}%")
                print(f"Max: {rounded_percent(max(scores))}%")
        else:
            plt.hist(scores, bins=[0, 25, 50, 75, 100])
            plt.xlabel("Score (%)")
            plt.ylabel("Number of submissions")
            plt.title(name)
            plt.show()
