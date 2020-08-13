# Background Information and Requirements

- Data was collected using cellphones running Physics Toolbox Sensor Suite and can be found in the file Raw Data file

- All code requires Python 3 
- Required Libraries: numpy, pandas, matplotlib, seaborn, scipy, math, sys

# Running the Pipeline
While in the Project Directory runnin the following commands will output plots
into the Report_and_Figures Directory:

Script to determine best Butterworth via Fourier:
py /Python/KevinAnalysis_Fourier.py /Raw_data/15min_sam.csv

Script to view the noise reduction due to Butterworth filtering:
py .\Python\KevinAnalysis_filtering.py .\Raw_data\walk_kevin.csv

This script returns graphs velocity and distance of individual for subset of time:
py Python/KevinVelocity.py /Raw_data/15min_sam.csv'

This script returns graphs all velocity and distance of individual:
py Python/big_scale_velocity.py /Raw_data/15min_sam.csv'