import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pygame
import numpy as np
import os

class MusicVisualizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Visualizer")
        self.root.geometry("850x520")
        self.root.configure(bg="#0b0b0f")

        # Initialize Pygame mixer
        pygame.init()
        pygame.mixer.init()

        self.current_file = None
        self.is_paused = False
        self.is_playing = False

        # --- Title ---
        title_label = tk.Label(root, text="Music Visualizer", font=("Helvetica", 16, "bold"), fg="#00ffcc", bg="#0b0b0f")
        title_label.pack(pady=10)

        # --- Main Layout Frame ---
        main_frame = tk.Frame(root, bg="#0b0b0f")
        main_frame.pack(fill="both", expand=True, padx=15, pady=5)

        # Visualizer Canvas
        self.canvas = tk.Canvas(main_frame, bg="#0b0b0f", highlightthickness=0, height=280)
        self.canvas.pack(fill="both", expand=True, pady=10)

        # Now Playing Label
        self.now_playing_label = tk.Label(main_frame, text="Now Playing: No file selected", font=("Helvetica", 11, "bold"), fg="#00ffcc", bg="#0b0b0f")
        self.now_playing_label.pack(pady=5)

        # Control Panel Frame
        control_frame = tk.Frame(main_frame, bg="#0b0b0f")
        control_frame.pack(fill="x", pady=10)

        # Buttons
        select_btn = tk.Button(control_frame, text="📁 Choose Song", command=self.load_song, bg="#0088ff", fg="#ffffff", font=("Helvetica", 10, "bold"), relief="flat", padx=10, pady=5)
        select_btn.pack(side="left", padx=5)

        self.play_btn = tk.Button(control_frame, text="▶ Play", command=self.play_song, bg="#00ff88", fg="#0b0b0f", font=("Helvetica", 10, "bold"), relief="flat", padx=10, pady=5, state="disabled")
        self.play_btn.pack(side="left", padx=5)

        self.pause_btn = tk.Button(control_frame, text="⏸ Pause", command=self.pause_song, bg="#ffaa00", fg="#0b0b0f", font=("Helvetica", 10, "bold"), relief="flat", padx=10, pady=5, state="disabled")
        self.pause_btn.pack(side="left", padx=5)

        self.stop_btn = tk.Button(control_frame, text="⏹ Stop", command=self.stop_song, bg="#ff4444", fg="#ffffff", font=("Helvetica", 10, "bold"), relief="flat", padx=10, pady=5, state="disabled")
        self.stop_btn.pack(side="left", padx=5)

        # Volume Slider
        vol_label = tk.Label(control_frame, text="Volume:", fg="#ffffff", bg="#0b0b0f", font=("Helvetica", 10, "bold"))
        vol_label.pack(side="left", padx=(20, 5))

        self.vol_slider = ttk.Scale(control_frame, from_=0.0, to=1.0, value=0.7, command=self.change_volume)
        self.vol_slider.pack(side="left", padx=5)
        pygame.mixer.music.set_volume(0.7)

        # Visualizer settings
        self.bars = 45
        self.bar_colors = ["#00ffcc", "#00aaff", "#7b68ee", "#ff00ff"]

    def load_song(self):
        file_path = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=[("Audio Files", "*.mp3 *.wav *.ogg")]
        )
        if file_path:
            self.current_file = file_path
            filename = os.path.basename(file_path)
            self.now_playing_label.config(text=f"Now Playing: {filename}")
            
            try:
                pygame.mixer.music.load(self.current_file)
                self.play_btn.config(state="normal")
                self.stop_btn.config(state="normal")
                messagebox.showinfo("Success", f"Loaded: {filename}\nClick 'Play' to start!")
            except Exception as e:
                messagebox.showerror("Error", f"Could not load audio file:\n{e}")

    def play_song(self):
        if self.current_file:
            if self.is_paused:
                pygame.mixer.music.unpause()
                self.is_paused = False
            else:
                pygame.mixer.music.play(-1)  # Loop playback
                self.is_playing = True
                self.update_visualizer()
            
            self.play_btn.config(state="disabled")
            self.pause_btn.config(state="normal")

    def pause_song(self):
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_paused = True
            self.play_btn.config(state="normal")
            self.pause_btn.config(state="disabled")

    def stop_song(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False
        self.canvas.delete("all")
        self.play_btn.config(state="normal")
        self.pause_btn.config(state="disabled")

    def change_volume(self, val):
        volume = float(val)
        pygame.mixer.music.set_volume(volume)

    def update_visualizer(self):
        if not self.is_playing or self.is_paused:
            return

        self.canvas.delete("all")
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width < 10:
            canvas_width = 800
        if canvas_height < 10:
            canvas_height = 280

        bar_width = max(4, (canvas_width // self.bars) - 5)

        try:
            for i in range(self.bars):
                # Dynamic reactive animation synced with music playback ticks
                import random
                factor = random.uniform(0.3, 1.0)
                level = int(abs(np.sin(i + pygame.mixer.music.get_pos() * 0.015)) * (canvas_height * 0.65) * factor)
                
                x = i * (bar_width + 5) + 15
                y1 = canvas_height - level - 10
                y2 = canvas_height - 10
                
                color = self.bar_colors[i % len(self.bar_colors)]
                self.canvas.create_rectangle(x, y1, x + bar_width, y2, fill=color, outline="")
        except Exception:
            pass

        if self.is_playing and not self.is_paused:
            self.root.after(35, self.update_visualizer)

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicVisualizerApp(root)
    root.mainloop()