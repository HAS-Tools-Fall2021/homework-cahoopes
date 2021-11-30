Week 14 homework submission - by Andrew Hoopes

____
## Grade: 
3/3:  Really great job reflecting on this process and walking through everything! Yours is a great example of a repo that appears to be thoughtfully setup and well documented but when you really try to use it causes trouble. Environments are a very common cause of issues as are compiled codes like the fortran you ran into. 
______

1. The paper I picked was titled SMAP-HydroBlocks, a 30-m satellite-based soil moisture dataset for the conterminous US.  The paper came from the scientific data journal from nature.co, and it was accessed from https://www.nature.com/articles/s41597-021-01050-2.  This paper developed an extremely high resolution (30m) dataset for soil moisture, using land surface and radiative transfer modeling, machine learning, microwave satellite data, and in-situ observations.

2. Code for the HydroBlocks land surface model was included, stored on two separate github repos; one at https://github.com/chaneyn/HydroBlocks and the other at https://github.com/chaneyn/geospatialtools.  The code made available was for a simplified version of the land surface model.  Unfortunately, the full model, with machine learning components, use in the final paper, only had its code availiable "upon request".

3. The repos themselves were quite well-organized, with a clear heirarchy of files, directories, and codes.  The readme file as also quite helpful during the model setup, as it contained the exact steps to obtain the necessary repositories and python packages, run the code, and get the necessary data, though I was not able to replicate these steps for reasons I will explain later.  While the readme and file hierarchies were easy to understand, the codes themselves were not.  Most of the parent python codes were barebones, containing nothing more than direct calls to various source code files, most of them run in fortran.  The python codes were written so that working with the source code was unnecessary, but it was sometimes unclear as to which source code file was being called, making troubleshooting very difficult.  The readme file, although detailed with its steps, likewise contained no information on what was being done in each of the steps, only giving the steps and nothing else.  It is likely the writers assumed, given the detailed nature of the steps and the lack of information on what the code was doing in them, that, as long as the steps were followed exactly, the code would run without any problems.  This makes the code act like a black box, something which would be unhelpful should errors arise.

An example of a python code. This is a preprocessing code, the entire py file, the last one ran before the model itelf.  In the course of running it, several routine status messages appeared, likely sourced from the fortran-based source code before eventually returning a "process killed" message, without any errors.  I was unable to ascertain the source of these messages due to the short time limit, and therefore did not know whether the process had been sucessful and where it had gotten stuck if not.  Running the main model code afterwards gave me actual errors.

import datetime
import Preprocessing
import sys

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

def Read_Metadata_File(file):

 import json
 metadata = json.load(open(file))['Preprocessing']

 return metadata


#Read in the metadata file
metadata_file = sys.argv[1]
metadata = Read_Metadata_File(metadata_file)
info = metadata
info['idate'] = datetime.datetime(metadata['startdate']['year'],
                           metadata['startdate']['month'],
                           metadata['startdate']['day'],0)
info['fdate'] = datetime.datetime(metadata['enddate']['year'],
                           metadata['enddate']['month'],
                           metadata['enddate']['day'],0) + datetime.timedelta(days=1) - datetime.timedelta(seconds=info['dt'])


#Cluster the data
Preprocessing.Prepare_Model_Input_Data(info)

4. It has likely already become apparent, but I was not sucessful in running the code.  I have already men tioned the possible error during preprocessing, and trying to run the model afterward gave a key error; an improperly-referenced variable call.  Although the steps to run the code were clear, there was no assistance if errors appeared, and the lack of commenting and referencing within the code made it hard to find the exact source of errors.  Additional problems came from the version of Python used.  The code was made for version 3.6, but I was running version 3.8.  I tried to rectify this by creating a separate environment in the older python version, a step suggested by the readme file, but, for an unknown reason, I could not install any packages to this new environment upon creation, the installer would always say there was a conflict with the readme-suggested packages.  I was unable to figure out why this was happening, and this also took time away from my search through the source code.  It may be that the errors experienced were the result of a version conflict, and, had I been able to create the python 3.6 environment described in the readme, the code would have ran without any issues.  It seems the authors assumed as such, due to the lack of support outside of exact steps within the readme.

5. The data referred to by the readme was stored in an online dropbox, and needed to be untarred upon downloading.  Once extracted, the input files were all in netcdf4 format, with associated metadata extracted as a .json file.  The metaata was read in via the code, one example shown earlier in question 3.  I was able to access the data without any issues, as the readme showed exactly where it was and how to get it.  The data referenced was made for an idealized test case within the model, as the full data was again only availiable "on request".

6. My experinces with this repo showed the importance of clear commenting and data referencing within scripts, especially if source code not directly referenced by the parent script is being worked with.  Without such information, I was unable to easily resolve the errors that came up when I tried to run it. I would recommend that the authors here more clearly reference the behind the scenes processes involving the model source code, either within the readme files or in comments within the various python scripts.  This would make it easier to understand exactly what is being done with the model at each step, and would aid in troubleshooting should any errors pop up.  I would also recommend making the full code availiable once the issues in what is already availiable are resolved.
