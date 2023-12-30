for i in range(1, len(hull_points)):
        vis.add_line_segment( (hull_points[i - 1], hull_points[i]) )
    vis.add_line_segment( (hull_points[-1], hull_points[0]) )