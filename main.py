from problem_graph import create_sim_space
from wiring_rect import plotter_rect, svg2dwgscr_rect
from wiring_bend import plotter_bend, svg2gds_bend
# Demands
File_Name = "./fiberBoard896.xls"
# the width of the fibers, unit: mm
# Line_Width = 0.125
Line_Width = 0.01
# the minimal Distance between parallel lines, unit: mm
# Dist = 0.2
Dist = 0.05
# save folder
Save_Folder = './results/'
# minimal bend radius, unit: mm
Bend_Radius = 5.0
# bend.svg accuracy, unit: mm
Delta_Arc = 0.001

def main() -> None:
    df = create_sim_space(File_Name, Save_Folder, Line_Width, Dist)
    df_rect = plotter_rect(df, Line_Width, Dist, Save_Folder)
    svg2dwgscr_rect(df_rect, "fiberBoard896rect.scr", Save_Folder)
    # df_bend = plotter_bend(df_rect, Line_Width, Dist, Bend_Radius, Delta_Arc, Save_Folder)
    # svg2gds_bend(df_bend, Line_Width, Bend_Radius, "fiberBoard896bend.gds", Save_Folder)


if __name__ == "__main__":
    main()
