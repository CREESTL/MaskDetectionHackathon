
# Person & Mask Detector
# What was this project about?
* Make web application implementing computer vision methods
* Use OpenVINO and OpenCV models to improve perfomance
* A)Find unique people to:
    1. Give them personal ID 
    2. Count them
    3. Calculate time they've spent indoors
* B)Or check the presence of a medical mask on their faces
 ____
### How to activate:
- You <strong>have</strong> to install OpenVINO in order to use this run this code!
- download weights for yolov3 [here](https://yadi.sk/d/WuMc8B3krEHh1Q)
- `cd C:\Program Files (x86)\IntelSWTools\openvino\bin` (this directory can be accessed only if OpenVINO is present on your PC)
- `setupvars.bin`
- `cd` to `this_project_folder/DjangoStream/`
- `python manage.py runserver`
- Go to `localhost:/8000/index` 
- Log in as: username - `a`, password - `1` (that simple) 
- Navigate through the website 

![Alt text](https://github.com/kremlev404/MaskDetectionHackathon/blob/kremlev/1.gif "Result")
____
#### What was used:
- Python 3.7
- Django
- OpenCV
- OpenVINO
- Bootstrap

