import tkinter as tk

# CONFIGURATION
WIDTH, HEIGHT = 600, 400
COLORS = ["#FF5555", "#55FF55", "#5555FF"] # Red, Green, Blue

class MultiGraph:
    def __init__(self, root):
        self.root = root
        self.root.title("PlotData")
        
        # 1. Labels to show raw numbers
        self.label_frame = tk.Frame(root)
        self.label_frame.pack()
        self.value_labels = [tk.Label(self.label_frame, text="0.0", fg=COLORS[i], font=("Arial", 14, "bold")) for i in range(3)]
        for lbl in self.value_labels: lbl.pack(side=tk.LEFT, padx=20)

        # 2. Canvas for the graph
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#1e1e1e")
        self.canvas.pack()
        
        # Store data for 3 separate lines
        self.data_history = [[], [], []] 
        self.max_points = 60


    def update(self, data):
        num_inputs = len(data)
        while len(self.data_history) < num_inputs:
            self.data_history.append([])
            
        # Synchronize Labels (Optional but helpful)
        while len(self.value_labels) < num_inputs:
            new_idx = len(self.value_labels)
            lbl = tk.Label(self.label_frame, text="0.0", font=("Arial", 12))
            lbl.pack(side=tk.LEFT, padx=10)
            self.value_labels.append(lbl)

        # Update the data
        for i in range(num_inputs):
            val = data[i]
            self.data_history[i].append(val)
            
            # Keep history length in check
            if len(self.data_history[i]) > self.max_points:
                self.data_history[i].pop(0)
            
            # Update label text
            self.value_labels[i].config(text=f"V{i}: {val:.2f}")

        # 5. Redraw all active lines
        self.draw_graphs()
        

    def draw_graphs(self):
        self.canvas.delete("all")
        
        # Generate some colors in case we have more than 3 lines
        dynamic_colors = ["#FF5555", "#55FF55", "#5555FF", "#FFFF55", "#FF55FF", "#55FFFF"]

        
        for ch in range(len(self.data_history)):
            if len(self.data_history[ch]) < 2: 
                continue
            
            points = []
            color = dynamic_colors[ch % len(dynamic_colors)]
            
            for i, val in enumerate(self.data_history[ch]):
                x = (i / (self.max_points - 1)) * WIDTH
                y = HEIGHT - ((val) * (HEIGHT / 127)) 
                points.extend([x, y])
            
            self.canvas.create_line(points, fill=color, width=2)
        
        self.root.update_idletasks()
        self.root.update()
