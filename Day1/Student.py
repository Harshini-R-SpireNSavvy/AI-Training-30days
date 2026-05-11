import json

# load data
with open('students.json', 'r') as f:
    students = json.load(f)

# 1. names with marks > 70
print("Marks > 70:")
for s in students:
    if s["marks"] > 70:
        print(s["name"])


# 2. count students per department
count = {}

for s in students:
    dept = s["department"]
    count[dept] = count.get(dept, 0) + 1

print("\nDepartment count:")
for d in count:
    print(d, count[d])


# 3. highest marks student
top = students[0]

for s in students:
    if s["marks"] > top["marks"]:
        top = s

print("\nTop student:")
print(top["name"], top["marks"])


# 4. save Data Science students
ds = []

for s in students:
    if s["department"] == "Data Science":
        ds.append(s)

with open("ds_students.json", "w") as f:
    json.dump(ds, f)

print("\nSaved Data Science students")