"""
This file demonstrates how to create synthetic .npz files for testing the NPZ Viewer
"""

import numpy as np
import os

def create_test_npz():
    """Create a test NPZ file with various array types and dimensions"""
    # Create a directory for test data if it doesn't exist
    test_dir = os.path.join(os.path.dirname(__file__), "test_data")
    os.makedirs(test_dir, exist_ok=True)
    
    # 1D array - simple sequence
    array_1d = np.arange(0, 100)
    
    # 2D array - matrix with 5 columns (like a dataset with features)
    array_2d = np.random.normal(size=(1000, 5))
    
    # 2D array - image-like
    array_image = np.random.rand(256, 256)
    
    # 3D array - multiple images or time series of images
    array_3d = np.random.rand(10, 50, 50)
    
    # Structured array with named fields (like a table)
    dt = np.dtype([('x', float), ('y', float), ('z', float), ('value', float)])
    array_structured = np.zeros(100, dtype=dt)
    array_structured['x'] = np.random.rand(100)
    array_structured['y'] = np.random.rand(100)
    array_structured['z'] = np.random.rand(100)
    array_structured['value'] = np.random.normal(size=100)
    
    # Save all arrays to an .npz file
    output_path = os.path.join(test_dir, "test_arrays.npz")
    np.savez(output_path, 
             sequence=array_1d,
             matrix=array_2d,
             image=array_image,
             volume=array_3d,
             table=array_structured)
    
    print(f"Created test NPZ file: {output_path}")
    return output_path

if __name__ == "__main__":
    npz_path = create_test_npz()
    print("\nTo visualize this file, run ReadData.py and open the generated test file.")
