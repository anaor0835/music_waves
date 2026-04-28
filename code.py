import csv
import os
from mapper import map_to_pitch, map_to_tempo, map_to_duration, map_to_velocity, map_to_octave
from player import create_midi_file, create_wav_file

folder = os.path.dirname(os.path.abspath(__file__))


def load_brainwave_data(filepath):
    data = []
    with open(filepath, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            cur = {}
            cur["alpha"] = float(row["alpha"])
            cur["beta"] = float(row["beta"])
            cur["delta"] = float(row["delta"])
            cur["theta"] = float(row["theta"])
            cur["gamma"] = float(row["gamma"])
            data.append(cur)
    return data


def turn_data_into_notes(data):
    notes = []
    for row in data:
        p = map_to_pitch(row["alpha"]) + map_to_octave(row["gamma"])
        t = map_to_tempo(row["beta"])
        d = map_to_duration(row["delta"])
        v = map_to_velocity(row["theta"])
        p = max(0, min(p, 127))

        note = {
            "pitch": p,
            "tempo": t,
            "duration": d,
            "velocity": v
        }
        notes.append(note)

    return notes


def main():
    filepath = os.path.join(folder, "data.csv")
    data = load_brainwave_data(filepath)
    notes = turn_data_into_notes(data)

    for note in notes:
        print(
            f'Pitch: {note["pitch"]} | Tempo: {note["tempo"]} BPM | '
            f'Duration: {note["duration"]:.2f}s | Velocity: {note["velocity"]}'
        )

    out = os.path.join(folder, "brain_music.mid")
    wav_out = os.path.join(folder, "brain_music.wav")
    create_midi_file(notes, out)
    create_wav_file(out, wav_out)
    print(f"MIDI file saved to {out}")
    print(f"WAV file saved to {wav_out}")

main()
