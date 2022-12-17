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

It will show you how much the chessboard has tilted and distance from camera.

With tiltation and distance we can control the movement of cars.

