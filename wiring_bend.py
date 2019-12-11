import pandas as pd
import numpy as np
import gdspy
import matplotlib.pyplot as plt

def plotter_bend(df_rect: pd.DataFrame, line_width: float, dist: float, bend_radius: float = 5.0, delta_arc: float = 0.001, save_folder: str = './results/') -> pd.DataFrame:
    def dir_norm(a: list) -> list:
        for i in range(len(a)):
            if a[i] > 0:
                a[i] = 1
            elif a[i] < 0:
                a[i] = -1
        return a

    def dir_list(x):
        # <todo>
        # ("'function' object does not support item assignment", 'occurred at index 0')
        # dir_list如何初始化更有利于维护？
        dir_list = []
        for i in range(len(x.inflection_x) - 2):
            # ignore the starting point and ending point
            # the current index is i+1
            dir_in = dir_norm([x.inflection_x[i] - x.inflection_x[i + 1], x.inflection_y[i] - x.inflection_y[i + 1]])
            dir_out = dir_norm(
                [x.inflection_x[i + 2] - x.inflection_x[i + 1], x.inflection_y[i + 2] - x.inflection_y[i + 1]])
            dir_list.append(tuple(np.array(dir_in) + np.array(dir_out)))
        return dir_list

    def elements_round_list(a: list) -> list:
        for i in range(len(a)):
            a[i] = round(a[i], 4)
        return a

    def bend_x_list(x):
        # bend_x_list=list(np.zeros((len(x.inflection_x)-2)*2+2,))
        bend_x_list = []
        for i in range(len(x.inflection_x) - 2):
            # ignore the starting point and ending point
            # the current index is i+1
            dir_in = dir_norm([x.inflection_x[i] - x.inflection_x[i + 1], x.inflection_y[i] - x.inflection_y[i + 1]])
            dir_out = dir_norm(
                [x.inflection_x[i + 2] - x.inflection_x[i + 1], x.inflection_y[i + 2] - x.inflection_y[i + 1]])
            bend_x_list = bend_x_list + [x.inflection_x[i + 1] + bend_radius * dir_in[0],
                                         x.inflection_x[i + 1] + bend_radius * dir_out[0]]
        # bend_x_list = [x.inflection_x[0]] + bend_x_list + [x.inflection_x[-1]]
        return elements_round_list(bend_x_list)

    '''
    def bend_x_list(x):
        bend_x_list = []
        for i in range(len(x.inflection_x) - 2):
            # ignore the starting point and ending point
            # the current index is i+1
            dir_in = dir_norm([x.inflection_x[i] - x.inflection_x[i + 1], x.inflection_y[i] - x.inflection_y[i + 1]])
            dir_out = dir_norm(
                [x.inflection_x[i + 2] - x.inflection_x[i + 1], x.inflection_y[i + 2] - x.inflection_y[i + 1]])
            bend_x_list = bend_x_list + [x.inflection_x[i + 1] + bend_radius * dir_in[0],
                                         x.inflection_x[i + 1] + bend_radius * dir_out[0]]
        return elements_round_list(bend_x_list)
    '''

    def bend_y_list(x):
        bend_y_list = []
        for i in range(len(x.inflection_x) - 2):
            # ignore the starting point and ending point
            # the current index is i+1
            dir_in = dir_norm([x.inflection_x[i] - x.inflection_x[i + 1], x.inflection_y[i] - x.inflection_y[i + 1]])
            dir_out = dir_norm(
                [x.inflection_x[i + 2] - x.inflection_x[i + 1], x.inflection_y[i + 2] - x.inflection_y[i + 1]])
            bend_y_list = bend_y_list + [x.inflection_y[i + 1] + bend_radius * dir_in[1],
                                         x.inflection_y[i + 1] + bend_radius * dir_out[1]]
        return elements_round_list(bend_y_list)

    def center_list(x):
        # <todo>
        # 同dir_list如何初始化更有利于维护？
        center_list = []
        for i in range(len(x.dir)):
            center_list.append(tuple(
                np.array([x.inflection_x[i + 1], x.inflection_y[i + 1]]) + bend_radius * np.array(x.dir[i])))
        return center_list

    dir_map = [(-1.0, -1.0), (1.0, -1.0), (1.0, 1.0), (-1.0, 1.0)]
    theta_map = [(0, np.pi / 2), (np.pi / 2, np.pi), (np.pi, np.pi / 2 * 3), (np.pi / 2 * 3, 2 * np.pi)]

    df = df_rect.copy()
    df["dir"] = df.apply(dir_list, axis=1)
    df["center"] = df.apply(center_list, axis=1)
    df["bend_x"] = df.apply(bend_x_list, axis=1)
    df["bend_y"] = df.apply(bend_y_list, axis=1)


    fig = plt.figure()
    ax = plt.gca()

    ax.set_xlabel('x')
    ax.set_ylabel('y')

    target = [[9, 10], [15, 16], [17, 18], [23, 24]]
    color = ['r', 'b', 'm', 'c']
    for index in range(4):
        for i in range(int(df.shape[0] / 4)):
            tempx = df[df['MT'].isin(target[index])]['inflection_x'].tolist()
            tempy = df[df['MT'].isin(target[index])]['inflection_y'].tolist()
            bendx = df[df['MT'].isin(target[index])]['bend_x'].tolist()
            bendy = df[df['MT'].isin(target[index])]['bend_y'].tolist()
            dir_list = df[df['MT'].isin(target[index])]["dir"].tolist()[i]
            center_list = df[df['MT'].isin(target[index])]["center"].tolist()[i]

            x_list = [tempx[i][0]] + bendx[i] + [tempx[i][-1]]
            y_list = [tempy[i][0]] + bendy[i] + [tempy[i][-1]]
            theta_list = [theta_map[dir_map.index(dir_list[j])] for j in range(len(dir_list))]
            j = 0
            for k in range(int(len(x_list) / 2)):
                ax.plot(x_list[j:j + 2], y_list[j:j + 2], color=color[index], linewidth=line_width, alpha=0.8)
                j = j + 2
            for k in range(int(len(center_list))):
                arc_x_list = list(
                    center_list[k][0] + bend_radius * np.cos(np.arange(theta_list[k][0], theta_list[k][1], delta_arc)))
                arc_y_list = list(
                    center_list[k][1] + bend_radius * np.sin(np.arange(theta_list[k][0], theta_list[k][1], delta_arc)))
                ax.plot(arc_x_list, arc_y_list, color=color[index], linewidth=line_width, alpha=0.8)

    fig.savefig(save_folder+'fiberBoard896bend.svg', dpi=3000, format='svg')
    fig.savefig(save_folder+'fiberBoard896bend.pdf', dpi=3000, format='pdf')

    df.to_excel(save_folder + "fiberBoard896bend.xlsx")

    return df


def svg2gds_bend(df: pd.DataFrame, line_width: float = 0.125, bend_radius: float = 5, gds_filename: str = 'fiberBoard896bend.gds', save_folder: str = './results/') -> None:
    gdspy.current_library = gdspy.GdsLibrary()
    # gdspy.unit=1e-3
    cell = gdspy.Cell('wiring896')
    for i in range(df.shape[0]):
        points = []
        for j in range(len(df["inflection_x"][i])):
            points = points + [tuple([df["inflection_x"][i][j], df["inflection_y"][i][j]])]

        # multiply 1000 to convert mm to um
        sp = gdspy.FlexPath(points, line_width, corners="circular bend", bend_radius=bend_radius, gdsii_path=True)
        cell.add(sp)
    gdspy.write_gds(save_folder + gds_filename)
