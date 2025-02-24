import math

ground_points = [
    [ #   X   Y
        (-12, 6),
        (12,  3)
    ],
]

pos = (
    -10, 3
)

x = 0
y = 1

# This WORKSSSSS!!!!!!!!! YESSSSSSSSSS
def getHeightOfPoint(ab, cx):
    a, b = ab
    return \
        (
            (a[y] - b[y]) /
            (a[x] - b[x])
        ) * (cx - a[x]) + a[y]

iscolliding = lambda a, b, c, widthOfLine: \
    (c[x] > a[x] and c[x] < b[x]) and \
    (c[y] > getHeightOfPoint((a, b), c[x]) and c[y] < getHeightOfPoint((a, b), c[x]) + widthOfLine)

print(iscolliding(
    (-12, 1),
    (-2, -2),
    (-5, -2),
    2
))