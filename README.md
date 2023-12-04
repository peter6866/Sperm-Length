# Measuring Sperm Length

An interactive tool for cell length using Python and Gradio as the GUI interface.

## Getting Started

These instructions will get you the project up and running on your local machine for development and testing purposes.

## Setting Up the Conda Environment
1. Navigate to the Project Directory and use the provided 'environment.yml' file to create your Conda environment by 'conda env create -f environment.yml'
2. Activate the newly created environment by 'conda activate geometric'

## Start the project
1. In the current directory, run 'python src/main.py' and click the URL.
2. Upload image and draw roi using red marker that is close to the cell.
3. Use a thinner white marker to draw rough sketch on the cell if needed.
4. Select appropriate threshold and click submit.

## Tested threshold values
| Filename         | threshold value |
|------------------|-----------------|
| 24708.1_1 at 20X | 186             |
| 24708.1_2 at 20X | 166             |
| 24708.1_3 at 20X | 178             |
| WT.C.1           | 47              |
| WT.C.2           | 32              |
| 24708.1_4 at 20X | 181             |
| 28369.2.6_2      | 139             |


