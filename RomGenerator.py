import mcschematic
from enum import Enum

class Axis(Enum):
    X = 0
    Z = 1

class Direction(Enum):
    POSITIVE = 1
    NEGATIVE = -1

class Directions(Enum):
    NORTH = "north"
    EAST = "east"
    SOUTH = "south"
    WEST = "west"

class Color(Enum):
    RED = "red"
    BLUE = "blue"
    GREEN = "green"
    YELLOW = "yellow"
    BLACK = "black"
    WHITE = "white"
    ORANGE = "orange"
    PURPLE = "purple"
    CYAN = "cyan"
    MAGENTA = "magenta"
    LIME = "lime"
    PINK = "pink"
    GRAY = "gray"
    LIGHT_GRAY = "light_gray"
    LIGHT_BLUE = "light_blue"
    BROWN = "brown"

class BlockType(Enum):
    WOOL = "wool"
    CONCRETE = "concrete"

# -------------------------------------------- #
#                  SETTINGS                    #
# data = [
#     #0, 0, .5, .5, 1.0, 1.0, 1.5, 1.5, 2.0, 2.0
#     #[0, 0, 69, 92, 128, 184, 207, 277, 277, 369],
#     #0, .5, 1.0, 1.5, 2.0,|1.0, 1.5, 2.0, 2.5, 3.0
#     [0, 69, 128, 207, 277, 128, 207, 277, 345, 414],
#     [0, 92, 184, 277, 369, 184, 277, 369, 460, 511] # 552
# ]

data = [
    [0, 12, 9, 22, 9, 14, 7],
    [0],
    [0],
    [0],
    [0],
    [0, 13, 1, 19, 20, 5, 18],
    [0, 0, 2, 15, 25, 19],
    [2, 1, 19, 5, 13, 5, 14, 20],
    [0, 18, 9, 7, 8, 20],
    [0, 0, 12, 5, 6, 20],
]

axis = Axis.X
direction = Direction.POSITIVE
bits = 5
color = Color.BROWN
blockType = BlockType.CONCRETE
invert = True
fillCharacters = True
characterAmount = 8 # only used if fillCharacters is True
offsetSetting = 0

# -------------------------------------------- #
#                DO NOT TOUCH                  #
schem = mcschematic.MCSchematic()
offset = 0

def setBlock(x, y, z):
    if axis == Axis.X:
        schem.setBlock((x, y, z), f"minecraft:{color.value}_{blockType.value}")
    else:
        schem.setBlock((x, y, z), f"minecraft:{color.value}_{blockType.value}")

def setGlass(x, y, z):
    if axis == Axis.X:
        schem.setBlock((x, y, z), f"minecraft:{color.value}_stained_glass")
    else:
        schem.setBlock((x, y, z), f"minecraft:{color.value}_stained_glass")

def setSpecificBlock(x, y, z, block):
    if axis == Axis.X:
        schem.setBlock((x, y, z), block)
    else:
        schem.setBlock((x, y, z), block)

def getOpposingDirection(direction):
    if direction == Directions.NORTH:
        return Directions.SOUTH
    elif direction == Directions.EAST:
        return Directions.WEST
    elif direction == Directions.SOUTH:
        return Directions.NORTH
    elif direction == Directions.WEST:
        return Directions.EAST
    
def getDirection(axis, direction):
    if axis == Axis.X:
        if direction == Direction.POSITIVE:
            return Directions.EAST
        else:
            return Directions.WEST
    else:
        if direction == Direction.POSITIVE:
            return Directions.SOUTH
        else:
            return Directions.NORTH
        
def getNextDirection(direction):
    if direction == Directions.NORTH:
        return Directions.EAST
    elif direction == Directions.EAST:
        return Directions.SOUTH
    elif direction == Directions.SOUTH:
        return Directions.WEST
    elif direction == Directions.WEST:
        return Directions.NORTH

dir = getDirection(axis, direction)
oppDir = getOpposingDirection(dir).value
nextDir = getNextDirection(dir)
oppNextDir = getOpposingDirection(nextDir).value

