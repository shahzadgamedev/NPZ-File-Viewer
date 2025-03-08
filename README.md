# NPZ File Visualizer

A Python tool to explore and visualize NumPy .npz files. This tool helps you understand the structure and contents of .npz files by providing:

- File structure overview
- Array dimension and data type information
- Statistical summaries
- Data preview tables
- Multiple visualization options

## Features

- Interactive GUI for browsing .npz file contents
- Display of array dimensions, types, and basic statistics
- Interactive data table with pagination and CSV export
- Multiple visualization options:
  - Histograms
  - Line plots
  - Heatmaps
  - Scatter plots with customizable X/Y dimensions
- Support for large arrays with automatic sampling
![image](https://github.com/user-attachments/assets/f7e82a24-d6df-4c52-8434-666caf559b9d)
## Requirements

- Python 3.6+
- NumPy
- Matplotlib
- tkinter (usually included with Python)

## Usage

1. Run the script: `python ReadData.py`
2. Click "Open NPZ File" to select your .npz file
3. Select an array from the list to see its information and data preview
4. Click "View Data Table" to open an interactive table view of the array
5. Choose a visualization type and click "Plot" to visualize the data

### Using the Data Table View

The data table provides a paginated view of your array data:
- Navigate between pages using the pagination controls
- Export the entire array to a CSV file for further analysis
- For large arrays, the data is automatically paginated (50 rows per page)
![image](https://github.com/user-attachments/assets/a0511301-c465-4cb2-a754-071da0973224)

### Using the Dimension Selector

When using scatter plots, you can select which dimensions to plot on the X and Y axes:

1. Select "scatter" from the Plot Type dropdown
2. Use the X and Y dropdowns to select dimensions
3. For 2D arrays, the numbers correspond to the column indices
4. For 1D arrays, you can choose between "index" and "value"

![image](https://github.com/user-attachments/assets/dbb51ae0-4853-4e44-b715-5e96a72e638c)


## Tips

- For large arrays, the tool will automatically sample data to maintain performance
- Use the table view to examine specific data values
- Export to CSV when you need to work with the data in other applications
- Different visualization types work better for different array dimensions:
  - Histograms: Good for distribution analysis
  - Line plots: Good for 1D arrays or time series
  - Heatmaps: Good for 2D arrays or matrices
  - Scatter plots: Good for showing relationships between values
