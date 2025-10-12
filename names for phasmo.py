from enum import Enum

class Characters(Enum):
    a = 1
    b = 2
    c = 3
    d = 4
    e = 5
    f = 6
    g = 7
    h = 8
    i = 9
    j = 10
    k = 11
    l = 12
    m = 13
    n = 14
    o = 15
    p = 16
    q = 17
    r = 18
    s = 19
    t = 20
    u = 21
    v = 22
    w = 23
    x = 24
    y = 25
    z = 26

clear = str(input("Do u want to clear the file? (yes/no)\n"))
clear = clear.lower()
if clear == "yes":
    with open('names.txt', 'w') as f:
        f.write("")
    with open('out.txt', 'w') as f:
        f.write("")

names = []
print("\nEnter -1 to end entry.")

Continue = True
while Continue:
    user = str(input("Enter username: "))
    if user == "-1":
        Continue = False
    else: 
        with open('names.txt', 'a') as f:
            f.write(f"{user}\n")

data = []  
  
with open("names.txt", "r") as file:
    names = [line.strip() for line in file]

names = list(dict.fromkeys(names))
    
for name in names:
    name_data = []
    for char in name:
        name_data.append(Characters[char.lower()].value)
    data.append(name_data)

with open('out.txt', 'w') as f:
    for item in data:
        f.write(f"{item},\n")