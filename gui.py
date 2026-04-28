import os
import subprocess
import sys
import time
import tkinter as tk
from tkinter import *
from tkinter import ttk

try:
    import winsound
except ImportError:
    winsound = None

from code import load_brainwave_data, turn_data_into_notes
from player import create_midi_file, create_wav_file


here = os.path.dirname(os.path.abspath(__file__))
default_csv = os.path.join(here, "data.csv")
default_midi = os.path.join(here, "brain_music.mid")


def average_waves(data):
    keys = ["alpha", "beta", "delta", "theta", "gamma"]
    result = {}
    for key in keys:
        total = 0
        for row in data:
            total += row[key]
        result[key] = total / len(data)
    return result


def make_wav_name(midi_path):
    if midi_path.lower().endswith(".mid"):
        return midi_path[:-4] + ".wav"
    return midi_path + ".wav"


def get_audio_command(wav_path):
    if winsound is not None:
        return []
    if sys.platform == "darwin":
        return ["afplay", wav_path]
    return []


class MusicWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Waves")
        self.root.minsize(1020, 780)

        self.csv_path = tk.StringVar(value=default_csv)
        self.midi_path = tk.StringVar(value=default_midi)
        self.status = tk.StringVar(value="Waiting...")

        if winsound is None and not get_audio_command(make_wav_name(default_midi)):
            self.status.set("Audio playback unavailable")

        self.current_data = []
        self.current_notes = []
        self.brainwave_summary = {}
        self.play_started_at = None
        self.play_duration = 0
        self.audio_process = None

        self.header_color = "#233446"
        self.background_color = "#f0f4f8"
        self.panel_color = "#ffffff"
        self.border_color = "#b4b4b4"
        self.text_color = "#202020"
        self.muted_color = "#5a5a5a"
        self.generate_color = "#3e8c5c"
        self.help_color = "#6e6e6e"
        self.play_color = "#4862a2"
        self.stop_color = "#965643"

        self.make_screen()
        self.root.after(120, self.keep_playing)

)

    def make_button(self, parent, text, command, background):
        button = tk.Button(parent,text=text,command=command,bg=background,fg="black",activebackground=background,activeforeground="black",font=("Arial", 13),relief="flat",cursor="hand2")
        return button

    def make_screen(self):
        self.root.configure(bg=self.background_color)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        header = tk.Frame(self.root, bg=self.header_color, height=92)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)
        header.columnconfigure(0, weight=1)

        title = tk.Label(
            header,
            text="Brainwave To Music",
            bg=self.header_color,
            fg="white",
            font=("Arial", 28, "bold"),
            anchor="w",
        )
        title.grid(row=0, column=0, sticky="nsew", padx=42)

        content = tk.Frame(self.root, bg=self.background_color)
        content.grid(row=1, column=0, sticky="nsew", padx=42, pady=28)
        content.columnconfigure(0, weight=1)
        content.rowconfigure(5, weight=1)

        csv_label = tk.Label(content,
            text="CSV file path",
            bg=self.background_color,
            fg=self.text_color,
            font=("Arial", 15),
            anchor="w")
        csv_label.grid(row=0, column=0, sticky="ew")

        self.csv_entry = ttk.Entry(content, textvariable=self.csv_path, font=("Arial", 14))
        self.csv_entry.grid(row=1, column=0, sticky="ew", ipady=10, pady=(6, 22))

        midi_label = tk.Label(
            content,
            text="MIDI save path",
            bg=self.background_color,
            fg=self.text_color,
            font=("Arial", 15),
            anchor="w",
        )
        midi_label.grid(row=2, column=0, sticky="ew")

        self.midi_entry = ttk.Entry(content, textvariable=self.midi_path, font=("Arial", 14))
        self.midi_entry.grid(row=3, column=0, sticky="ew", ipady=10, pady=(6, 18))

        status_label = tk.Label(
            content,
            textvariable=self.status,
            bg=self.background_color,
            fg=self.header_color,
            font=("Arial", 15),
            anchor="w",
        )
        status_label.grid(row=4, column=0, sticky="ew", pady=(0, 10))

        body = tk.Frame(content, bg=self.background_color)
        body.grid(row=5, column=0, sticky="nsew")
        body.columnconfigure(0, weight=1)
        body.rowconfigure(2, weight=1)

        buttons = tk.Frame(body, bg=self.background_color)
        buttons.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        buttons.columnconfigure((0, 1), weight=1, uniform="buttons")

        generate_button = self.make_button(buttons, "Generate Music", self.make_files, self.generate_color)
        generate_button.grid(row=0, column=0, sticky="ew", padx=(0, 8), ipady=9)

        help_button = self.make_button(buttons, "Help", self.help_text, self.help_color)
        help_button.grid(row=0, column=1, sticky="ew", padx=(8, 0), ipady=9)

        play_button = self.make_button(buttons, "Play WAV", self.play_sound, self.play_color)
        play_button.grid(row=1, column=0, sticky="ew", padx=(0, 8), pady=(8, 0), ipady=9)

        stop_button = self.make_button(buttons, "Stop Audio", self.stop_sound, self.stop_color)
        stop_button.grid(row=1, column=1, sticky="ew", padx=(8, 0), pady=(8, 0), ipady=9)

        self.visualization = tk.Canvas(
            body,
            bg=self.panel_color,
            highlightthickness=1,
            highlightbackground=self.border_color,
            height=210,
        )
        self.visualization.grid(row=1, column=0, sticky="ew", pady=(0, 22))
        self.visualization.bind("<Configure>", lambda _event: self.draw_stuff())

        self.log = tk.Text(
            body,
            bg=self.panel_color,
            fg=self.text_color,
            font=("Courier New", 11),
            height=12,
            wrap="none",
            relief="solid",
            borderwidth=1,
        )
        self.log.grid(row=2, column=0, sticky="nsew")
        self.log.configure(state="disabled")

    def put_words(self, lines):
        self.log.configure(state="normal")
        self.log.delete("1.0", END)
        self.log.insert(END, "\n".join(lines))
        self.log.configure(state="disabled")
    
    def make_files(self):
        try:
            csv_path = self.csv_path.get().strip()
            midi_path = self.midi_path.get().strip()
            wav_path = make_wav_name(midi_path)

            data = load_brainwave_data(csv_path)
            notes = turn_data_into_notes(data)

            if not notes:
                self.current_data = []
                self.current_notes = []
                self.brainwave_summary = {}
                self.status.set("The file had no data")
                self.put_words(["The file had no data."])
                self.draw_stuff()
                return

            self.stop_sound()
            create_midi_file(notes, midi_path)
            create_wav_file(midi_path, wav_path)

            self.current_data = data
            self.current_notes = notes
            self.brainwave_summary = average_waves(data)

            total_duration = 0
            for note in notes:
                total_duration += note["duration"]
            self.play_duration = total_duration

            lines = []
            lines.append("Saved MIDI file:")
            lines.append(midi_path)
            lines.append("")
            lines.append("Saved WAV file:")
            lines.append(wav_path)
            lines.append("")

            index = 1
            for note in notes:
                 line = "note %s | pitch %s | tempo %s | duration %.2f | velocity %s" % (index, note["pitch"], note["tempo"], note["duration"], note["velocity"])
                 lines.append(line)
                 index += 1

            self.status.set("Saved MIDI and WAV files")
            self.put_words(lines)
            self.draw_stuff()
        except Exception as err:
            self.status.set("Could not make files")
            self.put_words([str(err)])

    def help_text(self):
        self.status.set("Showing help")
        lines = []
        lines.append("How to use:")
        lines.append("1. Type the CSV file path in the top box.")
        lines.append("2. Type where the MIDI should save in the second box.")
        lines.append("3. Press Generate Music Files.")
        lines.append("4. The WAV file will save next to the MIDI file.")
        lines.append("")
        lines.append("Default CSV file already points to data.csv in this folder.")
        self.put_words(lines)

    def play_sound(self):
        wav_path = make_wav_name(self.midi_path.get().strip())

        if not os.path.exists(wav_path):
            self.status.set("No WAV file to play")
            self.put_words(["Generate music first so the WAV file exists.", wav_path])
            return

        try:
            self.stop_sound(update_status=False)
            audio_command = get_audio_command(wav_path)

            if winsound is not None:
                winsound.PlaySound(wav_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
            elif audio_command:
                with open(os.devnull, "wb") as devnull:
                    self.audio_process = subprocess.Popen(audio_command, stdout=devnull, stderr=devnull)
            else:
                self.status.set("Audio playback unavailable")
                self.put_words([
                    "WAV playback is not available on this system.",
                    "Windows uses winsound. macOS needs afplay.",
                ])
                return

            self.play_started_at = time.monotonic()
            if self.current_notes:
                total = 0
                for note in self.current_notes:
                    total += note["duration"]
                self.play_duration = total
            self.status.set("Playing WAV file")
        except (OSError, RuntimeError) as err:
            self.play_started_at = None
            self.audio_process = None
            self.status.set("Could not play WAV file")
            self.put_words([str(err)])

    def stop_sound(self, update_status=True):
        if winsound is not None:
            winsound.PlaySound(None, winsound.SND_PURGE)
        elif self.audio_process is not None:
            self.audio_process.terminate()
            try:
                self.audio_process.wait(timeout=1)
            except subprocess.TimeoutExpired:
                self.audio_process.kill()
                self.audio_process.wait(timeout=1)
            self.audio_process = None
        self.play_started_at = None
        self.draw_stuff()
        if update_status and self.status.get() == "Playing WAV file":
            self.status.set("Audio stopped")

    def keep_playing(self):
        if self.play_started_at is not None and self.play_duration:
            time_passed = time.monotonic() - self.play_started_at
            if time_passed >= self.play_duration:
                self.play_started_at = None
                self.audio_process = None
            self.draw_stuff()
        self.root.after(120, self.keep_playing)

    def get_seconds(self):
        if self.play_started_at is None:
            return None
        return time.monotonic() - self.play_started_at

    def find_note(self, secs):
        if secs is None or not self.current_notes:
            return None
        total = 0
        for i in range(len(self.current_notes)):
            note = self.current_notes[i]
            total += note["duration"]
            if secs < total:
                return i
        return len(self.current_notes) - 1

    def get_bar_values(self, active_note):
        if active_note is not None and 0 <= active_note < len(self.current_data):
            return self.current_data[active_note], "Current note %s values" % (active_note + 1)
        return self.brainwave_summary, "Average brainwave values"

    def draw_stuff(self):
        viz = self.visualization
        viz.delete("all")

        width = viz.winfo_width()
        if width < 1:
            width = 1
        height = viz.winfo_height()
        if height < 1:
            height = 1

        viz.create_text(14, 14, text="Visualization", fill=self.header_color, font=("Arial", 12), anchor="nw")

        if not self.current_notes or not self.brainwave_summary:
            viz.create_text(14, 50, text="Generate music to see brainwave bars and note timeline.",
                fill=self.muted_color, font=("Courier New", 11), anchor="nw")
            return

        labels = [
            ("alpha", "#4678dc"),
            ("beta", "#dc9241"),
            ("delta", "#3e8c5c"),
            ("theta", "#965643"),
            ("gamma", "#785aaa"),
        ]

        bar_left = 14
        bar_top = 50
        bar_area_width = int(width * 0.38)
        if bar_area_width < 260:
            bar_area_width = 260
        bar_gap = 10
        bar_height = int((height - 76) / len(labels)) - bar_gap
        if bar_height < 16:
            bar_height = 16

        active_note = self.find_note(self.get_seconds())
        bar_values, bar_title = self.get_bar_values(active_note)

        viz.create_text(bar_left, 30, text=bar_title, fill=self.header_color, font=("Courier New", 11), anchor="nw")

        for i in range(len(labels)):
            label = labels[i][0]
            color = labels[i][1]
            y = bar_top + i * (bar_height + bar_gap)
            value = bar_values[label]

            viz.create_text(bar_left, y, text="%s %.2f" % (label, value),
                fill=self.text_color, font=("Courier New", 11), anchor="nw")

            track_x = bar_left + 100
            track_y = y + 2
            track_width = bar_area_width - 118
            viz.create_rectangle(track_x, track_y, track_x + track_width, track_y + bar_height - 4, fill="#e6eaee", outline="")

            fill_width = track_width * value
            if fill_width < 0:
                fill_width = 0
            if fill_width > track_width:
                fill_width = track_width
            if fill_width < 2:
                fill_width = 2
            viz.create_rectangle(track_x, track_y, track_x + fill_width, track_y + bar_height - 4, fill=color, outline="")

        chart_x = bar_area_width + 26
        chart_y = 42
        chart_width = width - chart_x - 14
        if chart_width < 80:
            chart_width = 80
        chart_height = height - chart_y - 18
        if chart_height < 80:
            chart_height = 80

        viz.create_text(chart_x, 14, text="Pitch / velocity timeline", fill=self.header_color, font=("Courier New", 11), anchor="nw")
        viz.create_rectangle(chart_x, chart_y, chart_x + chart_width, chart_y + chart_height, fill="#f4f7fa", outline="")

        min_pitch = self.current_notes[0]["pitch"]
        max_pitch = self.current_notes[0]["pitch"]
        for note in self.current_notes:
            if note["pitch"] < min_pitch:
                min_pitch = note["pitch"]
            if note["pitch"] > max_pitch:
                max_pitch = note["pitch"]

        pitch_span = max_pitch - min_pitch
        if pitch_span < 1:
            pitch_span = 1

        note_width = chart_width / len(self.current_notes)
        if note_width < 3:
            note_width = 3

        for i in range(len(self.current_notes)):
            note = self.current_notes[i]
            normalized_pitch = (note["pitch"] - min_pitch) / pitch_span
            normalized_velocity = note["velocity"] / 127
            rect_width = note_width - 1
            if rect_width < 2:
                rect_width = 2
            rect_height = chart_height * (0.2 + normalized_velocity * 0.8)
            if rect_height < 8:
                rect_height = 8
            x = chart_x + i * note_width
            space = chart_height - rect_height
            if space < 1:
                space = 1
            y = chart_y + chart_height - rect_height - normalized_pitch * space
            if active_note == i:
                color = "#e26c49"
            else:
                color = "#5283c6"
            viz.create_rectangle(x, y, x + rect_width, y + rect_height, fill=color, outline="")

        secs = self.get_seconds()
        if secs is not None and self.play_duration > 0:
            position = secs / self.play_duration
            if position > 1:
                position = 1
            playhead_x = chart_x + position * chart_width
            viz.create_line(playhead_x, chart_y, playhead_x, chart_y + chart_height, fill="#282828", width=2)


def main():
    root = tk.Tk()
    app = MusicWindow(root)
    root.protocol("WM_DELETE_WINDOW", lambda: (app.stop_sound(), root.destroy()))
    root.mainloop()

main()





    


            
