import pandas as pd
import numpy as np
from numpy.linalg import norm
import ast

def calc_index(data: pd.DataFrame, line_width: float, bend_radius: float, plain_square: float) -> pd.DataFrame:
    def calc_length(x):
        if x.dx < 2 * bend_radius:
            theta = np.arccos((bend_radius - x.dx * 0.5) / bend_radius)
            bend_length = 2 * bend_radius * theta
            vertical_length = np.abs(x.sy - x.inflection) + np.abs(x.ly - x.inflection) - 2 * bend_radius * np.sin(theta)
            return bend_length + vertical_length
        else:
            bend_length = bend_radius * np.pi
            vertical_length = np.abs(x.sy - x.inflection) + np.abs(x.ly - x.inflection) - 2 * bend_radius
            horizontal_length = x.dx - 2 * bend_radius
            return bend_length + vertical_length + horizontal_length

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]
    
    def is_fall_on(p, line):
        return p[0] >= min(line[0][0], line[1][0]) and p[0] <= max(line[0][0], line[1][0]) and \
               p[1] >= min(line[0][1], line[1][1]) and p[1] <= max(line[0][1], line[1][1])

    def is_cross(line1, line2):
        xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
        ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

        div = det(xdiff, ydiff)
        if div == 0:
            return False, None
        d = (det(*line1), det(*line2))
        # 
        x = np.round(det(d, xdiff) / div, 1)
        y = np.round(det(d, ydiff) / div, 1)
        return is_fall_on((x,y), line1) and is_fall_on((x,y), line2), (x,y)

    def calc_crossing(row):
        def is_across_at_bend(p, line1, line2):
            # line1 vertical which means line2 horizontal
            if np.abs(line1[0][0] - line1[1][0]) < 0.1:
                return int(np.abs(p[0] - line2[0][0]) < bend_radius) + int(np.abs(p[0] - line2[1][0]) < bend_radius) * 2 + \
                    int(np.abs(p[1] - line1[0][1]) < bend_radius or np.abs(p[1] - line1[1][1]) < bend_radius) * 3
            # else line1 horizontal which means line2 vertical
            else:
                return -int(np.abs(p[0] - line1[0][0]) < bend_radius) - int(np.abs(p[0] - line1[1][0]) < bend_radius) * 2 - \
                    int(np.abs(p[1] - line2[0][1]) < bend_radius or np.abs(p[1] - line2[1][1]) < bend_radius) * 3
        
        def line_to_arc(center, line, idx):
            p0 = np.asarray(center)
            p1 = np.asarray(line[0])
            p2 = np.asarray(line[1])
            d = np.abs(np.cross(p2 - p1, p1 - p0) / norm(p2 - p1))
            if d < bend_radius:
                return np.round(np.arccos(d/bend_radius), 4)
            else:
                return 0
        
        def arc_to_arc(center1, center2, idx):
            p1 = np.asarray(center1)
            p2 = np.asarray(center2)
            d = norm(p1 - p2)
            if d < 2 * bend_radius:
                return np.round(np.arccos(1 - d ** 2 / (2 * bend_radius ** 2)), 4)
            else:
                return 0

        def f(lines, center1, x, y, center2):
            for i in range(len(x) - 1):
                for j, line1 in enumerate(lines):
                    line2 = ((x[i], y[i]), (x[i + 1], y[i + 1]))
                    if line1 == line2:
                        return None
                    ok, p = is_cross(line1, line2)
                    if ok:
                        return {
                            -1: line_to_arc(center1[0], line2, -1),
                            -2: line_to_arc(center1[1], line2, -2),
                            -3: line_to_arc(center2[0], line1, -3) if line2[0][1] == 0 or line2[0][1] == 100 else line_to_arc(center2[1], line1, 3),
                            -4: arc_to_arc(center1[0], center2[0], -4) if line2[0][1] == 0 or line2[0][1] == 100 else arc_to_arc(center1[0], center2[1], -4),
                            -5: arc_to_arc(center1[1], center2[0], -5) if line2[0][1] == 0 or line2[0][1] == 100 else arc_to_arc(center1[1], center2[1], -5),
                            1: line_to_arc(center2[0], line1, 1),
                            2: line_to_arc(center2[1], line1, 2),
                            3: line_to_arc(center1[0], line2, 3) if line1[0][1] == 0 or line1[0][1] == 100 else line_to_arc(center1[1], line2, -3),
                            4: arc_to_arc(center2[0], center1[0], 4) if line1[0][1] == 0 or line1[0][1] == 100 else arc_to_arc(center2[0], center1[1], 4),
                            5: arc_to_arc(center2[1], center1[0], 5) if line1[0][1] == 0 or line1[0][1] == 100 else arc_to_arc(center2[1], center1[1], 5),
                            0: np.round(np.pi/2, 4),
                        }[is_across_at_bend(p, line1, line2)]
            return None

        lines = []
        # the length of inflection_x and inflection_y should be the same
        for i in range(len(row.inflection_x) - 1):
            lines.append(((row.inflection_x[i], row.inflection_y[i]), (row.inflection_x[i + 1], row.inflection_y[i + 1])))

        points = [f(lines, row.center, r[0], r[1], r[2]) for r in data[["inflection_x", "inflection_y", "center"]].values]
        points = [p for p in points if p != None]
        '''
        for index, row in data.iterrows():
            if index == x.name:
                continue
            for i in range(len(row.inflection_x) - 1):
                for line1 in lines:
                    # ok shows is there an intersection, p indicates the intersection
                    line2 = ((row.inflection_x[i], row.inflection_y[i]), (row.inflection_x[i + 1], row.inflection_y[i + 1]))
                    ok, p = is_cross(line1, line2)
                    if ok:
                        points.append(p)
        '''
        if 0 in points:
            print(points)
        return points
    
    '''
    data["inflection_x"] = data.apply(lambda x: x.inflection_x[1:-1].split(','), axis=1)
    data["inflection_x"] = data.apply(lambda x: [float(v) for v in x.inflection_x], axis=1)
    data["inflection_y"] = data.apply(lambda x: x.inflection_y[1:-1].split(','), axis=1)
    data["inflection_y"] = data.apply(lambda x: [float(v) for v in x.inflection_y], axis = 1)
    '''
    data["inflection_x"] = data.apply(lambda x: ast.literal_eval(x.inflection_x), axis=1)
    data["inflection_y"] = data.apply(lambda x: ast.literal_eval(x.inflection_y), axis=1)
    data["center"] = data.apply(lambda x: ast.literal_eval(x.center), axis=1)
    data = data.sort_values(by="inflection", ascending=True)
    data["length"] = data.apply(lambda x: np.round(calc_length(x), 4), axis=1)
    bg_density = np.round(np.sum(data["length"]) * line_width / plain_square, 4)
    # print(bg_density)
    data["anglss"] = data.apply(lambda x: calc_crossing(x), axis = 1)
    data["crossing"] = data.apply(lambda x: len(x.anglss), axis = 1)
    data.to_excel("fiberBoard256calc.xlsx")
    
    return data