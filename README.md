https://youtu.be/mZxBL6PsIss
Due to the lack of time as the deadline appeared to be faster than anticipated + my general nervousness while recording myself I forgot to mention some new concets I've learned in order to complete this project, so I will list them in my README.
time.monotonic() — this is a clock that counts upward from the moment the program starts, this way I was able to track how many seconds have passed since the audio started playing.
Lambda - I ended with many functions, so I used in one line to connect the canvas resize to the draw function without needing an actual def statement. 
StringVar - this is a tkinter variable type that automatically updates the interface when its value changes.
MIDI and WAV - the very base of my project:
A MIDI file contains a set of instructions for audio. For example, it tells to play a specific note at a specific volume for a specific number of seconds.
WAV file contains real recorded audio aka actual sound waves saved as numbers. WAV files are uncompressed, meaning the audio is stored at full quality. This makes them larger in size, but the sound is better.
