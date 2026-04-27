import pretty_midi
import wave, struct


def create_midi_file(notes, filename):
    midi = pretty_midi.PrettyMIDI()
    piano = pretty_midi.Instrument(
        program=pretty_midi.instrument_name_to_program("Voice Oohs")
    )

    start = 0

    for note in notes:
        pitch = note["pitch"]
        velocity = note["velocity"]
        duration = note["duration"]
        end = start + duration

        n = pretty_midi.Note(
            velocity=velocity,
            pitch=pitch,
            start=start,
            end=end
        )

        piano.notes.append(n)
        start = end

    midi.instruments.append(piano)
    midi.write(filename)


def create_wav_file(midi_name, wav_name):
    midi_data = pretty_midi.PrettyMIDI(midi_name)
    audio = midi_data.synthesize(fs=44100)

    wav = wave.open(wav_name, "w")
    # write wav
    wav.setnchannels(1)
    wav.setsampwidth(2)
    wav.setframerate(44100)

    for sample in audio:
        n = int(sample * 32767)
        n = max(-32768, min(n, 32767))
        wav.writeframes(struct.pack("<h", n))

    wav.close()
