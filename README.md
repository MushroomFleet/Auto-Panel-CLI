# Comic Panel Composer

A Python CLI tool that automatically arranges sequential images into comic book page layouts based on preset templates.

## Features

- Takes a folder of sequential images and arranges them into comic panel layouts
- Supports customizable layout templates via JSON preset files
- Multiple image fitting options: contain, cover, or stretch
- Automatically generates multiple pages if there are more images than cells in the layout
- Preserves image sequence order

## Requirements

- Python 3.6 or higher
- Pillow (PIL) library

## Installation

### Windows Users (Easy Setup)

1. Clone this repository or download the files
2. Double-click `install.bat` to:
   - Create a Python virtual environment
   - Install all required dependencies
   - Set up the presets directory

### Manual Installation (All Platforms)

1. Clone this repository or download the files
2. Install required dependencies:

```bash
pip install -r requirements.txt
# Or directly:
pip install pillow
```

3. Make the script executable (Linux/macOS):

```bash
chmod +x comic_panel_composer.py
```

## Usage

### Windows Users (Using Batch Files)

Basic usage:
```
start-layout.bat path\to\image\folder
```

Advanced usage:
```
start-layout.bat path\to\image\folder --preset presets\3col_preset.json --output output_folder --fit cover
```

### Manual Usage (All Platforms)

Basic usage:

```bash
python comic_panel_composer.py path/to/image/folder
```

This will use the default 2-column, 3-row layout preset.

Advanced usage:

```bash
python comic_panel_composer.py path/to/image/folder --preset presets/3col_preset.json --output output_folder --fit cover
```

## Parameters

- `image_path` (required): Path to directory containing sequential images
- `--preset`: Path to layout preset JSON file (default: presets/2col_preset.json)
- `--output`: Output directory (default: image_folder_timestamp)
- `--fit`: How to fit images in cells: 
  - `contain`: Preserve aspect ratio, fit entire image (may leave empty space)
  - `cover`: Preserve aspect ratio, fill entire cell (may crop image)
  - `stretch`: Stretch image to fill cell (may distort image)

## Directory Structure

```
comic-panel-composer/
├── comic_panel_composer.py  # Main script
├── README.md
├── requirements.txt        # Python dependencies
├── install.bat             # Setup script for Windows
├── start-layout.bat        # Launcher script for Windows
└── presets/
    ├── 2col_preset.json
    └── 3col_preset.json
```

## Creating Custom Layouts

You can create custom layout presets by creating a JSON file following this structure:

```json
{
  "name": "Custom Layout",
  "description": "A custom layout for comic pages",
  "page": {
    "width": 2480,  // A4 at 300 DPI
    "height": 3508,
    "background_color": "white"
  },
  "layout": {
    "rows": 3,
    "columns": 2,
    "margin": 100,
    "gutter": 20,
    "cells": [
      {
        "id": 1,
        "x": 100,  // X position from left
        "y": 100,  // Y position from top
        "width": 1130,
        "height": 1096
      },
      // More cells...
    ]
  }
}
```

Each cell defines:
- `id`: Unique identifier for the cell
- `x`, `y`: Coordinates of the top-left corner of the cell
- `width`, `height`: Dimensions of the cell

## Example Process

### For Windows Users:

1. Double-click `install.bat` to set up the environment (first-time only)
2. Place your sequential comic panel images in a folder
3. Double-click `start-layout.bat` and when prompted, type:
   ```
   path\to\your\images --preset presets\2col_preset.json
   ```
4. Find your composed comic pages in the output directory

### For All Users:

1. Place your sequential comic panel images in a folder
2. Run the tool with your chosen layout preset
3. The tool will:
   - Load all images from the folder and sort them by filename
   - Arrange them in the specified layout, preserving sequence
   - Create multiple pages if needed
   - Save the composed pages as PNG files with timestamp

## License

MIT