# Background Information on project and repository

- Data was collected using cellphones running Physics Toolbox Sensor Suite and can be found in the file Raw Data file
- Python and Jupyter notebooks relevent to the project can be found in the Python Directory
- running the python scripts will result in plots being saved to Report_and_Figures Directory
----
# Requirements
- All code requires Python 3 and Jupyter Notebook
- Required Libraries: numpy, pandas, matplotlib, seaborn, scipy, sklearn, math, sys
----
# Running the Pipeline
After cloning this git move to the Project Directory if you are not already there.  
While in the Project Directory running the following commands will output plots
into the Report_and_Figures Directory:

Script to determine best Butterworth via Fourier:  
py /Python/KevinAnalysis_Fourier.py /Raw_data/15min_sam.csv

Script to view the noise reduction due to Butterworth filtering:  
py /Python/KevinAnalysis_filtering.py /Raw_data/15min_sam.csv

This script returns graphs velocity and distance of individual for subset of time with bad method:  
py Python/KevinVelocity.py Raw_data/15min_sam.csv

This script returns graphs all velocity and distance of individual with bad method:  
py Python/big_scale_velocity.py Raw_data/15min_sam.csv

This script returns graphs all velocity and distance using best method:  
py Python/Velocity_and_Distance.py Raw_data/15min_sam.csv

Script to predict the exercises based on x, y, and z forces:  
python3 Python/Vera_ML_Exercise.py Raw_data/labelled_exercises.csv Raw_data/unlabelled_exercises.csv Raw_data/