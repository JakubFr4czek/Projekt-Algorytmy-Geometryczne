from bitalg.visualizer.main import Visualizer

def mbr(hull_points, CalculationType = "area"):

    #Krawędzie
    edges = []
    for i in range(1, len(hull_points)):
        edges.append( (hull_points[i - 1], hull_points[i]) )
    edges.append( (hull_points[-1], hull_points[0]) )

    #Wektory kierunkowe krawędzi
    dir_vec = []
    for edge in edges:
        dir_vec.append( ( (edge[1][0] - edge[0][0]), (edge[1][1] - edge[0][1]) ) )

    #Długości krawędzi (długości wektorów)
    edges_len = []
    for vec in dir_vec:
        edges_len.append( (vec[0]**2 + vec[1]**2)**(1/2) ) 

    #Normalizacja wektorów
    norm_vec = []
    for i in range(len(dir_vec)):
        norm_vec.append( (dir_vec[i][0] / edges_len[i], dir_vec[i][1] / edges_len[i]) )

    #Wektory prostopadłe
    perp_vec = []
    for i in range(len(norm_vec)):
        perp_vec.append( (-norm_vec[i][1], norm_vec[i][0]) )

    #Mnożę punkty przez wektory i szukam wartosci maksymalnych i minimalnych
    
    minX = [] 
    maxX = [] 

    for i in range(len(norm_vec)):

        minXVal = float('inf')
        maxXVal = float('-inf')

        for j in range(len(hull_points)):

            temp = hull_points[j][0] * norm_vec[i][0] + hull_points[j][1] * norm_vec[i][1]

            #vis.add_point(temp, color = 'brown')

            if temp > maxXVal:
                maxXVal = temp
            
            if temp < minXVal:
                minXVal = temp
        
        minX.append(minXVal)
        maxX.append(maxXVal)

        
    minY = []
    maxY = []

    for i in range(len(perp_vec)):
        
        minYVal = float('inf')
        maxYVal = float('-inf')

        for j in range(len(hull_points)):

            temp = hull_points[j][0] * perp_vec[i][0] + hull_points[j][1] * perp_vec[i][1]

            #print(temp)

            if temp > maxYVal:
                maxYVal = temp
            
            if temp < minYVal:
                minYVal = temp
        
        minY.append(minYVal)
        maxY.append(maxYVal)

    minArea = float('inf')
    minAreaIdx = -1

    for i in range(len(minX)):

        if CalculationType == "area":
            area = abs(minX[i] - maxX[i]) * abs(minY[i] - maxY[i])
        elif CalculationType == "perimiter":
            area = 2 * abs(minX[i] - maxX[i]) + abs(minY[i] - maxY[i])

        if area < minArea:
            minArea = area
            minAreaIdx = i

    print(CalculationType, ": ", minArea)

    pts = [(minX[minAreaIdx],minY[minAreaIdx]),
           (maxX[minAreaIdx], minY[minAreaIdx]),
           (maxX[minAreaIdx], maxY[minAreaIdx]),
           (minX[minAreaIdx], maxY[minAreaIdx])]
    
    for i in range(len(pts)):

        pts[i] = (pts[i][0] * norm_vec[minAreaIdx][0] + pts[i][1] * perp_vec[minAreaIdx][0], pts[i][0] * norm_vec[minAreaIdx][1] + pts[i][1] *perp_vec[minAreaIdx][1])

    return pts

