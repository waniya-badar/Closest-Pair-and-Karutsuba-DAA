import tkinter as tk
from tkinter import filedialog
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Karatsuba implementation with an improved tree-like visualization
def karatsuba(x, y, depth=0):
    if x < 10 or y < 10:
        return x * y
    n = max(len(str(x)), len(str(y)))
    m = n // 2
    high1, low1 = divmod(x, 10**m)
    high2, low2 = divmod(y, 10**m)
    
    # Recursively calculate the three products
    z0 = karatsuba(low1, low2, depth + 1)
    z1 = karatsuba((low1 + high1), (low2 + high2), depth + 1)
    z2 = karatsuba(high1, high2, depth + 1)

    # Improved visualization of recursive steps (text representation)
    tree_text.insert(tk.END, f"{'  ' * depth}Depth {depth}: z2={z2}, z1={z1}, z0={z0}\n")
    tree_text.see(tk.END)

    # Return the result with the corrected formula
    return z2 * (10**(2 * m)) + (z1 - z2 - z0) * (10**m) + z0

# Euclidean distance for Closest Pair
def euclidean_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# Closest Pair with scatter plot and highlighted pair
def closest_pair(points):
    min_dist = float('inf')
    pair = None
    fig, ax = plt.subplots()

    # Scatter plot of points
    x_vals, y_vals = zip(*points)
    ax.scatter(x_vals, y_vals, color='blue', label="Points")

    # Find the closest pair
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            dist = euclidean_distance(points[i], points[j])
            if dist < min_dist:
                min_dist = dist
                pair = (points[i], points[j])

    # Draw a line and circle between the closest pair
    if pair:
        ax.plot(
            [pair[0][0], pair[1][0]],
            [pair[0][1], pair[1][1]],
            color='red',
            linestyle='--',
            linewidth=2,
            label="Closest Pair"
        )
        # Highlight the closest pair points
        ax.scatter(pair[0][0], pair[0][1], color='green', s=100, edgecolor='black', label="Closest Point 1", zorder=5)
        ax.scatter(pair[1][0], pair[1][1], color='green', s=100, edgecolor='black', label="Closest Point 2", zorder=5)
    
    ax.set_title("Closest Pair Visualization")
    ax.legend()

    # Embed the plot in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=result_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

    return min_dist, pair

# File processing function
def process_file():
    global tree_text
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if not file_path:
        return

    with open(file_path, 'r') as file:
        content = file.read().strip()
        lines = content.split('\n')

    # Clear previous content in the result frame
    for widget in result_frame.winfo_children():
        widget.destroy()

    if len(lines) == 2:  # Integer multiplication case
        x, y = map(int, lines)
        # Create Karatsuba frame
        karatsuba_frame = tk.Frame(result_frame, bg="#E5E5E5", bd=2, relief="groove", padx=20, pady=20)
        karatsuba_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        # Create the tree_text widget for Karatsuba
        tree_text = tk.Text(karatsuba_frame, bg="#E5E5E5", fg="#000000", font=("Courier New", 12), wrap="word", height=10)
        tree_text.pack()

        result = karatsuba(x, y)

        # Add Karatsuba result - center-aligned and wrapped
        karatsuba_result_label = tk.Label(
            karatsuba_frame, 
            text=f"Karatsuba Multiplication Result: {result}",
            bg="#E5E5E5",
            fg="#000000",
            font=("Courier New", 14, "bold"),
            pady=10,
            wraplength=650,  # Wrap long lines
            justify="center"  # Center the text
        )
        karatsuba_result_label.pack()

    else:  # Closest pair case
        points = [tuple(map(int, line.split())) for line in lines]
        
        # Create Closest Pair frame
        closest_pair_frame = tk.Frame(result_frame, bg="#E5E5E5", bd=2, relief="groove", padx=20, pady=20)
        closest_pair_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        min_distance, closest_points = closest_pair(points)

        # Add Closest Pair result
        closest_pair_result_label = tk.Label(closest_pair_frame, 
                                             text=f"Closest Pair: {closest_points}, Distance: {min_distance:.2f}", 
                                             bg="#E5E5E5", fg="#000000", font=("Courier New", 14, "bold"), pady=10)
        closest_pair_result_label.pack()

    result_label.config(text="Processing Complete. Results displayed in the respective sections.")

# Tkinter GUI setup
root = tk.Tk()
root.title("Algorithm Runner with Visualization")
root.geometry("800x800")
root.configure(bg="#14213D")

# Header
header_label = tk.Label(root, text="Algorithm Runner", bg="#FCA311", fg="#000000", font=("Verdana", 28, "bold"))
header_label.pack(fill="x", pady=(0, 20))

# Instructions
instruction_frame = tk.Frame(root, bg="#E5E5E5")
instruction_frame.pack(padx=20, pady=10, anchor="center", fill="x")
instruction_label = tk.Label(instruction_frame, text="Upload a text file to process:", bg="#E5E5E5", fg="#000000", font=("Lucida Sans", 14, "bold"))
instruction_label.pack()

# Upload Button
upload_button = tk.Button(root, text="Upload and Process File", command=process_file, bg="#FCA311", fg="#000000", font=("Calibri", 16, "bold"), padx=20, pady=10, bd=0, relief="flat", cursor="hand2")
upload_button.pack(pady=20)

# Result Frame
result_frame = tk.Frame(root, bg="#E5E5E5", bd=2, relief="groove", padx=20, pady=20)
result_frame.pack(padx=20, pady=20, fill="both", expand=True)

# Result Label
result_label = tk.Label(result_frame, text="Awaiting file upload...", bg="#E5E5E5", fg="#000000", font=("Courier New", 16, "normal"), wraplength=650, justify="center")
result_label.pack()

root.mainloop()
