import pandas as pd
import matplotlib.pyplot as plt

interface_length = 5

def wiring_rect_below(dist: float, df: pd.DataFrame) -> pd.DataFrame:
    def f_inflection_x(x):
        if x.dx < 10:
            return list([x.sx, x.sx, x.sx+10, x.sx+10, x.lx, x.lx])
        else:
            return list([round(x.sx, 4), round(x.sx, 4), round(x.lx, 4), round(x.lx, 4)])

    def f_inflection_y(x, gap):
        if x.dx < 10:
            return list([x.sy, x.inflection, x.inflection, x.inflection+10, x.inflection+10, x.ly])
        else:
            return list([x.sy, x.inflection if x.inflection < 10 else x.inflection+10-gap, x.inflection if x.inflection < 10 else x.inflection+10-gap, x.ly])

    df2 = df.copy()
    df2 = df2[(df2["sy"]==0)]

    list_inflection = [(i * dist + interface_length for i in range(df2[df2["dz"] == layer].shape[0])) for layer in range(4)]
    df2['inflection'] = df2.apply(lambda x: next(list_inflection[x.dz]), axis=1)
    gap = [df2[(df2["dx"] >= 10) & (df2["inflection"] < 15) & (df2["dz"] == layer)].shape[0] * dist for layer in range(4)]
    df2['inflection_x'] = df2.apply(lambda x: f_inflection_x(x), axis=1)
    df2['inflection_y'] = df2.apply(lambda x: f_inflection_y(x, gap[x.dz]), axis=1)

    return df2

def wiring_rect_above(dist: float, df: pd.DataFrame) -> pd.DataFrame:
    def f_inflection_x(x):
        if x.dx == 0:
            return list([x.sx, x.lx])
        elif x.dx < 10:
            return list([x.sx, x.sx, x.sx+10, x.sx+10, x.lx, x.lx])
        else:
            return list([round(x.sx, 4), round(x.sx, 4), round(x.lx, 4), round(x.lx, 4)])

    def f_inflection_y(x, gap):
        if x.dx == 0:
            return list([x.sy, x.ly])
        elif x.dx < 10:
            return list([x.sy, x.inflection, x.inflection, x.inflection-10, x.inflection-10, x.ly])
        else:
            return list([x.sy, x.inflection if x.inflection > 90 else x.inflection-10+gap, x.inflection if x.inflection > 90 else x.inflection-10+gap, x.ly])

    df4 = df.copy()
    df4 = df4[(df4["sy"]!=0)]

    list_inflection = [(100 - (i * dist + interface_length) for i in range(df4[df4["dz"]==layer].shape[0])) for layer in range(4)]
    df4['inflection'] = df4.apply(lambda x: next(list_inflection[x.dz]), axis=1)
    gap = [df4[(df4["dx"] > 10) & (df4["inflection"] > 85) & (df4["dz"] == layer)].shape[0] * dist for layer in range(4)]
    df4['inflection_x'] = df4.apply(lambda x: f_inflection_x(x), axis=1)
    df4['inflection_y'] = df4.apply(lambda x: f_inflection_y(x, gap[x.dz]), axis=1)

    return df4

def plotter_rect(df: pd.DataFrame, line_width: float, dist: float, save_folder: str = './results/') -> pd.DataFrame:
    df2 = wiring_rect_below(dist, df)
    # df2.to_excel(save_folder + "fiberBoard826data.xlsx")
    df4 = wiring_rect_above(dist, df)
    df = pd.concat([df2, df4], axis=0)
    # df.to_excel(save_folder + "fiberBoard826data.xlsx")

    fig = plt.figure()
    ax = plt.gca()
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    for i in range(df2.shape[0]):
        x_list = df2['inflection_x'].tolist()[i]
        y_list = df2['inflection_y'].tolist()[i]
        ax.plot(x_list, y_list, color='r', linewidth=line_width, alpha=0.8)
    fig.savefig(save_folder + 'fiberBoard826_below.pdf', dpi=3000, format='pdf')

    '''
    fig = plt.figure()
    ax = plt.gca()
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    for i in range(df3.shape[0]):
        x_list = df3['inflection_x'].tolist()[i]
        y_list = df3['inflection_y'].tolist()[i]
        ax.plot(x_list, y_list, color='y', linewidth=line_width, alpha=0.8)
    fig.savefig(save_folder + 'fiberBoard826_below_above.pdf', dpi=3000, format='pdf')
    '''

    fig = plt.figure()
    ax = plt.gca()
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    for i in range(df4.shape[0]):
        x_list = df4['inflection_x'].tolist()[i]
        y_list = df4['inflection_y'].tolist()[i]
        ax.plot(x_list, y_list, color='b', linewidth=line_width, alpha=0.8)
    fig.savefig(save_folder + 'fiberBoard826_above.pdf', dpi=3000, format='pdf')

    '''
    fig = plt.figure()
    ax = plt.gca()
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    for i in range(df5.shape[0]):
        x_list = df5['inflection_x'].tolist()[i]
        y_list = df5['inflection_y'].tolist()[i]
        ax.plot(x_list, y_list, color='g', linewidth=line_width, alpha=0.8)
    fig.savefig(save_folder + 'fiberBoard826_above_below.pdf', dpi=3000, format='pdf')
    '''

    fig = plt.figure()
    ax = plt.gca()
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    for i in range(df.shape[0]):
        x_list = df['inflection_x'].tolist()[i]
        y_list = df['inflection_y'].tolist()[i]
        ax.plot(x_list, y_list, color='g', linewidth=line_width, alpha=0.8)
    fig.savefig(save_folder + 'fiberBoard826_rect.pdf', dpi=3000, format='pdf')

    df.to_excel(save_folder+"fiberBoard826rect.xlsx")
    return df


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