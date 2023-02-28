# Description
This Jupyter notebook was is a basic dart tracker that can be used to visualize improvements in dart throwing ability over time without the need for sophistocated tracking software. In short, this notebook will allow you to visualize what sections of the dartboard you are hitting over time with very minimal coding skill needed. This notebook will provide both a background as to how the code works, the general logic behind the setup, and then ultimately how to track dart throwing to generate images that can be converted into a heatmap video.
# Examples
This notebook, as stated before, will first go through the general logic behind how the code works and how the dart board in python was created. For those who are not interested in the technical coding aspects, all functions care called to the notebook but not written out in the notebook, making it more user friendly.

<img src="darts_images/position_array.jpeg" width="300" height="300"><img src="darts_images/numbervalue_array.jpeg" width="300" height="300">


**Figure 1**: *Left: Array displaying the different positions, such as 2X, 3X, etc. Right: Array displaying the different number values on a dartboard*

The notebook will then allow you to upload your own data and generate an array for every consecutive dart thow. These images can be exported and compiled into a movie using other programs.

<img src="darts_images/heatmap_ex1.jpeg" width="300" height="300">

**Figure 2**: *Example heatmap. The more red the section, the more times that section has been hit. This is 1D array (think x and y coordinates) displayed from a 3D array where the third dimenion is each throw.*

# Getting Started
## Dependencies
- Python 3.1 (other versions not guaranteed)
  
## Installing
- git clone https://github.com/msindoni/darts_tracker.git
- conda env create -f environment.yml
- conda env create -f requirements.txt

# Executing Program
- Format of input csv is provided (blank_table.csv)
- Table set up for different dates, rounds, and number of darts thrown and then the position and number for each dart throw.
- Input values for position column going from the center of the board outwards are below:
  
|Position| table input|
|--------| -----------|
| center bullseye| 0.5|
|outter ring bullseye|0.25|
|inner ring of values| 0.1|
|double (x3)| 0.3|
|otter ring of values|0.8|
|tripple (3x)| 0.3|
|out of bounds (black ring)|0.7|
|dart bounces/does not stay| 0.99|

- For the score column, values are just the section that the dart lands on.
- For the following section, if hit, the score column should contain a zero:
    - center blullseye
    - outter ring bullseye
    - out of bounds
    - dart bounce/does not stay

## Variables/Inputs
- directory_file: path to and file name of csv file containing dart data.
- directory: path to where user wants heatmap images to be saved to. Best to have a separate folder for these images since one image per dart will be generated.

# Authors
- Michael Sindoni msindoni22@gmail.com
# License
This project is licensed under the MIT License - see the LICENSE file for details