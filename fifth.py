eps = 0.000000001
# Ax + By + C = 0
class Line2d(object):
    __slots__ = ("A", "B", "C")

    def __init__(self, A, B):
        self.A = A[1] - B[1]
        self.B = B[0] - A[0]
        self.C = A[0]*B[1] - A[1]*B[0]

    def belongs(self, A):
        if( self.A*A[0] + self.B*A[1] + self.C <= eps ): return True
        else: return False

# return polygon area
def polygon_area(polygon):
    area = 0.0

    if(len(polygon) < 3): return area

    for i in range(len(polygon)):
        area = area + polygon[i][0]*polygon[(i+1)%len(polygon)][1] - polygon[i][1]*polygon[(i+1)%len(polygon)][0]

    area = area / 2.0
    if(area < 0.0): area = -area

    return area

# share segmet for two segmet, which correlate as n/m. Return intersection point
def share_segment(A, B, n, m):
    x = (A[0]*m + B[0]*n) / (m + n)
    y = (A[1]*m + B[1]*n) / (m + n)
    return (x, y)

#share polygon for two polygon, which areas correlate as n/m. Return intersection point of line, passing through one of the vertices of a polygon, and a polygon
def share_polygon(polygon, n,  m):
    S1 = n*polygon_area(polygon)/(n+m);

    total_S = 0.0
    i = 1

    for i in range(1, len(polygon)-1):
        triangle = [polygon[0], polygon[i], polygon[i+1]]
        area_tr = polygon_area(triangle)
        if( total_S + area_tr <= S1 ): total_S += area_tr
        else: break

    if( S1 - total_S <= eps ): return polygon[i]
    
    triangle = [polygon[0], polygon[i], polygon[i+1]]
    area_tr = polygon_area(triangle)

    return share_segment(polygon[i], polygon[i+1], S1-total_S, area_tr-S1+total_S)

# return two polygons, which areas correlate as n/m
def devide_polygon(polygon, n, m):
    P = share_polygon(polygon, n, m)

    polygon1 = []
    polygon2 = []

    polygon2.append(polygon[0])
    j = 0

    for i in range(len(polygon)-1):
        l = Line2d(polygon[i], polygon[i+1])
        if(l.belongs(P)):
            if( P[0] == polygon[i][0] and P[1] == polygon[i][1] ):
                polygon1.append(polygon[i])
                j = i+1
                break
            if( P[0] == polygon[i+1][0] and P[1] == polygon[i+1][1] ):
                polygon1.append(polygon[i])
                polygon1.append(P)
                j = i+1
                break
            polygon1.append(polygon[i])
            polygon1.append(P)
            polygon2.append(P)
            j = i + 1
            break
        polygon1.append(polygon[i])

    for i in range(j, len(polygon)):
        polygon2.append(polygon[i])

    return [polygon1, polygon2]

# return polygon, read from file
def polygon_from_file(file_name):
    try:
        file = open(file_name, 'r')
    except OSError:
        return -1
    
    polygon = []
    for line in file:
        try:
            polygon.append([float(x) for x in line.split()])
        except ValueError:
            return -2
        
    return polygon

def AutoTest1():
    polygon = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
    P = share_polygon(polygon, 1, 1)
    if P[0] == 1 and P[1] == 1: return True
    else: return False

def AutoTest2():
    polygon = [(2, -1), (7, -1), (10, 2), (7, 6), (1, 6), (-1, 3)]
    P = share_polygon(polygon, 5, 2)
    if P[0] > 3 and P[0] < 4 and P[1] == 6.0: return True
    else: return False

def AutoTest():
    all = 1
    if(AutoTest1() == 0):
        all = 0
        print("Error! AutoTest1 is failed.")
    if(AutoTest2() == 0):
        all = 0
        print("Error! AutoTest2 is failed.")
    
    return all

def main():
    if(AutoTest() == 0):
        return
    
    polygon = polygon_from_file(input("Input file name: "))

    if polygon == -1:
        print("Error! Cannot open file!")
        return
        
    if polygon == -2:
        print("Error! Wrong data!")
        return

    if(len(polygon) < 3):
        print("Error! Bad polygon.")
        return
    
    n = input("Input n: ")
    m = input("Input m: ")
    try:
        n = int(n)
        m = int(m)
    except ValueError:
        print("Error! Wrong n and m!")
        return

    if( m < 1 or n < 1): 
        print("Error! Wrong m and n!")
        return

    print("S: ", polygon_area(polygon))
    polygons = devide_polygon(polygon, n, m)
    print(polygons[0])
    print(polygons[1])
    print("S1; ", polygon_area(polygons[0]))
    print("S2: ", polygon_area(polygons[1]))
    print("k: ", polygon_area(polygons[0])/polygon_area(polygons[1]))

main()


