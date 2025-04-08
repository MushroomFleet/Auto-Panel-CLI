# Comic Panel Composer

## Description

Comic Panel Composer is a Python-based command-line tool designed to automatically arrange sequential images into comic book page layouts. The tool offers a streamlined solution for comic creators, storyboard artists, and visual storytellers who need to efficiently organize their sequential imagery into structured, visually appealing page layouts without manual positioning of each panel.

## Functionality

### Core Features

- **Automated Panel Arrangement**: Takes a folder of sequential images and arranges them into predefined comic panel layouts
- **Multiple Page Generation**: Automatically generates multiple pages if there are more images than cells in the layout
- **Sequence Preservation**: Maintains the original sequence order of images when arranging into panels
- **Customizable Layouts**: Supports various predefined layout templates via JSON preset files

### Configuration Options

- **Image Fitting Options**: Supports multiple ways to fit images within panels:
  - `contain`: Preserves aspect ratio while ensuring the entire image fits (may leave empty space)
  - `cover`: Preserves aspect ratio while filling the entire cell (may crop image edges)
  - `stretch`: Stretches image to fill cell completely (may distort image)
- **Overlay Support**: Optional overlay images (frames, decorations, etc.) can be applied to each completed page
- **Output Customization**: Custom output directory naming and organization

### User Interface

- **Command Line Interface**: Simple CLI that accepts parameters for image folder, layout preset, output location, and options
- **Batch File Support**: Windows users can utilize batch files for quick execution with predefined or custom parameters

## Technical Implementation

### Architecture

- **Single Module Design**: Core functionality implemented in a single Python script (`comic_panel_composer.py`)
- **Configuration-based**: Layout definitions stored in JSON preset files
- **Pipeline Processing**: Sequential processing of images through loading, arrangement, and output phases

### Data Structures

- **Layout Configuration**: JSON structure defining page parameters, dimensions, and cell positions
- **Cell Definitions**: Each cell contains an ID, position (x, y), and dimensions (width, height)
- **Image Sequence**: Ordered collection of input images maintained throughout processing

### Core Algorithms

1. **Image Loading**: Loads and sorts all images from input directory by filename
2. **Layout Application**: Maps images to cells according to the specified layout
3. **Image Fitting**: Applies selected fitting algorithm (contain, cover, stretch) to each image
4. **Page Generation**: Creates new pages as needed when more images exist than the layout can accommodate
5. **Overlay Application**: Composites overlay image on top of completed pages if specified

### External Dependencies

- **Python 3.6+**: Core language runtime
- **Pillow (PIL)**: Python imaging library for image manipulation and composition

## Setup Instructions

### Windows Installation (Easy Setup)

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

## Usage Guide

### Windows Users (Using Batch Files)

Basic usage:
```
start-layout.bat (defined inside the batch file)
```

Advanced usage:
```
start-layout.bat (options: path\to\image\folder --preset presets\3col_preset.json --output output_folder --fit cover --overlay frame\overlay_frame.png)
```

### Manual Usage (All Platforms)

Basic usage:

```bash
python comic_panel_composer.py path/to/image/folder
```

This will use the default 2-column, 3-row layout preset.

Advanced usage:

```bash
python comic_panel_composer.py path/to/image/folder --preset presets/3col_preset.json --output output_folder --fit cover --overlay frame/overlay_frame.png
```

### Parameters

- `image_path` (required): Path to directory containing sequential images
- `--preset`: Path to layout preset JSON file (default: presets/2col_preset.json)
- `--output`: Output directory (default: image_folder_timestamp)
- `--fit`: How to fit images in cells: 
  - `contain`: Preserve aspect ratio, fit entire image (may leave empty space)
  - `cover`: Preserve aspect ratio, fill entire cell (may crop image)
  - `stretch`: Stretch image to fill cell (may distort image)
- `--overlay`: Path to an overlay image to be placed on top of each completed page (optional)

## Custom Layouts

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

## Example Workflow

1. Place your sequential comic panel images in a folder
2. Run the tool with your chosen layout preset
3. The tool will:
   - Load all images from the folder and sort them by filename
   - Arrange them in the specified layout, preserving sequence
   - Create multiple pages if needed
   - Apply any specified overlay image on top of each completed page
   - Save the composed pages as PNG files with timestamp

## Directory Structure

```
comic-panel-composer/
├── comic_panel_composer.py  # Main script
├── README.md
├── requirements.txt        # Python dependencies
├── install.bat             # Setup script for Windows
├── start-layout.bat        # Launcher script for Windows
├── presets/
│   ├── 2col_preset.json
│   └── 3col_preset.json
└── frame/
    └── 2col_layout_frame1.png  # Example overlay frame
```

## License

MIT
