# AVSC project

<h3>About project</h3>

This is the project which we have been awarded in Sungkyunkwan University S-hero.

**Professor** : Electronic, Electrical and Computer Engineer 전재욱

**Mentor** : Telecommunications Research Institute Researcher 박성천

**Team Members** : Electronic electrical Engineer 박준호 박진석
Mechanical Engineer 홍영욱 이주헌 임진우   
  
<h3>Subject</h3>

**Autonomous Vehicle Separating and Coupling**

Rather than owning a large number of car models, 

we intend to develop a new type of transportation 

that can be freely combined and separated according to the needs of consumers 

by making a modular shared vehicle model.

In this broad topic, we focused on separating and coupling.

We created a coupler with 3D modeling and simulate it through CAD.

Also, using the Opencv tool and camera, we designed two vehicles to autonomously align for combination.


<h3>Code</h3>

#1 NewCalib 
#2 NewPoseEst

**First, you must prepare the chess board.**

**Second, view the chessboard on the sight of camera and execute #1 NewCalib.** 

You can get the calib.npz file from this code which contains information about camera.

**Next, execute #2 NewPoseEst. And move the chessboard in front of camera.**

You can get the parameters from above such as distance and tiltation between two cars.

Using these parameters you can control the RPM of motors.

Based on these parameter values, if it exceeds or falls short to a certain value, 

it is designed to change the motor rotation speed of Arduino by sending a signal through a Wi-Fi signal.

<h3>Presentation and testing Videos</h3>

https://drive.google.com/file/d/14X0415CaQd5Svz5pHHS3mrqSN1642C_3/view?usp=share_link

