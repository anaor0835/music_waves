# Music Waves

This project reads brainwave data from a CSV file and turns it into music files.

Required libraries:
- `pretty_midi`

Files:
- `code.py` reads the CSV data and maps it into music note values
- `mapper.py` changes brainwave values into pitch, tempo, duration, velocity, and octave
- `player.py` creates the MIDI file and WAV file
- `gui.py` opens a simple Tkinter window so the user can type a CSV path, generate the music files, and play the WAV file
- `data.csv` and `happy_birthday_brain_waves.csv` sample brainwave files

Run:
- `python gui.py`
- or `python code.py`

In the Tkinter window:
- type the CSV file path in the first box
- type the MIDI save path in the second box
- click `Generate Music Files`

The CSV file should have these columns:
- `alpha`
- `beta`
- `delta`
- `theta`
- `gamma`

Output:
- Generated `.wav` and `.mid` files with music! 

Playback:
- Windows uses `winsound`
- macOS uses `afplay`