
import customtkinter as ctk
import matplotlib.pyplot as plt
import copy
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk) 


#Importy z moich plikow
import random_points_generator as rpg
import WezlzAlgorithm as wezlz
import GrahamAlgorithm as graham
import MinimalBoundingRectangleAlgorithm as mbr
from bitalg.visualizer.main import Visualizer


#Zmienna przechowująca punkty na wykresie
points = []

#Fuknkcja pokazuje przekazane jako argument
#punkty z wykorzystaniem matplotlib
def show_points():

    vis = Visualizer()
    vis.add_point(points)

    fig = vis.get_fig()
    canvas = FigureCanvasTkAgg(fig, master = right_frame)   
    canvas.draw() 
    canvas.get_tk_widget().place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

def show_wezlz(circle):

    vis = Visualizer()
    vis.add_point(points)
    vis.add_circle((circle.S[0], circle.S[1], circle.r), color='green')
    
    fig = vis.get_fig()
    canvas = FigureCanvasTkAgg(fig, master = right_frame)   
    canvas.draw() 
    canvas.get_tk_widget().place(relx=0.5, rely=0.5, anchor=ctk.CENTER) 

def show_graham(hull_points):

    vis = Visualizer()
    vis.add_point(points)
    for i in range(1, len(hull_points)):
        vis.add_line_segment( (hull_points[i - 1], hull_points[i]) )
    vis.add_line_segment( (hull_points[-1], hull_points[0]) )

    fig = vis.get_fig()
    canvas = FigureCanvasTkAgg(fig, master = right_frame)   
    canvas.draw() 
    canvas.get_tk_widget().place(relx=0.5, rely=0.5, anchor=ctk.CENTER) 

def show_mbr(mbr_points):

    vis = Visualizer()
    vis.add_point(points)

    ptsSegments = []
    for i in range(1, len(mbr_points)):
        ptsSegments.append( (mbr_points[i - 1], mbr_points[i]) )
    ptsSegments.append( (mbr_points[-1], mbr_points[0]) )

    vis.add_line_segment(ptsSegments,  color = 'red')

    fig = vis.get_fig()
    canvas = FigureCanvasTkAgg(fig, master = right_frame)   
    canvas.draw() 
    canvas.get_tk_widget().place(relx=0.5, rely=0.5, anchor=ctk.CENTER) 

def show_combo(circle, hull_points, mbr_area_points, mbr_perimeter_points):

    vis = Visualizer()
    vis.add_point(points)

    vis.add_circle((circle.S[0], circle.S[1], circle.r), color='green')

    for i in range(1, len(hull_points)):
        vis.add_line_segment( (hull_points[i - 1], hull_points[i]), color = 'purple' )
    vis.add_line_segment( (hull_points[-1], hull_points[0]), color = 'purple' )

    ptsSegmentsArea = []
    for i in range(1, len(mbr_area_points)):
        ptsSegmentsArea.append( (mbr_area_points[i - 1], mbr_area_points[i]) )
    ptsSegmentsArea.append( (mbr_area_points[-1], mbr_area_points[0]) )

    vis.add_line_segment(ptsSegmentsArea,  color = 'red')

    ptsSegmentsPerimiter = []
    for i in range(1, len(mbr_perimeter_points)):
        ptsSegmentsPerimiter.append( (mbr_perimeter_points[i - 1], mbr_perimeter_points[i]) )
    ptsSegmentsPerimiter.append( (mbr_perimeter_points[-1], mbr_perimeter_points[0]) )

    vis.add_line_segment(ptsSegmentsPerimiter,  color = 'black')

    fig = vis.get_fig()
    canvas = FigureCanvasTkAgg(fig, master = right_frame)   
    canvas.draw() 
    canvas.get_tk_widget().place(relx=0.5, rely=0.5, anchor=ctk.CENTER) 

def generate():

    global points

    points_type = combo_box.get()
    number_of_points = int(NumOfPoints_sl.get())

    if points_type == "random_uniform":

        points = rpg.generate_uniform_points(n = number_of_points)
        show_points()

    elif points_type == "random_circle":
        points = rpg.generate_circle_points(n = number_of_points)
        for p in points:
            print(p)
        show_points()

    elif points_type == "random_rectangle":

        points = rpg.generate_rectangle_points(n = number_of_points)
        show_points()

    else: 
        raise Exception("Incorrect argument!")
    
  
