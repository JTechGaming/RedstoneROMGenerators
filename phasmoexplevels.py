import mcschematic

#schem.setBlock((0, 0, 0), "minecraft:redstone_block")

# mag comps in positive z
# 26 mag comps per row
# from start to the most significant bit is -2 in x, +3 in z, -1 in y
# from one mag comp tho the next is +5 in z
# from one bit to the next below is -2 in y
# from one row to the next is -2 in x
# 8 bit towers
# 2 rows
# 0 is sea lantern, 1 is redstone block
# read data in from a list



# -------------------------------------------- #
#                  SETTINGS                    #
data = [
           56, 112, 143, 174, 205, 220, 235, 251, 254, 255
       ]

rowLength = 5
rows = 2
bits = 8

x = 0
y = -1
z = 0

distance = 5
rowOffset = 4

direction = 1
rowDirection = 1

axis = "x"
rowAxis = "z"
hasIrregularSpacing = False
irregularSpacingInterval = 3
irregularSpacingDistance = 59

hasIrregularRowSpacing = False
onlyFirstTimeIrregular = False
irregularRowSpacingInterval = 2
irregularRowSpacingDistance = 84

# -------------------------------------------- #
#                DO NOT TOUCH                  #
# TODO: for some reason the 2nd irregular row is one block off
schem = mcschematic.MCSchematic() 
accum = 0
irrAccum = 0
irrRowAccum = 0
startValue = 0
hasDoneFirst = False
doneRows = 0
if axis == "x":
    startValue = x
else:
    startValue = z
for i in range(0, len(data)):
    if hasIrregularSpacing and (i - irrAccum) == irregularSpacingInterval:
        if axis == "x":
            z += (irregularSpacingDistance - distance) * direction
        else:
            x += (irregularSpacingDistance - distance) * direction
        irrAccum += irregularSpacingInterval
    if (i-accum) == rowLength:
        doneRows += 1
        #direction = direction * -1
        irrAccum = i
        accum += rowLength
        if axis == "x":
            z = startValue
            if hasIrregularRowSpacing and (doneRows - irrRowAccum) == irregularRowSpacingInterval and not (onlyFirstTimeIrregular and hasDoneFirst):
                hasDoneFirst = True
                if rowAxis == "z":
                    x += (irregularRowSpacingDistance - rowOffset) * rowDirection
                else:
                    z += (irregularRowSpacingDistance - rowOffset) * rowDirection
                irrRowAccum += irregularRowSpacingInterval
            x += rowOffset * rowDirection
        else:
            x = startValue
            z += rowOffset * rowDirection

    for j in range(0, bits):
        if data[i] & (1 << j):
            block = "minecraft:redstone_block"
        else:
            block = "minecraft:magenta_stained_glass"
        a = 0
        b = 0
        if axis == "x":
            a = z
            b = x
        else:
            a = x
            b = z
        schem.setBlock((a, y - bits * 2 - 2 + j * 2, b), block)
    if hasIrregularSpacing and (i - irrAccum) == irregularSpacingInterval:
        #nothing
        pass
    else:
        if rowAxis == "z":
            z += distance * direction
        else:
            x += distance * direction

schem.save("out", "phasmophobiaschematic", mcschematic.Version.JE_1_20_1)