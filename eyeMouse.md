'\_' this is used because fr.read() gives us two variables first bieng of no use and second being the frame hence we use '\_' as we not require the second one

image is always captured in BGR format we have to convert it into a rgb format

we use allface landmarks as it returns us the x,y,z coordinates of the face we are currently tracking

MediaPipe provides a set of 468 3d face landmarks, but mediapipe facemesh extends it landmarks 474->478 are part of it and is used for precise iris and eye tracking

right eye ke corrds -> 474->478
left eye ko corrds ->145->160

TO move the mouse with the right eye we need the id of the landmark points and landmark points -> for this we use enumerate function

The enumerate function in Python is a built-in function that allows you to iterate over a list (or any iterable) and have an automatic counter. This is useful when you need both the elements and their index positions during iteration.

Coordinates ->
leftbottom ->145 rightbottom->374
lefttop ->159 righttop ->386
