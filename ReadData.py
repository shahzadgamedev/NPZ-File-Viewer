import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog, ttk
import os
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import sys
import webbrowser
import tempfile


class NPZViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("NPZ File Viewer")
        self.root.geometry("1000x800")
        
        self.npz_data = None
        self.current_array_name = None
        self.current_array = None
        
        self.x_dim = tk.StringVar()
        self.y_dim = tk.StringVar()
        
        self.data_table_window = None  # Add variable to track data table window
        
        self.create_widgets()
    
    def create_widgets(self):
        # Create a menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Create Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="View README", command=self.show_readme)
        
        # Top frame for file selection
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(top_frame, text="Open NPZ File", command=self.load_npz).pack(side=tk.LEFT, padx=5)
        self.file_label = ttk.Label(top_frame, text="No file selected")
        self.file_label.pack(side=tk.LEFT, padx=5)
        
        # Middle frame for array selection and info
        middle_frame = ttk.Frame(self.root)
        middle_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel for array list
        left_panel = ttk.LabelFrame(middle_frame, text="Arrays")
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=5, pady=5)
        
        self.array_listbox = tk.Listbox(left_panel, width=30)
        self.array_listbox.pack(fill=tk.BOTH, expand=True)
        self.array_listbox.bind('<<ListboxSelect>>', self.on_array_select)
        
        # Right panel for array info and visualization
        right_panel = ttk.Frame(middle_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Info frame
        info_frame = ttk.LabelFrame(right_panel, text="Array Information")
        info_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Add button to view full data table
        info_controls = ttk.Frame(info_frame)
        info_controls.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(info_controls, text="View Data Table", command=self.show_data_table).pack(side=tk.RIGHT)
        
        self.info_text = tk.Text(info_frame, height=8, wrap=tk.WORD)
        self.info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Visualization frame
        viz_frame = ttk.LabelFrame(right_panel, text="Visualization")
        viz_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        viz_controls = ttk.Frame(viz_frame)
        viz_controls.pack(fill=tk.X, padx=5, pady=5)
        
        # Plot type selection
        plot_type_frame = ttk.Frame(viz_controls)
        plot_type_frame.pack(side=tk.LEFT, padx=5, pady=5)
        
        ttk.Label(plot_type_frame, text="Plot Type:").pack(side=tk.LEFT, padx=5)
        
        self.plot_type = tk.StringVar(value="histogram")
        plot_types = ["histogram", "line", "heatmap", "scatter"]
        plot_combo = ttk.Combobox(plot_type_frame, textvariable=self.plot_type, values=plot_types, width=10)
        plot_combo.pack(side=tk.LEFT, padx=5)
        plot_combo.bind("<<ComboboxSelected>>", self.on_plot_type_change)
        
        # Make dimension selection controls always visible in their own frame
        dim_container = ttk.LabelFrame(viz_controls, text="Dimensions")
        dim_container.pack(side=tk.LEFT, padx=10, fill=tk.X)
        
        self.dim_frame = ttk.Frame(dim_container)
        self.dim_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(self.dim_frame, text="X:").pack(side=tk.LEFT)
        self.x_combo = ttk.Combobox(self.dim_frame, textvariable=self.x_dim, width=8)
        self.x_combo.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(self.dim_frame, text="Y:").pack(side=tk.LEFT)
        self.y_combo = ttk.Combobox(self.dim_frame, textvariable=self.y_dim, width=8)
        self.y_combo.pack(side=tk.LEFT, padx=5)
        
        # Initialize with some default values
        self.x_dim.set('0')
        self.y_dim.set('1')
        
        # Button should be after all the controls
        ttk.Button(viz_controls, text="Plot", command=self.plot_data).pack(side=tk.LEFT, padx=10)
        
        # Canvas for matplotlib - Fix the initialization order
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.canvas_frame = ttk.Frame(viz_frame)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.canvas_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Create toolbar frame after canvas is initialized
        toolbar_frame = ttk.Frame(viz_frame)
        toolbar_frame.pack(fill=tk.X)
        self.toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        
    def load_npz(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("NPZ files", "*.npz"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
            
        try:
            self.npz_data = np.load(file_path)
            self.file_label.config(text=os.path.basename(file_path))
            
            # Update array listbox
            self.array_listbox.delete(0, tk.END)
            for key in self.npz_data.files:
                self.array_listbox.insert(tk.END, key)
                
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(tk.END, f"File: {file_path}\n")
            self.info_text.insert(tk.END, f"Contains {len(self.npz_data.files)} arrays\n\n")
            self.info_text.insert(tk.END, "Select an array to view details")
            
            # Clear figure
            self.fig.clear()
            self.canvas.draw()
            
        except Exception as e:
            self.file_label.config(text=f"Error: {str(e)}")
    
    def on_array_select(self, event):
        if not self.npz_data:
            return
        
        selection = self.array_listbox.curselection()
        if not selection:
            return
            
        self.current_array_name = self.npz_data.files[selection[0]]
        self.current_array = self.npz_data[self.current_array_name]
        
        # Display array information
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, f"Array: {self.current_array_name}\n")
        self.info_text.insert(tk.END, f"Shape: {self.current_array.shape}\n")
        self.info_text.insert(tk.END, f"Type: {self.current_array.dtype}\n")
        
        if self.current_array.size > 0:
            self.info_text.insert(tk.END, f"Min: {self.current_array.min()}\n")
            self.info_text.insert(tk.END, f"Max: {self.current_array.max()}\n")
            if self.current_array.size > 1:
                self.info_text.insert(tk.END, f"Mean: {self.current_array.mean()}\n")
                self.info_text.insert(tk.END, f"Std Dev: {self.current_array.std()}\n")
        
        # Add a better data preview with tabular format
        self.info_text.insert(tk.END, "\nData Preview (First 10 rows):\n")
        
        # Format the preview based on array dimensions
        data = self.current_array
        
        if data.ndim == 1:
            # For 1D arrays, show index and value
            preview = "Index | Value\n"
            preview += "-" * 30 + "\n"
            for i in range(min(10, data.size)):
                preview += f"{i:5d} | {data[i]}\n"
                
        elif data.ndim == 2:
            # For 2D arrays, show row indices and columns
            max_cols = min(10, data.shape[1])  # Show at most 10 columns
            preview = "Row |"
            for col in range(max_cols):
                preview += f" Col{col} |"
            preview += "\n" + "-" * (8 * max_cols + 6) + "\n"
            
            for row in range(min(10, data.shape[0])):
                preview += f"{row:3d} |"
                for col in range(max_cols):
                    val = data[row, col]
                    # Format the value to keep table tidy
                    if isinstance(val, (int, np.integer)):
                        val_str = f"{val:5d}"
                    else:
                        val_str = f"{val:.4f}"[:6]
                    preview += f" {val_str:>5} |"
                preview += "\n"
                
        else:
            # For higher dimensional arrays, flatten first 100 elements and show
            preview = "Flattened view:\n"
            preview += "-" * 30 + "\n"
            flat_data = data.flatten()
            for i in range(min(10, flat_data.size)):
                preview += f"[{i:3d}]: {flat_data[i]}\n"
        
        self.info_text.insert(tk.END, preview)
        
        # If the array is large, add a note
        if (data.ndim == 1 and data.size > 10) or \
           (data.ndim == 2 and (data.shape[0] > 10 or data.shape[1] > 10)) or \
           (data.ndim > 2):
            self.info_text.insert(tk.END, "\n(Showing truncated preview of larger data)")
        
        # After setting current_array, update dimension options if scatter is selected
        if self.plot_type.get() == "scatter":
            self.update_dimension_options()
    
    def on_plot_type_change(self, event=None):
        """Show/hide dimension controls based on plot type"""
        if self.plot_type.get() == "scatter" and self.current_array is not None:
            self.update_dimension_options()
            self.dim_frame.pack(side=tk.LEFT, padx=5, fill=tk.X)
        else:
            self.dim_frame.pack_forget()
    
    def update_dimension_options(self):
        """Update the dimension dropdown options based on current array"""
        if self.current_array is None:
            return
            
        # Get the shape of the current array
        shape = self.current_array.shape
        
        if len(shape) == 1:
            # For 1D arrays, offer index and value
            options = ['index', 'value']
            self.x_combo.config(values=options)
            self.y_combo.config(values=options)
            self.x_dim.set('index')
            self.y_dim.set('value')
        elif len(shape) == 2:
            # For 2D arrays, offer columns/dimensions
            if shape[1] <= 20:  # Reasonable number of columns
                options = list(range(shape[1]))
                self.x_combo.config(values=options)
                self.y_combo.config(values=options)
                
                # Set defaults to first two columns if available
                self.x_dim.set(0 if len(options) > 0 else 'index')
                self.y_dim.set(1 if len(options) > 1 else 0 if len(options) > 0 else 'value')
            else:
                # Too many columns, just use numbers as input
                self.x_combo.config(values=[])
                self.y_combo.config(values=[])
                self.x_dim.set('0')
                self.y_dim.set('1')
        else:
            # For higher dimensional arrays
            options = ['flattened']
            self.x_combo.config(values=options)
            self.y_combo.config(values=options)
            self.x_dim.set('flattened')
            self.y_dim.set('flattened')
    
    def plot_data(self):
        if self.current_array is None:
            return
            
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        
        try:
            plot_type = self.plot_type.get()
            
            # Flatten data for certain plot types
            data = self.current_array
            
            if plot_type == "histogram":
                if data.size > 1000000:  # Prevent huge histograms
                    indices = np.random.choice(data.size, size=1000000, replace=False)
                    data_sample = data.flat[indices]
                    ax.hist(data_sample, bins=100)
                    ax.set_title(f"{self.current_array_name} Histogram (Sampled)")
                else:
                    ax.hist(data.flatten(), bins=100)
                    ax.set_title(f"{self.current_array_name} Histogram")
                
            elif plot_type == "line":
                if data.ndim == 1:
                    ax.plot(data)
                    ax.set_title(f"{self.current_array_name} Line Plot")
                elif data.ndim == 2 and (data.shape[0] <= 10 or data.shape[1] <= 10):
                    if data.shape[0] <= data.shape[1]:
                        for i in range(min(10, data.shape[0])):
                            ax.plot(data[i], label=f'Row {i}')
                    else:
                        for i in range(min(10, data.shape[1])):
                            ax.plot(data[:, i], label=f'Column {i}')
                    ax.legend()
                    ax.set_title(f"{self.current_array_name} Line Plot")
                else:
                    ax.plot(data.flatten())
                    ax.set_title(f"{self.current_array_name} Line Plot (Flattened)")
                    
            elif plot_type == "heatmap":
                if data.ndim == 1:
                    data = data.reshape(-1, 1)
                    im = ax.imshow(data, aspect="auto", cmap="viridis")
                elif data.ndim == 2:
                    # Sample if too large
                    if data.shape[0] > 1000 or data.shape[1] > 1000:
                        rows = min(1000, data.shape[0])
                        cols = min(1000, data.shape[1])
                        row_indices = np.linspace(0, data.shape[0]-1, rows, dtype=int)
                        col_indices = np.linspace(0, data.shape[1]-1, cols, dtype=int)
                        data_sample = data[np.ix_(row_indices, col_indices)]
                        im = ax.imshow(data_sample, aspect="auto", cmap="viridis")
                        ax.set_title(f"{self.current_array_name} Heatmap (Sampled)")
                    else:
                        im = ax.imshow(data, aspect="auto", cmap="viridis")
                        ax.set_title(f"{self.current_array_name} Heatmap")
                    self.fig.colorbar(im, ax=ax)
                else:
                    # For higher dimensions, reshape to 2D
                    if data.size > 1000000:
                        flat_data = data.flatten()[:1000000]
                        side = int(np.sqrt(flat_data.size))
                        reshaped_data = flat_data[:side*side].reshape(side, side)
                    else:
                        flat_data = data.flatten()
                        side = int(np.sqrt(flat_data.size))
                        reshaped_data = flat_data[:side*side].reshape(side, side)
                    im = ax.imshow(reshaped_data, aspect="auto", cmap="viridis")
                    self.fig.colorbar(im, ax=ax)
                    ax.set_title(f"{self.current_array_name} Heatmap (Reshaped)")
                    
            elif plot_type == "scatter":
                if data.ndim == 1:
                    # For 1D data, use index vs value or value vs index
                    if self.x_dim.get() == 'index' and self.y_dim.get() == 'value':
                        ax.scatter(range(len(data)), data, alpha=0.5)
                    elif self.x_dim.get() == 'value' and self.y_dim.get() == 'index':
                        ax.scatter(data, range(len(data)), alpha=0.5)
                    else:
                        # Default to index vs value
                        ax.scatter(range(len(data)), data, alpha=0.5)
                    ax.set_title(f"{self.current_array_name} Scatter Plot")
                    
                elif data.ndim == 2:
                    # For 2D data, get the selected dimensions
                    try:
                        x_idx = int(self.x_dim.get())
                        y_idx = int(self.y_dim.get())
                        
                        # Check if indices are valid
                        if x_idx < 0 or x_idx >= data.shape[1] or y_idx < 0 or y_idx >= data.shape[1]:
                            raise ValueError(f"Invalid indices: x={x_idx}, y={y_idx} for shape {data.shape}")
                        
                        # Sample if too many points
                        if data.shape[0] > 10000:
                            indices = np.random.choice(data.shape[0], size=10000, replace=False)
                            ax.scatter(data[indices, x_idx], data[indices, y_idx], alpha=0.5)
                            ax.set_title(f"{self.current_array_name} Scatter (Dim {x_idx} vs {y_idx}, Sampled)")
                        else:
                            ax.scatter(data[:, x_idx], data[:, y_idx], alpha=0.5)
                            ax.set_title(f"{self.current_array_name} Scatter (Dim {x_idx} vs {y_idx})")
                        
                        # Add dimension labels to axes
                        ax.set_xlabel(f"Dimension {x_idx}")
                        ax.set_ylabel(f"Dimension {y_idx}")
                        
                    except ValueError as e:
                        # Handle case where dimensions are not valid integers
                        flat_data = data.flatten()
                        ax.scatter(range(len(flat_data)), flat_data, alpha=0.5)
                        ax.set_title(f"{self.current_array_name} Scatter Plot (Flattened)")
                        print(f"Error with dimensions: {str(e)}")
                        
                else:
                    # For higher dimensions, flatten and create sequence vs. value scatter
                    if data.size > 10000:
                        indices = np.random.choice(data.size, size=10000, replace=False)
                        flat_data = data.flat[indices]
                        ax.scatter(range(len(flat_data)), flat_data, alpha=0.5)
                        ax.set_title(f"{self.current_array_name} Scatter Plot (Sampled)")
                    else:
                        flat_data = data.flatten()
                        ax.scatter(range(len(flat_data)), flat_data, alpha=0.5)
                        ax.set_title(f"{self.current_array_name} Scatter Plot (Flattened)")
            
            self.canvas.draw()
            
        except Exception as e:
            print(f"Error plotting: {str(e)}")
            ax.text(0.5, 0.5, f"Error plotting: {str(e)}", 
                   ha='center', va='center', transform=ax.transAxes)
            self.canvas.draw()
    
    def show_data_table(self):
        """Opens a new window with a full table view of the data"""
        if self.current_array is None:
            return
            
        # Close previous window if open
        if self.data_table_window is not None and self.data_table_window.winfo_exists():
            self.data_table_window.destroy()
            
        # Create new window
        self.data_table_window = tk.Toplevel(self.root)
        self.data_table_window.title(f"Data Table - {self.current_array_name}")
        self.data_table_window.geometry("800x600")
        
        # Create frame for the table
        main_frame = ttk.Frame(self.data_table_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create toolbar with pagination controls and info
        toolbar = ttk.Frame(main_frame)
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        data = self.current_array
        shape_info = f"Shape: {data.shape} | "
        if data.ndim == 1:
            shape_info += f"Elements: {data.size}"
        elif data.ndim == 2:
            shape_info += f"Rows: {data.shape[0]}, Columns: {data.shape[1]}"
        else:
            shape_info += f"Dimensions: {data.ndim}, Total Elements: {data.size}"
            
        ttk.Label(toolbar, text=shape_info).pack(side=tk.LEFT, padx=5)
        
        # Page controls
        page_frame = ttk.Frame(toolbar)
        page_frame.pack(side=tk.RIGHT)
        
        ttk.Label(page_frame, text="Page:").pack(side=tk.LEFT)
        self.page_var = tk.IntVar(value=1)
        
        # Calculate total pages based on the data shape
        if data.ndim == 1:
            rows_per_page = 50
            self.total_pages = max(1, (data.size + rows_per_page - 1) // rows_per_page)
        elif data.ndim == 2:
            rows_per_page = 50
            self.total_pages = max(1, (data.shape[0] + rows_per_page - 1) // rows_per_page)
        else:
            # For higher dims, flatten and paginate
            rows_per_page = 50
            self.total_pages = max(1, (data.size + rows_per_page - 1) // rows_per_page)
            
        # Page controls
        ttk.Button(page_frame, text="<", width=2, 
                  command=lambda: self.change_page(-1)).pack(side=tk.LEFT)
        
        self.page_spinbox = ttk.Spinbox(
            page_frame, 
            from_=1, 
            to=self.total_pages, 
            width=5,
            textvariable=self.page_var,
            command=lambda: self.update_table_view()
        )
        self.page_spinbox.pack(side=tk.LEFT, padx=5)
        self.page_spinbox.bind("<Return>", lambda e: self.update_table_view())
        
        ttk.Label(page_frame, text=f"of {self.total_pages}").pack(side=tk.LEFT)
        
        ttk.Button(page_frame, text=">", width=2,
                  command=lambda: self.change_page(1)).pack(side=tk.LEFT)
        
        # Create the treeview for data display
        columns = []
        if data.ndim == 1:
            columns = ["Index", "Value"]
        elif data.ndim == 2:
            columns = ["Row"] + [f"Col {i}" for i in range(min(20, data.shape[1]))]
        else:
            columns = ["Index", "Value"]  # For flattened view
            
        # Create Treeview with scrollbars
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
            
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        
        # Configure scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Grid layout for treeview and scrollbars
        self.tree.grid(column=0, row=0, sticky='nsew')
        vsb.grid(column=1, row=0, sticky='ns')
        hsb.grid(column=0, row=1, sticky='ew')
        
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)
        
        # Configure columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=80)
            
        # Add "Export to CSV" button
        export_frame = ttk.Frame(main_frame)
        export_frame.pack(fill=tk.X, pady=(10, 0))
        ttk.Button(export_frame, text="Export to CSV", 
                   command=self.export_to_csv).pack(side=tk.RIGHT)
        
        # Populate the table
        self.update_table_view()
        
    def update_table_view(self):
        """Update the table with current page data"""
        if not hasattr(self, 'tree') or self.current_array is None:
            return
            
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Get current page
        page = self.page_var.get()
        if page < 1:
            page = 1
        elif page > self.total_pages:
            page = self.total_pages
            
        self.page_var.set(page)
        
        # Get data for the current page
        data = self.current_array
        rows_per_page = 50
        
        if data.ndim == 1:
            start_idx = (page - 1) * rows_per_page
            end_idx = min(start_idx + rows_per_page, data.size)
            
            for i in range(start_idx, end_idx):
                self.tree.insert("", "end", values=(i, data[i]))
                
        elif data.ndim == 2:
            start_row = (page - 1) * rows_per_page
            end_row = min(start_row + rows_per_page, data.shape[0])
            
            max_cols = min(20, data.shape[1])  # Limit columns display
            
            for row in range(start_row, end_row):
                row_data = [row]
                for col in range(max_cols):
                    row_data.append(data[row, col])
                self.tree.insert("", "end", values=tuple(row_data))
                
        else:
            # Flattened view for higher dimensions
            flat_data = data.flatten()
            start_idx = (page - 1) * rows_per_page
            end_idx = min(start_idx + rows_per_page, flat_data.size)
            
            for i in range(start_idx, end_idx):
                self.tree.insert("", "end", values=(i, flat_data[i]))
    
    def change_page(self, delta):
        """Change the current page by delta amount"""
        new_page = self.page_var.get() + delta
        if 1 <= new_page <= self.total_pages:
            self.page_var.set(new_page)
            self.update_table_view()
            
    def export_to_csv(self):
        """Export the current array to CSV file"""
        if self.current_array is None:
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=f"{self.current_array_name}.csv"
        )
        
        if not file_path:
            return
            
        try:
            data = self.current_array
            
            with open(file_path, "w", newline='') as f:
                # Write header
                if data.ndim == 1:
                    f.write("Index,Value\n")
                    for i in range(data.size):
                        f.write(f"{i},{data[i]}\n")
                        
                elif data.ndim == 2:
                    # Header row
                    header = "Row," + ",".join(f"Col{i}" for i in range(data.shape[1]))
                    f.write(header + "\n")
                    
                    # Data rows
                    for i in range(data.shape[0]):
                        row = f"{i}," + ",".join(str(data[i, j]) for j in range(data.shape[1]))
                        f.write(row + "\n")
                        
                else:
                    # Flattened view for higher dimensions
                    f.write("Index,Value\n")
                    flat_data = data.flatten()
                    for i in range(flat_data.size):
                        f.write(f"{i},{flat_data[i]}\n")
                        
            tk.messagebox.showinfo("Export Complete", f"Data exported to {file_path}")
            
        except Exception as e:
            tk.messagebox.showerror("Export Error", f"Error exporting data: {str(e)}")
    
    def show_readme(self):
        # Get the README path - works with PyInstaller bundled files
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            application_path = sys._MEIPASS
        else:
            # Running as a normal Python script
            application_path = os.path.dirname(os.path.abspath(__file__))
        
        readme_path = os.path.join(application_path, 'README.md')
        
        if os.path.exists(readme_path):
            # Create a temporary HTML file to display the README
            with open(readme_path, 'r') as f:
                content = f.read()
            
            # Simple conversion of markdown to basic HTML
            html_content = f"<html><body><pre>{content}</pre></body></html>"
            
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.html')
            temp_file.write(html_content.encode('utf-8'))
            temp_file.close()
            
            # Open the temporary file in the default web browser
            webbrowser.open('file://' + temp_file.name)
        else:
            tk.messagebox.showerror("Error", "README file not found")


if __name__ == "__main__":
    root = tk.Tk()
    app = NPZViewer(root)
    root.mainloop()
