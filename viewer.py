
import customtkinter as ctk
import matplotlib.pyplot as plt
import copy
import time
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk) 
from PIL import Image


#Importy z moich plikow
from random_points_generator import Random
from smallestcircle import Welzl
from convexhull import Graham
from mbr import Mbr
from geometry import Rectangle, PointSet
from bitalg.visualizer.main import Visualizer


#Zmienna przechowująca punkty na wykresie
points = []
vis_img = None
vis_gif = None
display_type = "png"
current_job = None
gif_interval = 100

#Fuknkcja pokazuje przekazane jako argument
#punkty z wykorzystaniem matplotlib
def show_points():

    vis = Visualizer()
    vis.add_point(points)

    clearPlot()

    fig, ax = vis.get_fig()
    canvas = FigureCanvasTkAgg(fig, master = right_frame)   
    canvas.draw() 
    canvas.get_tk_widget().place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

def wezlz_vis_img(circle):

    vis = Visualizer()
    vis.add_point(points)
    vis.add_circle((circle.S[0], circle.S[1], circle.r), color='purple')
    
    return vis 

def graham_vis_img(hull_points):

    vis = Visualizer()
    vis.add_point(points)
    vis.add_line_segment(PointSet.getEdges(hull_points), color = 'green')

    return vis

def mbr_vis_img(mbr_rectangle):

    vis = Visualizer()

    vis.add_point(points)
    vis.add_line_segment(mbr_rectangle.getEdges(),  color = 'red')

    return vis

def combo_vis_img(circle, hull_points, mbr_area_points, mbr_perimeter_points):

    vis = Visualizer()
    vis.add_point(points)

    vis.add_circle((circle.S[0], circle.S[1], circle.r), color='purple')

    vis.add_line_segment(PointSet.getEdges(hull_points), color = 'green')

    vis.add_line_segment(mbr_area_points.getEdges(), color = 'orange')

    vis.add_line_segment(mbr_perimeter_points.getEdges(), color = 'black')

    return vis


def show_image():

    global current_job
    
    if current_job != None:
        window.after_cancel(current_job)
        current_job = None

    clearPlot()

    if display_type == "png":
        
        if vis_img == None:
            return

        fig, ax = vis_img.get_fig()
        ax.set_xlim(-150, 150)
        ax.set_ylim(-150, 150)

        canvas = FigureCanvasTkAgg(fig, master = right_frame)   
        canvas.draw() 
        canvas.get_tk_widget().place(relx=0.5, rely=0.5, anchor=ctk.CENTER) 

    elif display_type == "gif":
        
        if vis_gif == None:
            return

        def update(idx):

            if idx >= openImage.n_frames:
                idx = 0

            openImage.seek(idx)
            gifDriver.configure(light_image = openImage)
            gif_Label.configure(image = gifDriver)
            global current_job
            current_job = window.after(int(gif_interval), update, idx + 1)

        gifImage = vis_gif.save_gif(filename="anim")
        openImage = Image.open(gifImage)
        openImage.seek(0)
        gifDriver = ctk.CTkImage(light_image=openImage, size=(640, 480))
        gif_Label = ctk.CTkLabel(right_frame, image=gifDriver, text = "")
        gif_Label.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        update(1)
        
def clearPlot():
    plt.clf()
    plt.cla()
    plt.close()

def getFigure(n = 10, xLimit = (0, 100), yLimit = (0, 100)):

    vertices = []
    
    def on_click(event):
        
        if event.inaxes:

            plt.plot(event.xdata, event.ydata, 'o')

            vertices.append((event.xdata, event.ydata))
            plt.title(str(n - len(vertices)) +  ' points left') 
            plt.show()

            if(len(vertices) >= n):
                plt.close()

    clearPlot()

    fig, ax = plt.subplots()

    plt.setp(ax, xlim=xLimit, ylim=yLimit)
    plt.connect('button_press_event', on_click)
    plt.title(str(n) +  ' points left') 
    plt.show()    
    return vertices