def mbr_draw(hull_points, CalculationType = "area"):

    vis = Visualizer()

    vis.add_point(hull_points)

    for i in range(1, len(hull_points)):
        vis.add_line_segment( (hull_points[i - 1], hull_points[i]) )
    vis.add_line_segment( (hull_points[-1], hull_points[0]) )

    #Krawędzie
    edges = []
    for i in range(1, len(hull_points)):
        edges.append( (hull_points[i - 1], hull_points[i]) )
    edges.append( (hull_points[-1], hull_points[0]) )

    #Wektory kierunkowe krawędzi
    dir_vec = []
    for edge in edges:
        dir_vec.append( ( (edge[1][0] - edge[0][0]), (edge[1][1] - edge[0][1]) ) )

    #Długości krawędzi (długości wektorów)
    edges_len = []
    for vec in dir_vec:
        edges_len.append( (vec[0]**2 + vec[1]**2)**(1/2) ) 

    #Normalizacja wektorów
    norm_vec = []
    for i in range(len(dir_vec)):
        norm_vec.append( (dir_vec[i][0] / edges_len[i], dir_vec[i][1] / edges_len[i]) )

    #Wektory prostopadłe
    perp_vec = []
    for i in range(len(norm_vec)):
        perp_vec.append( (-norm_vec[i][1], norm_vec[i][0]) )

    #Mnożę punkty przez wektory i szukam wartosci maksymalnych i minimalnych
    
    minX = [] 
    maxX = [] 

    for i in range(len(norm_vec)):

        minXVal = float('inf')
        maxXVal = float('-inf')

        for j in range(len(hull_points)):

            temp = hull_points[j][0] * norm_vec[i][0] + hull_points[j][1] * norm_vec[i][1]

            if temp > maxXVal:
                maxXVal = temp
            
            if temp < minXVal:
                minXVal = temp
        
        minX.append(minXVal)
        maxX.append(maxXVal)

        
    minY = []
    maxY = []

    for i in range(len(perp_vec)):
        
        minYVal = float('inf')
        maxYVal = float('-inf')

        for j in range(len(hull_points)):

            temp = hull_points[j][0] * perp_vec[i][0] + hull_points[j][1] * perp_vec[i][1]

            if temp > maxYVal:
                maxYVal = temp
            
            if temp < minYVal:
                minYVal = temp
        
        minY.append(minYVal)
        maxY.append(maxYVal)

    minArea = float('inf')
    minAreaIdx = -1

    for i in range(len(minX)):

        if CalculationType == "area":
            area = abs(minX[i] - maxX[i]) * abs(minY[i] - maxY[i])
        elif CalculationType == "perimiter":
            area = 2 * abs(minX[i] - maxX[i]) + abs(minY[i] - maxY[i])

        if area < minArea:
            minArea = area
            minAreaIdx = i

        tempPts = [(minX[i], minY[i]),
                   (maxX[i], minY[i]),
                   (maxX[i], maxY[i]),
                   (minX[i], maxY[i])]

        for j in range(len(tempPts)):

            tempPts[j] = (tempPts[j][0] * norm_vec[i][0] + tempPts[j][1] * perp_vec[i][0], tempPts[j][0] * norm_vec[i][1] + tempPts[j][1] *perp_vec[i][1])

        rectangles = []

        for i in range(1, len(tempPts)):

            rectangles.append( (tempPts[i - 1], tempPts[i]) )

        rectangles.append( (tempPts[-1], tempPts[0]) )

        temp = vis.add_line_segment(rectangles, color = 'blue')
        vis.remove_figure(temp)


    pts = [(minX[minAreaIdx],minY[minAreaIdx]),
           (maxX[minAreaIdx], minY[minAreaIdx]),
           (maxX[minAreaIdx], maxY[minAreaIdx]),
           (minX[minAreaIdx], maxY[minAreaIdx])]
    
    for i in range(len(pts)):

        pts[i] = (pts[i][0] * norm_vec[minAreaIdx][0] + pts[i][1] * perp_vec[minAreaIdx][0], pts[i][0] * norm_vec[minAreaIdx][1] + pts[i][1] *perp_vec[minAreaIdx][1])
    
    ptsSegments = []
    for i in range(1, len(pts)):
        ptsSegments.append( (pts[i - 1], pts[i]) )
    ptsSegments.append( (pts[-1], pts[0]) )

    vis.add_line_segment(ptsSegments,  color = 'green')

    return pts, vis