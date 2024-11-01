import tkinter as tk
from tkinter import ttk, filedialog
import time
import threading
import os
import pygame

class PomodoroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicación Pomodoro")
        self.root.geometry("400x300")
        self.running = False
        self.timer_thread = None

        # Variables de configuración
        self.focus_time = tk.IntVar(value=25)
        self.short_break_time = tk.IntVar(value=5)
        self.long_break_time = tk.IntVar(value=15)
        self.cycles = tk.IntVar(value=4)
        self.current_cycle = 0
        self.remaining_time = 0
        self.alarm_sound = "alarm.wav"

        # Inicializar pygame para reproducir sonido
        pygame.mixer.init()

        # Crear la interfaz
        self.setup_ui()

    def setup_ui(self):
        # Estilo de la interfaz
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 12), padding=10)
        style.configure("TLabel", font=("Helvetica", 12))

        # Frame para los ajustes
        settings_frame = ttk.LabelFrame(self.root, text="Ajustes")
        settings_frame.pack(pady=10, padx=10, fill="x")

        # Ajustes de tiempos
        ttk.Label(settings_frame, text="Tiempo de concentración (min):").grid(row=0, column=0, sticky="w")
        ttk.Entry(settings_frame, textvariable=self.focus_time, width=5).grid(row=0, column=1)

        ttk.Label(settings_frame, text="Descanso corto (min):").grid(row=1, column=0, sticky="w")
        ttk.Entry(settings_frame, textvariable=self.short_break_time, width=5).grid(row=1, column=1)

        ttk.Label(settings_frame, text="Descanso largo (min):").grid(row=2, column=0, sticky="w")
        ttk.Entry(settings_frame, textvariable=self.long_break_time, width=5).grid(row=2, column=1)

        ttk.Label(settings_frame, text="Número de ciclos:").grid(row=3, column=0, sticky="w")
        ttk.Entry(settings_frame, textvariable=self.cycles, width=5).grid(row=3, column=1)

        # Botones de control
        control_frame = ttk.Frame(self.root)
        control_frame.pack(pady=10)

        self.start_button = ttk.Button(control_frame, text="Iniciar", command=self.start_timer)
        self.start_button.grid(row=0, column=0, padx=5)

        self.pause_button = ttk.Button(control_frame, text="Pausar", command=self.pause_timer, state=tk.DISABLED)
        self.pause_button.grid(row=0, column=1, padx=5)

        self.reset_button = ttk.Button(control_frame, text="Restablecer", command=self.reset_timer)
        self.reset_button.grid(row=0, column=2, padx=5)

        self.sound_button = ttk.Button(control_frame, text="Cambiar sonido", command=self.change_sound)
        self.sound_button.grid(row=0, column=3, padx=5)

        # Etiqueta para mostrar el tiempo restante
        self.timer_label = ttk.Label(self.root, text="00:00", font=("Helvetica", 24))
        self.timer_label.pack(pady=10)

    def start_timer(self):
        if not self.running:
            self.running = True
            self.start_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL)
            self.current_cycle = 0
            self.run_cycle()

    def run_cycle(self):
        if self.current_cycle < self.cycles.get():
            self.remaining_time = self.focus_time.get() * 60
            self.update_timer()
            self.current_cycle += 1
        else:
            self.remaining_time = self.long_break_time.get() * 60
            self.update_timer()

    def update_timer(self):
        if self.remaining_time > 0 and self.running:
            mins, secs = divmod(self.remaining_time, 60)
            self.timer_label.config(text=f"{mins:02}:{secs:02}")
            self.remaining_time -= 1
            self.root.after(1000, self.update_timer)
        elif self.remaining_time == 0 and self.running:
            self.play_alarm()
            if self.current_cycle < self.cycles.get():
                self.remaining_time = self.short_break_time.get() * 60
                self.update_timer()
            else:
                self.reset_timer()

    def pause_timer(self):
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)

    def reset_timer(self):
        self.running = False
        self.current_cycle = 0
        self.timer_label.config(text="00:00")
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)

    def change_sound(self):
        file_path = filedialog.askopenfilename(title="Seleccionar sonido", filetypes=[("Archivos WAV", "*.wav")])
        if file_path:
            self.alarm_sound = file_path

    def play_alarm(self):
        if os.path.exists(self.alarm_sound):
            pygame.mixer.music.load(self.alarm_sound)
            pygame.mixer.music.play()
        else:
            print("Archivo de sonido no encontrado.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroApp(root)
    root.mainloop()