def generate():

    global points

    points_type = combo_box.get()
    number_of_points = int(NumOfPoints_sl.get())

    if points_type == "random_uniform":

        points = Random.generate_uniform_points(n = number_of_points)
        show_points()

    elif points_type == "random_circle":
        points = Random.generate_circle_points(n = number_of_points)
        show_points()

    elif points_type == "random_rectangle":

        points = Random.generate_rectangle_points(n = number_of_points)
        show_points()

    elif points_type == "custom":

        points = getFigure(n = number_of_points)
        show_points()

    else: 
        raise Exception("Incorrect argument!")
    
  
def apply_algorithm():

    global vis_img
    global vis_gif

    vis_img = None
    vis_gif = None

    selected_algorithm = algorithm_selection_combo_box.get()

    if selected_algorithm == "Wezlz":
        
        #----------img----------

        start = time.time()
        welzl_points = Welzl.welzl_algorithm(copy.deepcopy(points))
        stop = time.time()

        #print("Welzl: ", stop - start)
        algorithm_runtime_label.configure( text = str( round(stop - start, 5) ) )

        vis_img = wezlz_vis_img(welzl_points)

        #----------gif----------

        vis_gif = Visualizer()
        vis_gif.add_point(points)


        circle = Welzl.welzl_algorithm_draw(copy.deepcopy(points), vis_gif)
        vis_gif.add_circle((circle.S[0], circle.S[1], circle.r), color='green')

        show_image()

    elif selected_algorithm == "Graham":

        #----------img----------

        start = time.time()
        hull_points = Graham.graham_algorithm(copy.deepcopy(points))
        stop = time.time()

        #print("Graham: ", stop - start)
        algorithm_runtime_label.configure( text = str(round(stop - start, 5)) )

        vis_img = graham_vis_img(hull_points)

        #----------gif----------

        hull_points, vis_gif = Graham.graham_algorithm_draw(copy.deepcopy(points))

        show_image()

    elif selected_algorithm == "MBR - Area":
        
        #----------img----------

        start = time.time()
        mbr_area_rectangle, area = Mbr.smallest_rectangle(copy.deepcopy(points), Mbr.compare_area)
        stop = time.time()

        algorithm_runtime_label.configure( text = str(round(stop - start, 5)) )

        vis_img = mbr_vis_img(mbr_area_rectangle)

        #----------gif----------

        vis_gif = Mbr.smallest_rectangle_draw(copy.deepcopy(points), Mbr.compare_area)

        show_image()

    elif selected_algorithm == "MBR - Perimiter":

        #----------img----------

        start = time.time()
        mbr_perimeter_rectangle, perimeter = Mbr.smallest_rectangle(copy.deepcopy(points), Mbr.compare_perimeter)
        stop = time.time()

        algorithm_runtime_label.configure( text = str(round(stop - start, 5)) )

        vis_img = mbr_vis_img(mbr_perimeter_rectangle)

        #----------gif----------

        vis_gif = Mbr.smallest_rectangle_draw(copy.deepcopy(points), Mbr.compare_perimeter)

        show_image()

    elif selected_algorithm == "Combo":

        #----------img----------

        circle = Welzl.welzl_algorithm(copy.deepcopy(points))
        hull_points = Graham.graham_algorithm(copy.deepcopy(points))
        mbr_area_points, area = Mbr.smallest_rectangle(copy.deepcopy(points), Mbr.compare_area)
        mbr_perimeter_points, perimeter = Mbr.smallest_rectangle(copy.deepcopy(points), Mbr.compare_perimeter)

        vis_img = combo_vis_img(circle, hull_points, mbr_area_points, mbr_perimeter_points)

        algorithm_runtime_label.configure( text = "-" )
        
        #----------gif----------

        vis_gif = None

        show_image()

    else:
        raise Exception("Incorrect argument!")

def updateTextBox_NumOfPoints(value):

    NumOfPoints_tb.configure(text = (str(int(value))))

def segmented_button_callback(value):

    global display_type
    display_type = value
    show_image()

def update_interval(value):
    global gif_interval
    gif_interval = int(value)

    interval_selection_tb.configure(text = str(int(value)))

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

combo_values = ["random_uniform", "random_circle", "random_rectangle", "custom"]
combo_box = ctk.CTkComboBox(master = left_frame, height = 20, width = 280, values = combo_values, corner_radius = 0, state = "readonly")
combo_box.set("random_uniform")
combo_box.place(x = 10, y = 50) 

