from enum import Enum

class Characters(Enum):
    a = 3
    b = 4
    c = 5
    d = 6
    e = 7
    f = 8
    g = 9
    h = 10
    i = 11
    j = 12
    k = 13
    l = 14
    m = 15
    n = 16
    o = 17
    p = 18
    q = 19
    r = 20
    s = 21
    t = 22
    u = 23
    v = 24
    w = 25
    x = 26
    y = 27
    z = 28
    one = 29
    two = 30
    three = 31
    four = 32
    five = 33
    six = 34
    seven = 35
    eight = 36
    nine = 37
    zero = 38
    _ = 0

names = [
    "Yes", "No", "543210", "Healthy", "Good", "Average", "Bad", "Awful",
    "Accident", "Drowned", "Choked", "Murder", "Shot", "Fell", "Slipped", "Angry", "Cold", "Empty", "Excited", "Hurt", "Lonely", "Sad", "Scared", "Sick", "Strong", "Weak",
    "Hatred", "Kill", "Lonely", "Lost", "Love", "Peace", "Revenge", "Scared", "Trapped", "Vengeance", "You", "Whos_there", "Polo"
]

data = []

for name in names:
    name_data = []
    for char in name:
        if char.isdigit():
            # If the character is a digit, convert it to its id in the Characters enum, so if its 3, it will be Characters.three.value
            if char == '0':
                name_data.append(Characters.zero.value)
            elif char == '1':
                name_data.append(Characters.one.value)
            elif char == '2':
                name_data.append(Characters.two.value)
            elif char == '3':
                name_data.append(Characters.three.value)
            elif char == '4':
                name_data.append(Characters.four.value)
            elif char == '5':
                name_data.append(Characters.five.value)
            elif char == '6':
                name_data.append(Characters.six.value)
            elif char == '7':
                name_data.append(Characters.seven.value)
            elif char == '8':
                name_data.append(Characters.eight.value)
            elif char == '9':
                name_data.append(Characters.nine.value)
        else:
            name_data.append(Characters[char.lower()].value)
    data.append(name_data)
    
with open('out.txt', 'w') as f:
    for item in data:
        f.write(f"{item},\n")