import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from dataclasses import dataclass, field
from typing import List

interface_length = 5

@dataclass
class WGset:
    WGs: List[int] = field(default_factory=list)
    rEnd: List[int] = field(default_factory=list)
    lEnd: List[int] = field(default_factory=list)
    y: float = interface_length

def plotter_rect(df: pd.DataFrame, line_width: float, dist: float, save_folder: str = './results/', height: int = 150, N: int = 256) -> pd.DataFrame:

    yy = [np.round(i * 0.001, 3) for i in range(interface_length * 1000, (height - interface_length) * 1000, int(dist * 1000))]
    WGsets = [[WGset(y=y, rEnd=[-1], lEnd=[100]) for y in yy] for layer in range(4)]

    def ln_calc(lx, ly):
        # TODO: magic number here
        offset = 4 if ly == height else 2
        return max(int(np.round((lx - offset) % 4.5, 3) / dist) - 7, 4)

    def sn_calc(sx, sy):
        pass

    def noCross(lEnd, rEnd, i, WGset, _type='below', lx=0, ly=0, boundary=0):
        #TODO: 6 and 8 are magic numbers here
        if _type == 'below':
            for j in range(1,ln_calc(lx, ly)):
                if i>=j and WGset[i-j].WGs and WGset[i - j].rEnd[-1] < rEnd and WGset[i-j].lEnd[-1] < lEnd:
                    return False
                elif i >= j and len(WGset[i - j].rEnd) > 2 and WGset[i - j].rEnd[-2] < lEnd:
                    return False
            for j in range(1,8):
                if i+j<len(WGset) and WGset[i+j].WGs and WGset[i + j].rEnd[-1] > lEnd:
                    return False
        elif _type == 'above2below':
            for j in range(1, 4):
                if i>=j and WGset[i-j].WGs and WGset[i - j].lEnd[-1] < lEnd:
                    return False
            for j in range(1,6):
                if i+j<len(WGset) and WGset[i+j].WGs and WGset[i + j].rEnd[-1] > lEnd:
                    return False
        elif _type == 'above':
            for j in range(1,ln_calc(lx, ly)):
                if i + j < len(WGset) and WGset[i + j].WGs and WGset[i + j].rEnd[-1] != rEnd:
                    return False
                elif i + j < len(WGset) and len(WGset[i + j].rEnd) > 1 and WGset[i+j].rEnd[-2] > lEnd:
                    return False
            for j in range(1,7):
                if i>=j and WGset[i-j].WGs and WGset[i - j].rEnd[-1] > lEnd:
                    return False
        elif _type == 'below2above':
            for j in range(1,3):
                if i>=j and WGset[i-j].WGs and WGset[i - j].rEnd[-1] > lEnd and WGset[i-j].rEnd[-1] != rEnd:
                    return False
            for j in range(1,ln_calc(lx, ly)):
                if i + j < len(WGset) and WGset[i + j].WGs and WGset[i+j].rEnd[-1] > rEnd:
                    return False
        return True

    def wiring_rect_below(dist: float, df: pd.DataFrame) -> pd.DataFrame:
        def f_inflection_x(x):
            return list([round(x.sx, 4), round(x.sx, 4), round(x.lx, 4), round(x.lx, 4)])

        def f_inflection_y(x):
            return list([round(x.sy, 4), round(x.inflection, 4), round(x.inflection, 4), round(x.ly, 4)])

        df2 = df.copy()
        df2 = df2[(df2["sy"]==0) & (df2["ly"]==0)]
        # df2 = df2.sort_values(by=["index2", "sx"], ascending=[False, True])
        if N == 256:
            list_inflection = [(i * dist + interface_length \
                for i in range(df2[df2["dz"] == layer].shape[0])) for layer in range(4)]
        elif N == 512:
            list_inflection = []
            for layer in range(4):
                i = 0
                indexes = set()
                list_inflection += [[]]
                for row in df2[df2["dz"] == layer].iterrows():
                    if row[1]['index1'] not in indexes:
                        indexes.add(row[1]['index1'])
                    for i, w in enumerate(WGsets[layer]):
                        if row[1]['index2'] >= w.rEnd[-1] and \
                          noCross(row[1]['index2'], row[1]['index1'], i, \
                          lx=row[1]['lx'], ly=row[1]['ly'], WGset=WGsets[layer]):
                            w.WGs.append(row[0])
                            w.rEnd.append(row[1]['index1'])
                            w.lEnd.append(row[1]['index2'])
                            list_inflection[layer] += [w.y]
                            break

        it = [iter(list_inflection[i]) for i in range(4)]
        df2['inflection'] = df2.apply(lambda x: next(it[int(x.dz)]), axis=1)

        sx = []
        for layer in range(4):
            list_inflection = df2[df2["dz"] == layer]['inflection'].tolist()
            index1 = df2[df2["dz"] == layer]['index1'].tolist()
            sx += [df2[df2["dz"] == layer]['sx'].tolist()]
            sx_temp = sx[layer].copy()
            i = 0
            while i < len(list_inflection):
                for j in reversed(range(i)):
                    if index1[i] == index1[j] and list_inflection[i] < list_inflection[j]:
                        sx[layer][i], sx[layer][j] = sx[layer][j], sx[layer][i]
                        list_inflection[i], list_inflection[j] = list_inflection[j], list_inflection[i]
                        i = j
                    else:
                        break
                i += 1
            sx[layer] = [sx_temp[sx[layer].index(sx_temp[i])] for i in range(len(sx[layer]))]
        it = [iter(sx[i]) for i in range(4)]
        df2['sx'] = df2.apply(lambda x: next(it[int(x.dz)]), axis=1)

        df2 = df2.sort_values(by="lx", ascending=True)
        lx = []
        for layer in range(4):
            list_inflection = df2[df2["dz"] == layer]['inflection'].tolist()
            index2 = df2[df2["dz"] == layer]['index2'].tolist()
            lx += [df2[df2["dz"] == layer]['lx'].tolist()]
            lx_temp = lx[layer].copy()
            i = 0
            while i < len(list_inflection):
                for j in reversed(range(i)):
                    if index2[i] == index2[j] and list_inflection[i] > list_inflection[j]:
                        lx[layer][i], lx[layer][j] = lx[layer][j], lx[layer][i]
                        list_inflection[i], list_inflection[j] = list_inflection[j], list_inflection[i]
                        i = j
                    else:
                        break
                i += 1
            lx[layer] = [lx_temp[lx[layer].index(lx_temp[i])] for i in range(len(lx[layer]))]

        # it = [iter(lx[i]) for i in range(4)]
        # df2['inflection'] = df2.apply(lambda x: x.inflection + max(next(it[int(x.dz)])-x.lx, 0), axis=1)
        it = [iter(lx[i]) for i in range(4)]
        df2['lx'] = df2.apply(lambda x: next(it[int(x.dz)]), axis=1)
        
        df2["dx"] = df2.apply(lambda x: np.abs(x.sx - x.lx), axis=1)
        df2['inflection_x'] = df2.apply(lambda x: f_inflection_x(x), axis=1)
        df2['inflection_y'] = df2.apply(lambda x: f_inflection_y(x), axis=1)
        return df2

    def wiring_rect_above(dist: float, df: pd.DataFrame) -> pd.DataFrame:
        def f_inflection_x(x):
            if x.dx == 0:
                return list([x.sx, x.lx])
            else:
                return list([round(x.sx, 4), round(x.sx, 4), round(x.lx, 4), round(x.lx, 4)])

        def f_inflection_y(x):
            if x.dx == 0:
                return list([x.sy, x.ly])
            else:
                return list([round(x.sy, 4), round(x.inflection, 4), round(x.inflection, 4), round(x.ly, 4)])

        df4 = df.copy()
        df4 = df4[(df4["sy"]!=0) & (df4["ly"]!=0)]
        # df4 = df4.sort_values(by=["index2", "sx"], ascending=[False, True])

        if N == 256:
            list_inflection = [(height - (i * dist + interface_length) \
                for i in range(df4[df4["dz"] == layer].shape[0])) for layer in range(4)]
        elif N == 512:
            list_inflection = []
            for layer in range(4):
                i = 0
                indexes = set()
                gap = 0
                list_inflection += [[]]
                for row in df4[df4["dz"] == layer].iterrows():
                    if row[1]['index1'] not in indexes:
                        indexes.add(row[1]['index1'])
                        gap = 1
                    for i, w in reversed(list(enumerate(WGsets[layer]))):
                        if row[1]['index2'] >= w.rEnd[-1] and \
                           noCross(row[1]['index2'], row[1]['index1'], i, \
                           lx = row[1]['lx'], ly = row[1]['ly'], WGset=WGsets[layer], _type='above'):
                            w.WGs.append(row[0])
                            w.rEnd.append(row[1]['index1'])
                            w.lEnd.append(row[1]['index2'])
                            list_inflection[layer] += [w.y]
                            break
        
        it = [iter(list_inflection[i]) for i in range(4)]
        df4['inflection'] = df4.apply(lambda x: next(it[int(x.dz)], height - 1), axis=1)

        sx = []
        for layer in range(4):
            list_inflection = df4[df4["dz"] == layer]['inflection'].tolist()
            index1 = df4[df4["dz"] == layer]['index1'].tolist()
            sx += [df4[df4["dz"] == layer]['sx'].tolist()]
            sx_temp = sx[layer].copy()
            i = 0
            while i < len(list_inflection):
                for j in reversed(range(i)):
                    if index1[i] == index1[j] and list_inflection[i] > list_inflection[j]:
                        sx[layer][i], sx[layer][j] = sx[layer][j], sx[layer][i]
                        list_inflection[i], list_inflection[j] = list_inflection[j], list_inflection[i]
                        i = j
                    else:
                        break
                i += 1
            sx[layer] = [sx_temp[sx[layer].index(sx_temp[i])] for i in range(len(sx[layer]))]
        it = [iter(sx[i]) for i in range(4)]
        df4['sx'] = df4.apply(lambda x: next(it[int(x.dz)]), axis=1)

        df4 = df4.sort_values(by="lx", ascending=True)
        lx = []
        for layer in range(4):
            list_inflection = df4[df4["dz"] == layer]['inflection'].tolist()
            index2 = df4[df4["dz"] == layer]['index2'].tolist()
            lx += [df4[df4["dz"] == layer]['lx'].tolist()]
            lx_temp = lx[layer].copy()
            i = 0
            while i < len(list_inflection):
                for j in reversed(range(i)):
                    if index2[i] == index2[j] and list_inflection[i] < list_inflection[j]:
                        lx[layer][i], lx[layer][j] = lx[layer][j], lx[layer][i]
                        list_inflection[i], list_inflection[j] = list_inflection[j], list_inflection[i]
                        i = j
                    else:
                        break
                i += 1
            lx[layer] = [lx_temp[lx[layer].index(lx_temp[i])] for i in range(len(lx[layer]))]

        # it = [iter(lx[i]) for i in range(4)]
        # df4['inflection'] = df4.apply(lambda x: x.inflection - max(next(it[int(x.dz)])-x.lx, 0), axis=1)
        it = [iter(lx[i]) for i in range(4)]
        df4['lx'] = df4.apply(lambda x: next(it[int(x.dz)]), axis=1)
        df4["dx"] = df4.apply(lambda x: np.abs(x.sx - x.lx), axis=1)
        df4['inflection_x'] = df4.apply(lambda x: f_inflection_x(x), axis=1)
        df4['inflection_y'] = df4.apply(lambda x: f_inflection_y(x), axis=1)

        return df4

    def wiring_rect_below2above(dist: float, df: pd.DataFrame, df4: pd.DataFrame) -> pd.DataFrame:
        def f_inflection_x(x):
            if x.dx == 0:
                return list([x.sx, x.lx])
            else:
                return list([round(x.sx, 4), round(x.sx, 4), round(x.lx, 4), round(x.lx, 4)])

        def f_inflection_y(x):
            if x.dx == 0:
                return list([x.sy, x.ly])
            else:
                return list([round(x.sy, 4), round(x.inflection, 4), round(x.inflection, 4), round(x.ly, 4)])

        df3 = df.copy()
        df3 = df3[(df3["sy"] == 0) & (df3["ly"] != 0)]
        df3 = df3.sort_values(by="sx", ascending=False)
        above_line = min(df4['inflection'])

        list_inflection = []
        for layer in range(4):
            i = 0
            indexes = set()
            gap = 0
            list_inflection += [[]]
            for row in df3[df3["dz"] == layer].iterrows():
                if row[1]['index1'] not in indexes:
                    indexes.add(row[1]['index1'])
                    gap = 1
                for i, w in reversed(list(enumerate(WGsets[layer]))):
                    if w.y >= above_line:
                        continue
                    if row[1]['index2'] >= w.rEnd[-1] and \
                       noCross(row[1]['index2'], row[1]['index1']-32, i, \
                       lx = row[1]['sx'], ly = row[1]['sy'], WGset=WGsets[layer], _type='below2above'):
                    # if not w.WGs and noCross(row[1]['index2']+32, row[1]['index1'], i, WGsets[layer], 'below2above'):
                        w.WGs.append(row[0])
                        w.rEnd.append(row[1]['index1']-32)
                        w.lEnd.append(row[1]['index2'])
                        list_inflection[layer] += [w.y]
                        break

        it = [iter(list_inflection[i]) for i in range(4)]
        df3['inflection'] = df3.apply(lambda x: next(it[int(x.dz)]), axis=1)
        df3['inflection_x'] = df3.apply(lambda x: f_inflection_x(x), axis=1)
        df3['inflection_y'] = df3.apply(lambda x: f_inflection_y(x), axis=1)
        return df3

    def wiring_rect_above2below(dist: float, df: pd.DataFrame, df2: pd.DataFrame, df3: pd.DataFrame) -> pd.DataFrame:
        def f_inflection_x(x):
            if x.dx == 0:
                return list([x.sx, x.lx])
            else:
                return list([round(x.sx, 4), round(x.sx, 4), round(x.lx, 4), round(x.lx, 4)])

        def f_inflection_y(x):
            if x.dx == 0:
                return list([x.sy, x.ly])
            else:
                return list([round(x.sy, 4), round(x.inflection, 4), round(x.inflection, 4), round(x.ly, 4)])

        df5 = df.copy()
        df5 = df5[(df5["sy"] != 0) & (df5["ly"] == 0)]
        df5 = df5.sort_values(by="sx", ascending=False)
        b2a_line = min(df3['inflection'])
        below_line = max(df2['inflection'])
        boundary = yy.index(below_line)

        list_inflection = []
        for layer in range(4):
            i = 0
            indexes = set()
            list_inflection += [[]]
            for row in df5[df5["dz"] == layer].iterrows():
                if row[1]['index1'] not in indexes:
                    indexes.add(row[1]['index1'])
                for i, w in enumerate(WGsets[layer]):
                    if w.y < below_line:
                        continue
                    # TODO:32 is a magic number here
                    if row[1]['index2'] - 32 > w.rEnd[-1] and \
                       noCross(row[1]['index2'] - 32, row[1]['index1'], i, \
                       lx = row[1]['lx'], ly = row[1]['ly'], WGset=WGsets[layer], \
                       _type='above2below'):
                        w.WGs.append(row[0])
                        w.rEnd.append(row[1]['index1'])
                        w.lEnd.append(row[1]['index2']-32)
                        list_inflection[layer] += [w.y]
                        break
    
        it = [iter(list_inflection[i]) for i in range(4)]
        df5['inflection'] = df5.apply(lambda x: next(it[int(x.dz)], height+10), axis=1)
        df5 = df5.sort_values(by="sx", ascending=True)
        sx = []
        for layer in range(4):
            list_inflection = df5[df5["dz"] == layer]['inflection'].tolist()
            index1 = df5[df5["dz"] == layer]['index1'].tolist()
            sx += [df5[df5["dz"] == layer]['sx'].tolist()]
            sx_temp = sx[layer].copy()
            i = 0
            while i < len(list_inflection):
                for j in reversed(range(i)):
                    if index1[i] == index1[j] and list_inflection[i] > list_inflection[j]:
                        sx[layer][i], sx[layer][j] = sx[layer][j], sx[layer][i]
                        list_inflection[i], list_inflection[j] = list_inflection[j], list_inflection[i]
                        i = j
                    else:
                        break
                i += 1
            sx[layer] = [sx_temp[sx[layer].index(sx_temp[i])] for i in range(len(sx[layer]))]

        it = [iter(sx[i]) for i in range(4)]
        df5['sx'] = df5.apply(lambda x: next(it[int(x.dz)]), axis=1)
        df5["dx"] = df5.apply(lambda x: np.abs(x.sx - x.lx), axis=1)
        df5['inflection_x'] = df5.apply(lambda x: f_inflection_x(x), axis=1)
        df5['inflection_y'] = df5.apply(lambda x: f_inflection_y(x), axis=1)
        return df5

    df2 = wiring_rect_below(dist, df)
    df4 = wiring_rect_above(dist, df)
    df3 = wiring_rect_below2above(dist, df, df4)
    df5 = wiring_rect_above2below(dist, df, df2, df3)
    df = pd.concat([df2, df4, df3, df5], axis=0)
    df['ln'] = df.apply(lambda x: ln_calc(x.lx, x.ly), axis=1)
    # df.to_excel(save_folder + "fiberBoard826data.xlsx")

    fig = plt.figure()
    ax = plt.gca()
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    for i in range(df.shape[0]):
        x_list = df['inflection_x'].tolist()[i]
        y_list = df['inflection_y'].tolist()[i]
        ax.plot(x_list, y_list, color='g', linewidth=line_width, alpha=0.8)
    fig.savefig(save_folder + 'fiberBoard256_rect.pdf', dpi=3000, format='pdf')

    df.to_excel(save_folder + "fiberBoard256rect.xlsx")

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