#----------Number of points slider + valueLabel + label----------
NumOfPoints_label = ctk.CTkLabel(master = left_frame, width = 280, height = 20, corner_radius = 0, text = "Set number of points to be generated", text_color = "white", font = ("Arial", 10))
NumOfPoints_label.place(x = 10, y = 80)

NumOfPoints_tb = ctk.CTkLabel(master = left_frame, width = 40, height = 20, corner_radius=0, text  = "50", text_color = "white", font = ("Arial", 10))
NumOfPoints_tb.place(x = 240, y = 100)

NumOfPoints_sl = ctk.CTkSlider(master = left_frame, from_ = 0, to = 1_000, number_of_steps = 1_000, height = 20, width = 230, command = updateTextBox_NumOfPoints)
NumOfPoints_sl.set(50)
NumOfPoints_sl.place(x = 10, y = 100)

plot_button = ctk.CTkButton(master = left_frame,  command = generate, height = 20,  width = 280, text = "Generate", corner_radius = 0)
plot_button.place(x = 10, y = 130)

#----------ALGORITHM SELECTION----------

algorithm_selection_label = ctk.CTkLabel(master = left_frame, width = 280, height = 20, corner_radius = 0, text = "Select algorithm")
algorithm_selection_label.place(x = 10, y = 515)

algorithm_selection_combo_values = ["Wezlz", "Graham", "MBR - Perimiter", "MBR - Area", "Combo"]
algorithm_selection_combo_box = ctk.CTkComboBox(master = left_frame, height = 20, width = 280, values = algorithm_selection_combo_values, corner_radius = 0, state = "readonly")
algorithm_selection_combo_box.set("Wezlz")
algorithm_selection_combo_box.place(x = 10, y = 540)


algorithm_selection_button = ctk.CTkButton(master = left_frame,  command = apply_algorithm, height = 20,  width = 280, text = "Apply", corner_radius = 0)
algorithm_selection_button.place(x = 10, y = 570)

#----------RIGHT FRAME----------

right_frame = ctk.CTkFrame(master = window, width=900, height=600, corner_radius = 0) 
right_frame.pack(side=ctk.RIGHT) 

#----------Display selection----------

segemented_button = ctk.CTkSegmentedButton(master = right_frame, values=["png", "gif"], command=segmented_button_callback, corner_radius = 0, height = 30 ,width = 400, dynamic_resizing = False)
segemented_button.set("png")
segemented_button.place(x = 250, y = 560)

'''#----------Picture/Gif save------

def save_file():

    folder_selected = ctk.filedialog.askdirectory()
    print(folder_selected)

folder_selected = []

image_save_button = ctk.CTkButton(master = right_frame,  command = save_file, height = 30,  width = 50, text = "Save", corner_radius = 0)
image_save_button.place(x = 840, y = 10)

'''

#----------CHOOSE INTERVAL----------

interval_selection_label = ctk.CTkLabel(master = right_frame, width = 280, height = 20, corner_radius = 0, text = "Select gif interval")
interval_selection_label.place(x = 310, y = 10)

interval_selection_slider = ctk.CTkSlider(master = right_frame, from_ = 1, to = 1000, number_of_steps = 1000, height = 20, width = 230, command = update_interval)
interval_selection_slider.set(100)
interval_selection_slider.place(x = 335, y = 30)

interval_selection_tb = ctk.CTkLabel(master = right_frame, width = 40, height = 20, corner_radius=0, text  = "100", text_color = "white", font = ("Arial", 10))
interval_selection_tb.place(x = 550, y = 30)

#----------ALGORITHM RUNTIME----------

algorithm_runtime_name_label = ctk.CTkLabel(master = right_frame, width = 100, height = 20, corner_radius = 0, text = "Algorithm runtime")
algorithm_runtime_name_label.place(x = 20, y = 566)
algorithm_runtime_label = ctk.CTkLabel(master = right_frame, width = 40, height = 20, corner_radius = 0, text = "-")
algorithm_runtime_label.place(x = 150, y = 566)

# run the gui 
window.mainloop() 
