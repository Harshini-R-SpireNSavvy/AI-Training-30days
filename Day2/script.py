import json

# load data
with open('employees.json', 'r') as f:
    employees = json.load(f)

# 1. count employees per department
count = {}
for e in employees:
    dept = e.get("department")
    count[dept] = count.get(dept, 0) + 1

print("Department count:")
for d in count:
    print(d, count[d])


# 2. find employee with highest salary
top = employees[0]
for e in employees:
    if e.get("salary", 0) > top.get("salary", 0):
        top = e

print("\nHighest salary:")
print(top.get("name"), top.get("salary"))


# 3. list unique departments
unique_dept = set()
for e in employees:
    unique_dept.add(e.get("department"))

print("\nUnique departments:")
for d in unique_dept:
    print(d)


# 4. save engineering team
eng = []
for e in employees:
    if e.get("department") == "Engineering":
        eng.append(e)

with open("engineering_team.json", "w") as f:
    json.dump(eng, f, indent=4)

print("\nEngineering team saved")



for e in employees:
    name = e.get("name", "Unknown")
    dept = e.get("department", "Not given")
    salary = e.get("salary", 0)

    print(name, "-", dept, "-", salary)

