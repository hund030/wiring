import pandas as pd
import matplotlib.pyplot as plt


def wiring_rect_l15_l16(dist: float, df: pd.DataFrame) -> pd.DataFrame:
    def f_inflection_x_l15_l16(x):
        return list(
            [round(x.lx, 4), round(x.lx + 5 + x.inflection_x, 4), round(x.lx + 5 + x.inflection_x, 4), round(x.sx, 4),
             round(x.sx, 4)])

    def f_inflection_y_l15_l16(x):
        return list(
            [round(x.ly, 4), round(x.ly, 4), round(x.sy - 5 - x.inflection_y, 4), round(x.sy - 5 - x.inflection_y, 4),
             round(x.sy, 4)])

    df2 = df.copy()
    df2 = df2[df2['L'].isin([15, 16])]
    df2 = df2.sort_values(by="ly", ascending=False)

    list_inflection_x = [i * dist for i in range(df2.shape[0])]
    list_inflection_x.reverse()
    dict_inflection_x = {'inflection_x': list_inflection_x}
    df_x_temp = pd.DataFrame(dict_inflection_x, columns=['inflection_x'])

    list_inflection_y = [i * dist for i in range(df2.shape[0])]
    dict_inflection_y = {'inflection_y': list_inflection_y}
    df_y_temp = pd.DataFrame(dict_inflection_y, columns=['inflection_y'])

    df2 = df2.reset_index()
    df2 = pd.concat([df2, df_x_temp, df_y_temp], axis=1)

    df2['inflection_x'] = df2.apply(f_inflection_x_l15_l16, axis=1)
    df2['inflection_y'] = df2.apply(f_inflection_y_l15_l16, axis=1)

    return df2


