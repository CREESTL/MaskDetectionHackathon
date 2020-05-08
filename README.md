
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
- download weights for yolov3 [here](https://yadi.sk/d/vR00d0nHVo1qUA)
- `cd C:\Program Files (x86)\IntelSWTools\openvino\bin`
- `setupvars.bin`
- `cd` to `this_project_folder/DjangoStream/`
- `python manage.py runserver`
- Go to `localhost:/8000/index` 
- Log in as: username - `a`, password - `1` (that simple) 
- Navigate through the website 

![Alt text](https://github.com/kremlev404/MaskDetectionHackathon/blob/kremlev/1.gif "Result")
## Perfomed by OpenVino 
____
#### What was used:
- Python 3.7
- Django
- OpenCV
- OpenVINO
- Bootstrap

