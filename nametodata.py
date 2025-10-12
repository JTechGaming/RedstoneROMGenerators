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
    _ = 0

names = [
    #"Bone", "Burned_Crucifix", "Dead_Body", "Dirty_Water", "Disturbed_Salt", "Fingerprint", "Footprint", "Ghost", "Ghost_Writing", "Interaction", "Haunted_Mirror", "Monkey_Paw", "Music_Box", "Ouija_Board", "Summoning_Circle", "Tarot_Cards", "Voodoo_Doll"
    #"____room", "___garage", "__kitchen", "__hallway", "__bathroom", "__bedroom", "__bedroom", "__hallway", "storage_room", "storage_room"
    "_living", "_", "_", "_", "_", "_master", "__boys", "basement", "_right", "__left"
]

data = []

for name in names:
    name_data = []
    for char in name:
        name_data.append(Characters[char.lower()].value)
    data.append(name_data)
    
with open('out.txt', 'w') as f:
    for item in data:
        f.write(f"{item},\n")