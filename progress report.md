# Status Report

#### Your name

Anastacia Orekhova

#### Your section leader's name

Daniel Blitshtein

#### Project title

Music Waves

***

Short answers for the below questions suffice. If you want to alter your plan for your project (and obtain approval for the same), be sure to email your section leader directly!

#### What have you done for your project so far?

I used VS Code to write the code and connected it to a GitHub repository. First of all, I created 5 files: code.py, mapper.py, player.py, gui.py, and data.csv. In data.csv I put a simulated brainwave dataset with five columns representing the five brain wave types: alpha, beta, delta, theta, and gamma. I wrote and tested five mapping functions in mapper.py that convert brainwave values (0.0–1.0) into musical properties. After that, I implemented file reading in code.py that reads the brainwave data, converts all values to floats, and passes them through the mapping functions. Confirmed the full code works by  printing mapped musical values for all five rows of data.

#### What have you not done for your project yet?

I have not yet included MIDI file generation using the pretty_midi library, which will convert the mapped values into an actual playable music file. I still need to finish building the graphical user interface using tkinter, which will allow a user to load a CSV file and trigger music generation through buttons. 

#### What problems, if any, have you encountered?

I've been having troubles with pushing my code to Github for some reason. I'm currently trying to figure out why.
# Final-Project-1
