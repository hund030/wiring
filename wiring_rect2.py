import pandas as pd
import matplotlib.pyplot as plt

interface_length = 5

def wiring_rect_mt_below(dist: float, df: pd.DataFrame) -> pd.DataFrame:
    def f_inflection_x_below(x):
        return list(
            [round(x.lx, 4), round(x.lx - interface_length - x.inflection_x, 4), round(x.lx - interface_length - x.inflection_x, 4), round(x.sx, 4),
             round(x.sx, 4)])

    def f_inflection_y_below(x):
        return list(
            [round(x.ly, 4), round(x.ly, 4), round(x.sy + interface_length + x.inflection_y, 4), round(x.sy + interface_length + x.inflection_y, 4),
             round(x.sy, 4)])

    df2 = df.copy()
    df2 = df2[df2['MT'].isin([9, 10, 15, 16])]
    df2 = df2.sort_values(by="sx", ascending=False)

    list_inflection_x = [i * dist for i in range(df2.shape[0])]
    # list_inflection_x.reverse()
    dict_inflection_x = {'inflection_x': list_inflection_x}
    df_x_temp = pd.DataFrame(dict_inflection_x, columns=['inflection_x'])

    list_inflection_y = [i * dist for i in range(df2.shape[0])]
    list_inflection_y.reverse()
    dict_inflection_y = {'inflection_y': list_inflection_y}
    df_y_temp = pd.DataFrame(dict_inflection_y, columns=['inflection_y'])

    df2 = df2.reset_index()
    df2 = pd.concat([df2, df_x_temp, df_y_temp], axis=1)

    df2['inflection_x'] = df2.apply(f_inflection_x_below, axis=1)
    df2['inflection_y'] = df2.apply(f_inflection_y_below, axis=1)

    return df2

def wiring_rect_above(dist: float, df: pd.DataFrame) -> pd.DataFrame:
    def f_inflection_x_above(x):
        return list(
            [round(x.lx, 4), round(x.lx + interface_length + x.inflection_x, 4), round(x.lx + interface_length + x.inflection_x, 4), round(x.sx, 4),
             round(x.sx, 4)])

    def f_inflection_y_above(x):
        return list(
            [round(x.ly, 4), round(x.ly, 4), round(x.sy - interface_length - x.inflection_y, 4), round(x.sy - interface_length - x.inflection_y, 4),
             round(x.sy, 4)])

    df4 = df.copy()
    df4 = df4[df4['MT'].isin([17, 18, 23, 24])]
    df4 = df4.sort_values(by="sx", ascending=True)

    list_inflection_x = [i * dist for i in range(df4.shape[0])]
    # list_inflection_x.reverse()
    dict_inflection_x = {'inflection_x': list_inflection_x}
    df_x_temp = pd.DataFrame(dict_inflection_x, columns=['inflection_x'])

    list_inflection_y = [i * dist for i in range(df4.shape[0])]
    list_inflection_y.reverse()
    dict_inflection_y = {'inflection_y': list_inflection_y}
    df_y_temp = pd.DataFrame(dict_inflection_y, columns=['inflection_y'])

    df4 = df4.reset_index()
    df4 = pd.concat([df4, df_x_temp, df_y_temp], axis=1)

    df4['inflection_x'] = df4.apply(f_inflection_x_above, axis=1)
    df4['inflection_y'] = df4.apply(f_inflection_y_above, axis=1)

    return df4

def plotter_rect(df: pd.DataFrame, line_width: float, dist: float, save_folder: str = './results/') -> pd.DataFrame:
    df2 = wiring_rect_mt_below(dist, df)
    df4 = wiring_rect_above(dist, df)

    fig = plt.figure()
    ax = plt.gca()
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    for i in range(df2.shape[0]):
        x_list = df2['inflection_x'][i]
        y_list = df2['inflection_y'][i]
        ax.plot(x_list, y_list, color='r', linewidth=line_width, alpha=0.8)
    fig.savefig(save_folder+'fiberBoard896_below.pdf', dpi=3000, format='pdf')

    fig = plt.figure()
    ax = plt.gca()
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    for i in range(df4.shape[0]):
        x_list = df4['inflection_x'][i]
        y_list = df4['inflection_y'][i]
        ax.plot(x_list, y_list, color='m', linewidth=line_width, alpha=0.8)
    fig.savefig(save_folder+'fiberBoard896_above.pdf', dpi=3000, format='pdf')

    fig = plt.figure()
    ax = plt.gca()
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    for i in range(int(df2.shape[0]/2)):
        x_list = df2[df2['MT'].isin([9, 10])]['inflection_x'].tolist()
        y_list = df2[df2['MT'].isin([9, 10])]['inflection_y'].tolist()
        ax.plot(x_list[i], y_list[i], color='r', linewidth=line_width, alpha=0.8)
    for i in range(int(df2.shape[0]/2)):
        x_list = df2[df2['MT'].isin([15,16])]['inflection_x'].tolist()
        y_list = df2[df2['MT'].isin([15,16])]['inflection_y'].tolist()
        ax.plot(x_list[i], y_list[i], color='b', linewidth=line_width, alpha=0.8)
    for i in range(int(df4.shape[0]/2)):
        x_list = df4[df4['MT'].isin([17,18])]['inflection_x'].tolist()
        y_list = df4[df4['MT'].isin([17,18])]['inflection_y'].tolist()
        ax.plot(x_list[i], y_list[i], color='m', linewidth=line_width, alpha=0.8)
    for i in range(int(df4.shape[0]/2)):
        x_list = df4[df4['MT'].isin([23,24])]['inflection_x'].tolist()
        y_list = df4[df4['MT'].isin([23,24])]['inflection_y'].tolist()
        ax.plot(x_list[i], y_list[i], color='c', linewidth=line_width, alpha=0.8)
    fig.savefig(save_folder+'fiberBoard896rect.svg', dpi=3000, format='svg')
    fig.savefig(save_folder+'fiberBoard896rect.pdf', dpi=3000, format='pdf')

    df_coor = pd.concat([pd.concat([df2['NUM'], df2['inflection_x'], df2['inflection_y']], axis=1),
                         pd.concat([df4['NUM'], df4['inflection_x'], df4['inflection_y']], axis=1),
                         ], axis=0)

    df_coor = df_coor.sort_values(by="NUM", ascending=True)
    df_coor = df_coor.reset_index()

    data_res = pd.concat([df, df_coor['inflection_x'], df_coor['inflection_y']], axis=1)
    # data_res.to_excel(save_folder+"fiberBoard896rect.xlsx")

    return data_res


def svg2dwgscr_rect(data_res: pd.DataFrame, scr_filename: str = "fiberBoard896rect.scr",
                    save_folder: str = './results/') -> None:
    with open(save_folder+scr_filename, "w") as f:
        for i in range(data_res.shape[0]):
            f.write("line {},{} {},{} {},{} {},{} {},{}  \n".format(
                data_res["inflection_x"][i][0], data_res["inflection_y"][i][0],
                data_res["inflection_x"][i][1], data_res["inflection_y"][i][1],
                data_res["inflection_x"][i][2], data_res["inflection_y"][i][2],
                data_res["inflection_x"][i][3], data_res["inflection_y"][i][3],
                data_res["inflection_x"][i][4], data_res["inflection_y"][i][4]))