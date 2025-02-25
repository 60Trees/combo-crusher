x = 0
y = 1

floorCol = 0
ceilCol = 1

# This WORKSSSSS!!!!!!!!! YESSSSSSSSSS
def getHeightOfPoint(ab, cx):
    a, b = ab
    return \
        (
            (a[y] - b[y]) /
            (a[x] - b[x])
        ) * (cx - a[x]) + a[y]

def iscolliding(a, b, c, widthOfLine):
    return (c[x] > a[x] and c[x] < b[x]) and \
    (c[y] > getHeightOfPoint((a, b), c[x]) and c[y] < getHeightOfPoint((a, b), c[x]) + widthOfLine)

def iscolliding_ceiling(a, b, c, widthOfLine):
    return (c[x] > a[x] and c[x] < b[x]) and \
    (c[y] < getHeightOfPoint((a, b), c[x]) and c[y] > getHeightOfPoint((a, b), c[x]) - widthOfLine)

#print(iscolliding(
#    (4, 4),
#    (6, -2),
#    (5, 3),
#    2
#))