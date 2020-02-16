import pandas as pd
import numpy as np

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
        def f(lines, x, y):
            for i in range(len(x) - 1):
                for line1 in lines:
                    line2 = ((x[i], y[i]), (x[i + 1], y[i + 1]))
                    if line1 == line2:
                        return None
                    ok, p = is_cross(line1, line2)
                    if ok:
                        return p
            return None

        lines = []
        # the length of inflection_x and inflection_y should be the same
        for i in range(len(row.inflection_x) - 1):
            lines.append(((row.inflection_x[i], row.inflection_y[i]), (row.inflection_x[i + 1], row.inflection_y[i + 1])))

        points = [f(lines, x, y) for x, y in zip(data["inflection_x"], data["inflection_y"])]
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
        return len(points)

    data["inflection_x"] = data.apply(lambda x: x.inflection_x[1:-1].split(','), axis=1)
    data["inflection_x"] = data.apply(lambda x: [float(v) for v in x.inflection_x], axis=1)
    data["inflection_y"] = data.apply(lambda x: x.inflection_y[1:-1].split(','), axis=1)
    data["inflection_y"] = data.apply(lambda x: [float(v) for v in x.inflection_y], axis=1)
    data = data.sort_values(by="inflection", ascending=True)
    data["length"] = data.apply(lambda x: np.round(calc_length(x), 4), axis=1)
    bg_density = np.round(np.sum(data["length"]) * line_width / plain_square, 4)
    # print(bg_density)
    data["crossing"] = data.apply(lambda x: calc_crossing(x), axis=1)
    data.to_excel("fiberBoard256calc.xlsx")
    
    return data