def wiring_rect_l9_l10(dist: float, df: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    # df2 = wiring_rect_l15_l16(dist, df)
    def f_inflection_x_l9_l10(x):
        return list(
            [round(x.lx, 4), round(x.lx + 5 + x.inflection_x, 4), round(x.lx + 5 + x.inflection_x, 4), round(x.sx, 4),
             round(x.sx, 4)])

    def f_inflection_y_l9_l10(x):
        return list(
            [round(x.ly, 4), round(x.ly, 4), round(df2['inflection_y'][df2.shape[0] - 1][3] - dist - x.inflection_y, 4),
             round(df2['inflection_y'][df2.shape[0] - 1][3] - dist - x.inflection_y, 4), round(x.sy, 4)])

    df3 = df.copy()
    df3 = df3[df3['L'].isin([9, 10])]
    df3 = df3.sort_values(by="ly", ascending=False)

    list_inflection_x = [i * dist for i in range(df3.shape[0])]
    dict_inflection_x = {'inflection_x': list_inflection_x}
    df_x_temp = pd.DataFrame(dict_inflection_x, columns=['inflection_x'])

    list_inflection_y = [i * dist for i in range(df3.shape[0])]
    dict_inflection_y = {'inflection_y': list_inflection_y}
    df_y_temp = pd.DataFrame(dict_inflection_y, columns=['inflection_y'])

    df3 = df3.reset_index()
    df3 = pd.concat([df3, df_x_temp, df_y_temp], axis=1)

    df3['inflection_x'] = df3.apply(f_inflection_x_l9_l10, axis=1)
    df3['inflection_y'] = df3.apply(f_inflection_y_l9_l10, axis=1)

    return df3


def wiring_rect_l17_l18(dist: float, df: pd.DataFrame) -> pd.DataFrame:
    def f_inflection_x_l17_118(x):
        return list(
            [round(x.lx, 4), round(x.lx - 5 - x.inflection_x, 4), round(x.lx - 5 - x.inflection_x, 4), round(x.sx, 4),
             round(x.sx, 4)])

    def f_inflection_y_l17_118(x):
        return list(
            [round(x.ly, 4), round(x.ly, 4), round(x.sy + 5 + x.inflection_y, 4), round(x.sy + 5 + x.inflection_y, 4),
             round(x.sy, 4)])

    df4 = df.copy()
    df4 = df4[df4['L'].isin([17, 18])]
    df4 = df4.sort_values(by="ly", ascending=True)

    list_inflection_x = [i * dist for i in range(df4.shape[0])]
    list_inflection_x.reverse()
    dict_inflection_x = {'inflection_x': list_inflection_x}
    df_x_temp = pd.DataFrame(dict_inflection_x, columns=['inflection_x'])

    list_inflection_y = [i * dist for i in range(df4.shape[0])]
    dict_inflection_y = {'inflection_y': list_inflection_y}
    df_y_temp = pd.DataFrame(dict_inflection_y, columns=['inflection_y'])

    df4 = df4.reset_index()
    df4 = pd.concat([df4, df_x_temp, df_y_temp], axis=1)

    df4['inflection_x'] = df4.apply(f_inflection_x_l17_118, axis=1)
    df4['inflection_y'] = df4.apply(f_inflection_y_l17_118, axis=1)

    return df4


def wiring_rect_l23_l24(dist: float, df: pd.DataFrame, df4: pd.DataFrame) -> pd.DataFrame:
    # df4 = wiring_rect_l17_l18(dist, df)
    def f_inflection_x_l23_124(x):
        return list(
            [round(x.lx, 4), round(x.lx - 5 - x.inflection_x, 4), round(x.lx - 5 - x.inflection_x, 4), round(x.sx, 4),
             round(x.sx, 4)])

    def f_inflection_y_l23_124(x):
        return list(
            [round(x.ly, 4), round(x.ly, 4), round(df4['inflection_y'][df4.shape[0] - 1][2] + dist + x.inflection_y, 4),
             round(df4['inflection_y'][df4.shape[0] - 1][2] + dist + x.inflection_y, 4), round(x.sy, 4)])

    df5 = df.copy()
    df5 = df5[df5['L'].isin([23, 24])]
    df5 = df5.sort_values(by="ly", ascending=True)

    list_inflection_x = [i * dist for i in range(df5.shape[0])]
    dict_inflection_x = {'inflection_x': list_inflection_x}
    df_x_temp = pd.DataFrame(dict_inflection_x, columns=['inflection_x'])

    list_inflection_y = [i * dist for i in range(df5.shape[0])]
    dict_inflection_y = {'inflection_y': list_inflection_y}
    df_y_temp = pd.DataFrame(dict_inflection_y, columns=['inflection_y'])

    df5 = df5.reset_index()
    df5 = pd.concat([df5, df_x_temp, df_y_temp], axis=1)

    df5['inflection_x'] = df5.apply(f_inflection_x_l23_124, axis=1)
    df5['inflection_y'] = df5.apply(f_inflection_y_l23_124, axis=1)

    return df5


def plotter_rect(df: pd.DataFrame, line_width: float, dist: float, save_folder: str = './results/') -> pd.DataFrame:
    # wiring_order: L15_16 -> L9_10 -> L17_18 -> L23_24
    df2 = wiring_rect_l15_l16(dist, df)
    df3 = wiring_rect_l9_l10(dist, df, df2)
    df4 = wiring_rect_l17_l18(dist, df)
    df5 = wiring_rect_l23_l24(dist, df, df4)

    fig = plt.figure()
    ax = plt.gca()
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    for i in range(df2.shape[0]):
        x_list = df2['inflection_x'][i]
        y_list = df2['inflection_y'][i]
        ax.plot(x_list, y_list, color='r', linewidth=line_width, alpha=0.8)
    fig.savefig(save_folder+'fiberBoard896_l15_l16.pdf', dpi=3000, format='pdf')

    fig = plt.figure()
    ax = plt.gca()
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    for i in range(df3.shape[0]):
        x_list = df3['inflection_x'][i]
        y_list = df3['inflection_y'][i]
        ax.plot(x_list, y_list, color='b', linewidth=line_width, alpha=0.8)
    fig.savefig(save_folder+'fiberBoard896_l9_10.pdf', dpi=3000, format='pdf')

    fig = plt.figure()
    ax = plt.gca()
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    for i in range(df4.shape[0]):
        x_list = df4['inflection_x'][i]
        y_list = df4['inflection_y'][i]
        ax.plot(x_list, y_list, color='m', linewidth=line_width, alpha=0.8)
    fig.savefig(save_folder+'fiberBoard896_l17_118.pdf', dpi=3000, format='pdf')

    fig = plt.figure()
    ax = plt.gca()
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    for i in range(df5.shape[0]):
        x_list = df5['inflection_x'][i]
        y_list = df5['inflection_y'][i]
        ax.plot(x_list, y_list, color='c', linewidth=line_width, alpha=0.8)
    fig.savefig(save_folder+'fiberBoard896_l23_124.pdf', dpi=3000, format='pdf')

    fig = plt.figure()
    ax = plt.gca()
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    for i in range(df2.shape[0]):
        x_list = df2['inflection_x'][i]
        y_list = df2['inflection_y'][i]
        ax.plot(x_list, y_list, color='r', linewidth=line_width, alpha=0.8)
    for i in range(df3.shape[0]):
        x_list = df3['inflection_x'][i]
        y_list = df3['inflection_y'][i]
        ax.plot(x_list, y_list, color='b', linewidth=line_width, alpha=0.8)
    for i in range(df4.shape[0]):
        x_list = df4['inflection_x'][i]
        y_list = df4['inflection_y'][i]
        ax.plot(x_list, y_list, color='m', linewidth=line_width, alpha=0.8)
    for i in range(df5.shape[0]):
        x_list = df5['inflection_x'][i]
        y_list = df5['inflection_y'][i]
        ax.plot(x_list, y_list, color='c', linewidth=line_width, alpha=0.8)
    fig.savefig(save_folder+'fiberBoard896rect.svg', dpi=3000, format='svg')
    fig.savefig(save_folder+'fiberBoard896rect.pdf', dpi=3000, format='pdf')

    df_coor = pd.concat([pd.concat([df2['NUM'], df2['inflection_x'], df2['inflection_y']], axis=1),
                         pd.concat([df3['NUM'], df3['inflection_x'], df3['inflection_y']], axis=1),
                         pd.concat([df4['NUM'], df4['inflection_x'], df4['inflection_y']], axis=1),
                         pd.concat([df5['NUM'], df5['inflection_x'], df5['inflection_y']], axis=1)
                         ], axis=0)

    df_coor = df_coor.sort_values(by="NUM", ascending=True)
    df_coor = df_coor.reset_index()

    data_res = pd.concat([df, df_coor['inflection_x'], df_coor['inflection_y']], axis=1)
    data_res.to_excel(save_folder+"fiberBoard896rect.xlsx")

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