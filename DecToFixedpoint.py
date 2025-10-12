# -------------------------------------------- #
#                  SETTINGS                    #
integerBits = 7
fractionalBits = 9
number = 0.99

# -------------------------------------------- #
#                CONVERSION                    #

fixedPointNumber = int(number * (1 << fractionalBits))
precision = fixedPointNumber / (1 << fractionalBits)
print(f"Input: {number} , Output: {fixedPointNumber} , Precision: {precision}") 