def apply_algorithm():

    selected_algorithm = algorithm_selection_combo_box.get()

    if selected_algorithm == "Wezlz":

        circle = wezlz.welzl_algorithm(copy.deepcopy(points), list([]), len(points))
        show_wezlz(circle)

    elif selected_algorithm == "Graham":

        hull_points = graham.graham_algorithm(copy.deepcopy(points))
        show_graham(hull_points)

    elif selected_algorithm == "MBR - Area":

        mbr_area_points = mbr.mbr(graham.graham_algorithm(copy.deepcopy(points)), CalculationType="area")
        show_mbr(mbr_area_points)

    elif selected_algorithm == "MBR - Perimiter":

        mbr_perimeter_points = mbr.mbr(graham.graham_algorithm(copy.deepcopy(points)), CalculationType="perimiter")
        show_mbr(mbr_perimeter_points)

    elif selected_algorithm == "Combo":

        circle = wezlz.welzl_algorithm(copy.deepcopy(points), list([]), len(points))
        hull_points = graham.graham_algorithm(copy.deepcopy(points))
        mbr_area_points = mbr.mbr(copy.deepcopy(hull_points), CalculationType="area")
        mbr_perimeter_points = mbr.mbr(copy.deepcopy(hull_points), CalculationType="perimiter")

        show_combo(circle, hull_points, mbr_area_points, mbr_perimeter_points)

    else:
        raise Exception("Incorrect argument!")

def updateTextBox_NumOfPoints(value):

    NumOfPoints_tb.configure(text = (str(int(value))))

window = ctk.CTk()

window.resizable(False, False) 
window.title('Minimum bounding circle') 
window.geometry("1200x600") 

ctk.set_appearance_mode("dark")

#----------LEFT FRAME----------

left_frame = ctk.CTkFrame(master = window, width=300, height=600, corner_radius = 0, border_color = "gray", border_width = 1) 
left_frame.pack(side = ctk.LEFT) 

text_label = ctk.CTkLabel(master = left_frame, height = 20, width = 298, text = "Select a set of points", text_color = "white", font = ("Arial", 10))
text_label.place(x = 1, y = 20)

combo_values = ["random_uniform", "random_circle", "random_rectangle"]
combo_box = ctk.CTkComboBox(master = left_frame, height = 20, width = 280, values = combo_values, corner_radius = 0, state = "readonly")
combo_box.set("random_uniform")
combo_box.place(x = 10, y = 50)

#----------Number of points slider + valueLabel + label----------
NumOfPoints_label = ctk.CTkLabel(master = left_frame, width = 280, height = 20, corner_radius = 0, text = "Set number of points to be generated", text_color = "white", font = ("Arial", 10))
NumOfPoints_label.place(x = 10, y = 80)

NumOfPoints_tb = ctk.CTkLabel(master = left_frame, width = 40, height = 20, corner_radius=0, text  = "50", text_color = "white", font = ("Arial", 10))
NumOfPoints_tb.place(x = 240, y = 100)

NumOfPoints_sl = ctk.CTkSlider(master = left_frame, from_ = 0, to = 100, number_of_steps = 100, height = 20, width = 230, command = updateTextBox_NumOfPoints)
NumOfPoints_sl.set(50)
NumOfPoints_sl.place(x = 10, y = 100)

#----------###############################----------

plot_button = ctk.CTkButton(master = left_frame,  command = generate, height = 20,  width = 280, text = "Generate", corner_radius = 0)
plot_button.place(x = 10, y = 130)

#----------ALGORITHM SELECTION----------

algorithm_selection_label = ctk.CTkLabel(master = left_frame, width = 280, height = 20, corner_radius = 0, text = "Select algorithm")
algorithm_selection_label.place(x = 10, y = 500)

algorithm_selection_combo_values = ["Wezlz", "Graham", "MBR - Perimiter", "MBR - Area", "Combo"]
algorithm_selection_combo_box = ctk.CTkComboBox(master = left_frame, height = 20, width = 280, values = algorithm_selection_combo_values, corner_radius = 0, state = "readonly")
algorithm_selection_combo_box.set("Wezlz")
algorithm_selection_combo_box.place(x = 10, y = 530)


algorithm_selection_button = ctk.CTkButton(master = left_frame,  command = apply_algorithm, height = 20,  width = 280, text = "Apply", corner_radius = 0)
algorithm_selection_button.place(x = 10, y = 565)


#----------#####################----------


#----------RIGHT FRAME----------

right_frame = ctk.CTkFrame(master = window, width=900, height=600, corner_radius = 0) 
right_frame.pack(side=ctk.RIGHT) 


# run the gui 
window.mainloop() 