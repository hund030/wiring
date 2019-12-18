import pandas as pd
import matplotlib.pyplot as plt

interface_length = 5

def wiring_rect_below(dist: float, df: pd.DataFrame) -> pd.DataFrame:
    def f_inflection_x(x):
        return list([round(x.sx, 4), round(x.sx, 4), round(x.lx, 4), round(x.lx, 4)])

    def f_inflection_y(x):
        return list([round(x.sy, 4), round(x.inflection, 4), round(x.inflection, 4), round(x.ly, 4)])

    df2 = df.copy()
    df2 = df2[(df2["sy"]==0) & (df2["ly"]==0)]

    list_inflection = [(i * dist + interface_length for i in range(df2[df2["dz"]==layer].shape[0])) for layer in range(4)]
    df2['inflection'] = df2.apply(lambda x: next(list_inflection[x.dz]), axis=1)
    df2['inflection_x'] = df2.apply(lambda x: f_inflection_x(x), axis=1)
    df2['inflection_y'] = df2.apply(lambda x: f_inflection_y(x), axis=1)

    return df2

def wiring_rect_above(dist: float, df: pd.DataFrame) -> pd.DataFrame:
    def f_inflection_x(x):
        return list([round(x.sx, 4), round(x.sx, 4), round(x.lx, 4), round(x.lx, 4)])

    def f_inflection_y(x):
        return list([round(x.sy, 4), round(x.inflection, 4), round(x.inflection, 4), round(x.ly, 4)])

    df4 = df.copy()
    df4 = df4[(df4["sy"]!=0) & (df4["ly"]!=0)]

    list_inflection = [(100 - (i * dist + interface_length) for i in range(df4[df4["dz"]==layer].shape[0])) for layer in range(4)]
    df4['inflection'] = df4.apply(lambda x: next(list_inflection[x.dz]), axis=1)
    df4['inflection_x'] = df4.apply(lambda x: f_inflection_x(x), axis=1)
    df4['inflection_y'] = df4.apply(lambda x: f_inflection_y(x), axis=1)

    return df4

def wiring_rect_below_above(dist: float, df: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    def f_inflection_x(x):
        return list([round(x.sx, 4), round(x.sx, 4), round(x.lx, 4), round(x.lx, 4)])

    def f_inflection_y(x):
        return list([round(x.sy, 4), round(x.inflection, 4), round(x.inflection, 4), round(x.ly, 4)])

    df3 = df.copy()
    df3 = df3[(df3["sy"]==0) & (df3["ly"]!=0)]

    list_inflection = [((i + df2[df2["dz"]==layer].shape[0]) * dist + interface_length for i in range(df3[df3["dz"]==layer].shape[0])) for layer in range(4)]
    df3['inflection'] = df3.apply(lambda x: next(list_inflection[x.dz]), axis=1)
    df3['inflection_x'] = df3.apply(lambda x: f_inflection_x(x), axis=1)
    df3['inflection_y'] = df3.apply(lambda x: f_inflection_y(x), axis=1)

    return df3

def wiring_rect_above_below(dist: float, df: pd.DataFrame, df4: pd.DataFrame) -> pd.DataFrame:
    def f_inflection_x(x):
        return list([round(x.sx, 4), round(x.sx, 4), round(x.lx, 4), round(x.lx, 4)])

    def f_inflection_y(x):
        return list([round(x.sy, 4), round(x.inflection, 4), round(x.inflection, 4), round(x.ly, 4)])

    df5 = df.copy()
    df5 = df5[(df5["sy"]!=0) & (df5["ly"]==0)]

    list_inflection = [(100 - (i + df4[df4["dz"]==layer].shape[0]) * dist - interface_length for i in range(df5[df5["dz"]==layer].shape[0])) for layer in range(4)]
    df5['inflection'] = df5.apply(lambda x: next(list_inflection[x.dz]), axis=1)
    df5['inflection_x'] = df5.apply(lambda x: f_inflection_x(x), axis=1)
    df5['inflection_y'] = df5.apply(lambda x: f_inflection_y(x), axis=1)

    return df5

def plotter_rect(df: pd.DataFrame, line_width: float, dist: float, save_folder: str = './results/') -> pd.DataFrame:
    df2 = wiring_rect_below(dist, df)
    # df2.to_excel(save_folder + "fiberBoard826data.xlsx")
    df3 = wiring_rect_below_above(dist, df, df2)
    df4 = wiring_rect_above(dist, df)
    df5 = wiring_rect_above_below(dist, df, df4)
    df = pd.concat([df2, df3, df4, df5], axis=0)
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

    fig = plt.figure()
    ax = plt.gca()
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    for i in range(df3.shape[0]):
        x_list = df3['inflection_x'].tolist()[i]
        y_list = df3['inflection_y'].tolist()[i]
        ax.plot(x_list, y_list, color='y', linewidth=line_width, alpha=0.8)
    fig.savefig(save_folder + 'fiberBoard826_below_above.pdf', dpi=3000, format='pdf')

    fig = plt.figure()
    ax = plt.gca()
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    for i in range(df4.shape[0]):
        x_list = df4['inflection_x'].tolist()[i]
        y_list = df4['inflection_y'].tolist()[i]
        ax.plot(x_list, y_list, color='b', linewidth=line_width, alpha=0.8)
    fig.savefig(save_folder + 'fiberBoard826_above.pdf', dpi=3000, format='pdf')

    fig = plt.figure()
    ax = plt.gca()
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    for i in range(df5.shape[0]):
        x_list = df5['inflection_x'].tolist()[i]
        y_list = df5['inflection_y'].tolist()[i]
        ax.plot(x_list, y_list, color='g', linewidth=line_width, alpha=0.8)
    fig.savefig(save_folder + 'fiberBoard826_above_below.pdf', dpi=3000, format='pdf')

    fig = plt.figure()
    ax = plt.gca()
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    for i in range(df.shape[0]):
        x_list = df['inflection_x'].tolist()[i]
        y_list = df['inflection_y'].tolist()[i]
        ax.plot(x_list, y_list, color='g', linewidth=line_width, alpha=0.8)
    fig.savefig(save_folder + 'fiberBoard826_rect.pdf', dpi=3000, format='pdf')

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