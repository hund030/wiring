import pandas as pd
from problem_graph import create_sim_space
from wiring_rect_826 import plotter_rect, svg2dwgscr_rect
from wiring_bend_826 import plotter_bend, svg2gds_bend
from waveguide_calculator import calc_index, draw_chart
# Demands
# waveguide count
N = 512
# File_Name = "./fiberBoard896.xls"
# File_Name = "./fiberBoard826.xls"
File_Name = "./fiberBoard"+str(N)+".xlsx"
# the width of the fibers, unit: mm
# Line_Width = 0.125
Line_Width = 0.05
# the minimal Distance between parallel lines, unit: mm
# Dist = 0.2
Dist = 0.25
# save folder
Save_Folder = './results/'
# minimal bend radius, unit: mm
Bend_Radius = 4
# bend.svg accuracy, unit: mm
Delta_Arc = 0.001
# mm
height = 150
width = 150

def main() -> None:
    print("******* Start! ********")
    print("******* Routing the waveguides without bend... ********")
    df = create_sim_space(File_Name, Save_Folder, Line_Width, Dist, height=height, N=N)
    df_rect = plotter_rect(df, Line_Width, Dist+Line_Width, Save_Folder, height=height, N=N)
    # svg2dwgscr_rect(df_rect, "fiberBoard"+str(N)+"rect.scr", Save_Folder)
    print("******* Adding bend to the routed plain... ********")
    df_bend = plotter_bend(df_rect, Line_Width, Dist + Line_Width, Bend_Radius, Delta_Arc, Save_Folder, "fiberBoard"+str(N)+"bend")
    # print("******* Converting the data to gds file... ********")
    # svg2gds_bend(df_bend, Line_Width, Bend_Radius, "fiberBoard"+str(N)+"bend.gds", Save_Folder)
    '''
    print("******* Calculating various index for each waveguide... ********")
    loss = pd.read_excel('crossloss.xlsx')
    df_bend = pd.read_excel(Save_Folder + "fiberBoard"+str(N)+"bend.xlsx")
    del df_bend["Unnamed: 0"]
    df_calc = calc_index(df_bend, loss, Line_Width, Bend_Radius, height, width, "fiberBoard"+str(N)+"calc.xlsx")
    print("******* draw graph ********")
    data = pd.read_excel("fiberBoard"+str(N)+"calc.xlsx")
    draw_chart(data, str(N))
    print("******* All done! ********")
    '''

if __name__ == "__main__":
    main()
