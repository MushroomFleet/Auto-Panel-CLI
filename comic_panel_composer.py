#!/usr/bin/env python3
"""
Comic Panel Composer - CLI tool to composite sequential images into comic book layouts

This tool takes a directory of sequential images and a layout preset JSON file,
then composes the images into comic panels according to the specified layout.
"""

import argparse
import json
import os
import sys
from datetime import datetime
from PIL import Image


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Comic Panel Composer')
    parser.add_argument('image_path', help='Path to directory containing sequential images')
    parser.add_argument('--preset', default='presets/2col_preset.json', 
                       help='Path to layout preset JSON file (default: presets/2col_preset.json)')
    parser.add_argument('--output', default=None, 
                       help='Output directory (default: image_path with timestamp)')
    parser.add_argument('--fit', choices=['contain', 'cover', 'stretch'], default='contain',
                       help='How to fit images: contain (preserve ratio), cover (fill & crop), stretch')
    
    return parser.parse_args()


def load_preset(preset_path):
    """Load and validate the layout preset from a JSON file."""
    try:
        with open(preset_path, 'r') as f:
            preset = json.load(f)
        
        # Validate the preset has the required fields
        required_fields = ['name', 'page', 'layout']
        for field in required_fields:
            if field not in preset:
                raise ValueError(f"Preset is missing required field: {field}")
        
        # Validate page details
        if not all(k in preset['page'] for k in ['width', 'height', 'background_color']):
            raise ValueError("Preset page must specify width, height, and background_color")
        
        # Validate layout
        if 'cells' not in preset['layout']:
            raise ValueError("Preset layout must have a cells array")
        
        return preset
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        print(f"Error loading preset: {e}")
        sys.exit(1)


def get_image_files(image_path):
    """Get all image files from the directory and sort them by name."""
    try:
        # Check if the directory exists
        if not os.path.isdir(image_path):
            raise FileNotFoundError(f"Directory not found: {image_path}")
        
        # Get all image files from directory
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']
        files = [f for f in os.listdir(image_path) if 
                os.path.isfile(os.path.join(image_path, f)) and
                os.path.splitext(f)[1].lower() in image_extensions]
        
        # Sort files by name
        sorted_files = sorted(files)
        print(f"Found {len(sorted_files)} image files")
        return sorted_files
    except Exception as e:
        print(f"Error accessing image directory: {e}")
        sys.exit(1)


def fit_image(img, target_width, target_height, fit_mode='contain'):
    """
    Resize image based on the fit mode
    - contain: fit image entirely while preserving aspect ratio (may leave empty space)
    - cover: fill the entire target area while preserving aspect ratio (may crop image)
    - stretch: stretch the image to fill the target area (may distort image)
    """
    original_width, original_height = img.size
    
    if fit_mode == 'stretch':
        return img.resize((target_width, target_height), Image.LANCZOS)
    
    elif fit_mode == 'contain':
        ratio = min(target_width / original_width, target_height / original_height)
        new_width = int(original_width * ratio)
        new_height = int(original_height * ratio)
        
        # Resize the image
        resized_img = img.resize((new_width, new_height), Image.LANCZOS)
        
        # Create a new image with the target dimensions and paste the resized image in the center
        new_img = Image.new('RGBA', (target_width, target_height), (0, 0, 0, 0))
        paste_x = (target_width - new_width) // 2
        paste_y = (target_height - new_height) // 2
        new_img.paste(resized_img, (paste_x, paste_y))
        
        return new_img
    
    elif fit_mode == 'cover':
        ratio = max(target_width / original_width, target_height / original_height)
        new_width = int(original_width * ratio)
        new_height = int(original_height * ratio)
        
        # Resize the image
        resized_img = img.resize((new_width, new_height), Image.LANCZOS)
        
        # Crop to the target dimensions
        left = (new_width - target_width) // 2
        top = (new_height - target_height) // 2
        right = left + target_width
        bottom = top + target_height
        
        return resized_img.crop((left, top, right, bottom))
    
    else:
        raise ValueError(f"Unknown fit mode: {fit_mode}")


def create_comic_pages(image_files, image_path, preset, output_path, fit_mode):
    """Create comic pages by placing images into the layout cells."""
    page_width = preset['page']['width']
    page_height = preset['page']['height']
    bg_color = preset['page']['background_color']
    cells = preset['layout']['cells']
    cells_per_page = len(cells)
    
    # Calculate how many pages we need
    num_pages = (len(image_files) + cells_per_page - 1) // cells_per_page
    
    for page_num in range(num_pages):
        # Create a blank page
        page = Image.new('RGB', (page_width, page_height), bg_color)
        
        # For each cell in the layout
        for cell_idx in range(cells_per_page):
            image_idx = page_num * cells_per_page + cell_idx
            
            # Skip if we've run out of images
            if image_idx >= len(image_files):
                break
                
            # Get the corresponding cell definition
            cell = cells[cell_idx]
            
            # Open and resize the image
            img_path = os.path.join(image_path, image_files[image_idx])
            try:
                img = Image.open(img_path).convert('RGBA')
                
                # Resize image to fit the cell
                fitted_img = fit_image(img, cell['width'], cell['height'], fit_mode)
                
                # Paste the image onto the page
                if fitted_img.mode == 'RGBA':
                    # Use mask for transparent images
                    page.paste(fitted_img, (cell['x'], cell['y']), fitted_img)
                else:
                    page.paste(fitted_img, (cell['x'], cell['y']))
                
                print(f"Placed image {image_files[image_idx]} in cell {cell_idx+1}")
                
            except Exception as e:
                print(f"Error processing image {img_path}: {e}")
                continue
        
        # Save the page
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        folder_name = os.path.basename(os.path.normpath(image_path))
        output_filename = f"{folder_name}_{timestamp}_page{page_num+1}.png"
        output_filepath = os.path.join(output_path, output_filename)
        
        try:
            os.makedirs(output_path, exist_ok=True)
            page.save(output_filepath)
            print(f"Saved page {page_num+1} to {output_filepath}")
        except Exception as e:
            print(f"Error saving page {page_num+1}: {e}")


def main():
    """Main function to run the comic panel composer."""
    args = parse_arguments()
    
    print(f"Loading preset from {args.preset}")
    preset = load_preset(args.preset)
    
    print(f"Loading images from {args.image_path}")
    image_files = get_image_files(args.image_path)
    
    if not image_files:
        print("No image files found in the specified directory.")
        sys.exit(1)
    
    # Create output directory if not specified
    if args.output is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        folder_name = os.path.basename(os.path.normpath(args.image_path))
        args.output = f"{folder_name}_{timestamp}"
    
    print(f"Creating comic pages with {len(image_files)} images using fit mode: {args.fit}")
    create_comic_pages(image_files, args.image_path, preset, args.output, args.fit)
    
    print(f"Successfully created comic layout in {args.output}")


if __name__ == "__main__":
    main()