if fillCharacters: # might want to change this to just the size of the data
    for c in range(characterAmount):
        y = bits * -2
        for b in range(bits):
            for j in range(5):
                setBlock(j+offset-1+c*5, y, -2) # 5 supporting wool blocks
                if j == 4:
                    setBlock(j+offset-1+c*5, y+1, -2) # final block is wool block instead of redstone wire
                    setBlock(j+offset-1+c*5, y, -1) # repeater support block
                    setSpecificBlock(j+offset-1+c*5, y+1, -1, f"minecraft:repeater[delay=1,facing={nextDir.value},locked=false,powered=false]") # repeater
                elif j == 0:
                    setSpecificBlock(j+offset-1+c*5, y+1, -2, f"minecraft:repeater[delay=2,facing={dir.value},locked=false,powered=false]") # 2-tick repeater
                else:
                    setSpecificBlock(j+offset-1+c*5, y+1, -2, f"minecraft:redstone_wire[{dir.value}=side,{nextDir.value}=none,power=0,{oppNextDir}=none,{oppDir}=side]") # redstone wire
            y += 2

for n in range(0, len(data)):
    name = data[n]
    filledName = name + [0] * (characterAmount - len(name))
    if not fillCharacters:
        filledName = name
    if invert:
        invName = filledName[::-1]
    else:
        invName = filledName
    for i in range(0, len(invName)):
        dist = i * 5

        y = bits * -2 - 2
        for j in range(5): # 5 supporting wool blocks
            setBlock(j+offset+dist, y, n*2)
        y += 1
        for j in range(2): # 2 repeaters
            setSpecificBlock(j+offset+1+dist, y, n*2, f"minecraft:repeater[delay=1,facing={oppDir},locked=false,powered=true]")
        p = 15
        for j in range(2): # 2 dust
            p -= 1
            setSpecificBlock(j+offset+3+dist, y, n*2, f"minecraft:redstone_wire[{dir.value}=side,{nextDir.value}=none,power={p},{oppNextDir}=none,{oppDir}=side]")
        setBlock(offset+dist, y, n*2) # 1 wool block as the torch support block
        y += 1

        setSpecificBlock(offset+dist, y, n*2, f"minecraft:redstone_torch[lit=false]")

        currentChar = invName[i]

        for b in range(bits):
            for j in range(2): # 2 supporting glass blocks (in the glass tower)
                setGlass(j+offset+1+dist, y, n*2)
            for j in range(2): # 2 supporting wool blocks and the 2 dust blocks
                setBlock(offset+3+dist, y, n*2+j)
                if j == 0 and currentChar & (1 << b):
                    setSpecificBlock(offset+3+dist, y+1, n*2+j, f"minecraft:redstone_wire[{nextDir.value}=side,{oppNextDir}=side,power=0,{dir.value}=none,{oppDir}=side]")
                else:
                    setSpecificBlock(offset+3+dist, y+1, n*2+j, f"minecraft:redstone_wire[{nextDir.value}=side,{oppNextDir}=side,power=0,{dir.value}=none,{oppDir}=none]")
            if b != bits - 1: # if it is not the last bit
                if b == 0: # if it is the first bit
                    setBlock(offset+dist, y+1, n*2) # 1 wool block as the torch top block
                else:
                    setGlass(offset+dist, y+1, n*2) # 1 glass block as the dust support block (in the glass tower)
            y += 1
            if b == bits - 1: # if it is the last bit
                setSpecificBlock(offset+1+dist, y, n*2, f"minecraft:redstone_wire[{dir.value}=side,{nextDir.value}=none,power=0,{oppNextDir}=none,{oppDir}=side]") # lower dust
            else:
                setSpecificBlock(offset+1+dist, y, n*2, f"minecraft:redstone_wire[{dir.value}=side,{nextDir.value}=none,power=0,{oppNextDir}=none,{oppDir}=up]") # lower dust
            if currentChar & (1 << b): # if the current bit is 1
                setSpecificBlock(offset+2+dist, y, n*2, f"minecraft:repeater[delay=1,facing={oppDir},locked=false,powered=false]") # set the repeater
            y += 1
            if b != bits - 1: # if it is not the last bit
                setSpecificBlock(offset+dist, y, n*2, f"minecraft:redstone_wire[{oppDir}=side,{nextDir.value}=none,power=0,{oppNextDir}=none,{dir.value}=up]") # upper dust

schem.save("out", "rom", mcschematic.Version.JE_1_20_1)