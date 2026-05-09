#!/usr/bin/env python3
"""
Vinlizer Studio - Professional System-Wide Audio Equalizer
Native PipeWire + LADSPA Engine | 15-Band + Bass Boost + 3D Surround
Built by Vinnius Mbuthia | TechGlobal
"""
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import subprocess, os, json, time

FREQUENCIES = [50, 100, 156, 220, 311, 440, 622, 880, 1250, 1750, 2500, 3500, 5000, 7000, 10000]
BAND_LABELS = ["50Hz","100Hz","156Hz","220Hz","311Hz","440Hz","622Hz","880Hz","1.25k","1.75k","2.5k","3.5k","5k","7k","10k"]
BAND_COLORS = ["#422006","#713f12","#854d0e","#a16207","#ca8a04","#eab308","#65a30d","#16a34a","#0891b2","#2563eb","#4f46e5","#7c3aed","#a21caf","#db2777","#e11d48"]
PRESETS_DIR = os.path.expanduser("~/.config/vinlizer/presets")
MODULE_ID_FILE = os.path.expanduser("~/.config/vinlizer/module_id")

# Studio-grade presets — tuned for maximum impact
STUDIO_PRESETS = {
    "flat":           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "bass_boost":     [16, 15, 13, 10, 7, 4, 2, 0, -1, -2, -2, -1, 0, 1, 2],
    "deep_bass":      [18, 17, 15, 12, 8, 5, 2, -1, -3, -4, -4, -3, -2, 0, 1],
    "vocal_clarity":  [-10, -8, -6, -3, 0, 3, 7, 10, 12, 11, 9, 6, 3, 1, -1],
    "voice_boost":    [-8, -6, -3, 0, 4, 8, 10, 12, 10, 7, 4, 1, -2, -4, -5],
    "rock_guitar":    [10, 8, 5, 1, -3, -5, -3, 1, 5, 8, 10, 8, 5, 3, 1],
    "metal":          [12, 10, 6, 1, -4, -6, -4, 0, 4, 8, 12, 10, 7, 4, 2],
    "hiphop_trap":    [18, 17, 14, 9, 5, 1, -2, -3, 0, 3, 5, 7, 9, 11, 13],
    "edm_dance":      [14, 13, 10, 5, 1, -1, -1, 2, 5, 8, 10, 12, 14, 15, 16],
    "gaming_fps":     [8, 7, 5, 3, 6, 9, 11, 11, 9, 7, 5, 7, 9, 11, 13],
    "cinema_movie":   [10, 8, 6, 3, 1, 0, 2, 4, 6, 5, 4, 6, 8, 10, 12],
    "acoustic":       [5, 6, 7, 6, 4, 2, 1, 2, 3, 4, 5, 4, 3, 2, 1],
    "podcast_spoken": [-6, -4, 0, 4, 8, 10, 8, 6, 4, 2, 0, -2, -4, -6, -8],
    "treble_boost":   [-4, -3, -2, 0, 2, 4, 6, 8, 10, 12, 13, 14, 15, 15, 14],
    "warm_jazz":      [6, 5, 4, 3, 2, 1, 0, 1, 2, 3, 4, 3, 2, 1, 0],
    "loudness":       [8, 7, 5, 3, 2, 1, 0, -1, -1, 0, 1, 3, 5, 7, 9],
}

class VinlizerStudio:
    def __init__(self):
        self.sliders = {}
        self.labels = {}
        self.bands = {label: 0 for label in BAND_LABELS}
        self.module_id = self._get_stored_module_id()
        self.bass_boost_val = 0
        self.surround_val = 0
        
        self.root = tk.Tk()
        self.enabled = tk.BooleanVar(value=True)
        self.bass_boost = tk.IntVar(value=0)
        self.surround = tk.IntVar(value=0)
        
        self.root.title("🎵 Vinlizer Studio - Professional Equalizer")
        self.root.geometry("860x780")
        self.root.configure(bg='#0a0a0f')
        
        self._ensure_loaded()
        self._create_presets()
        self.build_ui()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
    
    def _cmd(self, cmd):
        try:
            r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=3)
            return r.stdout.strip()
        except: return ""
    
    def _get_stored_module_id(self):
        if os.path.exists(MODULE_ID_FILE):
            with open(MODULE_ID_FILE) as f: return f.read().strip()
        return None
    
    def _store_module_id(self, mid):
        os.makedirs(os.path.dirname(MODULE_ID_FILE), exist_ok=True)
        with open(MODULE_ID_FILE, 'w') as f: f.write(str(mid))
        self.module_id = mid
    
    def _ensure_loaded(self):
        if self.module_id:
            stdout = self._cmd(f"pactl list modules short | grep '{self.module_id}'")
            if stdout: return
        
        # Add preamp gain to compensate for EQ cuts
        preamp_gain = max(0, -min(self.bands.values())) * 0.3
        for label in BAND_LABELS:
            self.bands[label] = int(self.bands[label] + preamp_gain)
        # Add preamp gain to compensate for EQ cuts
        preamp_gain = max(0, -min(self.bands.values())) * 0.3
        for label in BAND_LABELS:
            self.bands[label] = int(self.bands[label] + preamp_gain)
        controls = ",".join([str(self.bands[label]) for label in BAND_LABELS])
        cmd = (f'pactl load-module module-ladspa-sink sink_name=vinlizer_eq '
               f'sink_properties=device.description="Vinlizer_Studio" '
               f'master=@DEFAULT_SINK@ plugin=mbeq_1197 label=mbeq control={controls}')
        stdout = self._cmd(cmd)
        if stdout and stdout.isdigit():
            self._store_module_id(stdout)
            self._cmd("pactl set-default-sink vinlizer_eq 2>/dev/null")
    
    def apply_eq(self):
        if not self.enabled.get(): return
        if self.module_id:
            self._cmd(f"pactl unload-module {self.module_id}")
            self.module_id = None
        self._ensure_loaded()
    
    def slider_move(self, band, value):
        val = round(float(value))
        self.bands[band] = val
        self.labels[band].config(text=str(val))
        if hasattr(self, '_debounce_id'): self.root.after_cancel(self._debounce_id)
        self._debounce_id = self.root.after(100, self.apply_eq)
    
    def load_preset(self, name):
        if name in STUDIO_PRESETS:
            vals = STUDIO_PRESETS[name]
            for i, band in enumerate(BAND_LABELS):
                self.bands[band] = vals[i]
                self.sliders[band].set(vals[i])
                self.labels[band].config(text=str(vals[i]))
            self.apply_eq()
    
    def save_preset(self):
        name = simpledialog.askstring("Save Preset", "Preset name:")
        if name:
            path = os.path.join(PRESETS_DIR, f"{name.lower().replace(' ','_')}.json")
            with open(path, 'w') as f: json.dump(self.bands, f, indent=2)
            messagebox.showinfo("Vinlizer", f"Preset '{name}' saved!")
    
    def _create_presets(self):
        os.makedirs(PRESETS_DIR, exist_ok=True)
        for name, vals in STUDIO_PRESETS.items():
            path = os.path.join(PRESETS_DIR, f"{name}.json")
            if not os.path.exists(path):
                data = {BAND_LABELS[i]: vals[i] for i in range(len(BAND_LABELS))}
                with open(path, 'w') as f: json.dump(data, f, indent=2)
    
    def build_ui(self):
        # Header
        h = tk.Frame(self.root, bg='#0a0a0f', pady=8)
        h.pack(fill='x')
        tk.Label(h, text="🎵 Vinlizer Studio", font=("Helvetica", 26, "bold"), fg="#14b8a6", bg='#0a0a0f').pack()
        tk.Label(h, text="Professional System-Wide Equalizer | Native PipeWire Engine", fg="#64748b", bg='#0a0a0f', font=("Helvetica", 9)).pack()
        
        # Master controls
        master = tk.Frame(self.root, bg='#111118', padx=15, pady=10)
        master.pack(fill='x', padx=20, pady=5)
        
        tk.Checkbutton(master, text="🎧 Active", variable=self.enabled, command=self._toggle,
                      fg="#22c55e", bg='#111118', selectcolor='#111118', font=("Helvetica", 11, "bold")).pack(side='left', padx=10)
        
        # Bass Boost knob
        tk.Label(master, text="🔊 Bass Boost:", fg="#f59e0b", bg='#111118', font=("Helvetica", 10, "bold")).pack(side='left', padx=(20,5))
        bb = ttk.Scale(master, from_=0, to=20, variable=self.bass_boost, length=120,
                      command=lambda v: self._set_bass_boost(int(float(v))))
        bb.pack(side='left', padx=5)
        self.bb_label = tk.Label(master, text="0dB", fg="#f59e0b", bg='#111118', font=("Helvetica", 9))
        self.bb_label.pack(side='left')
        bb.set(0)
        
        # Surround
        tk.Label(master, text="🌐 Surround:", fg="#7c3aed", bg='#111118', font=("Helvetica", 10, "bold")).pack(side='left', padx=(20,5))
        sr = ttk.Scale(master, from_=0, to=100, variable=self.surround, length=120,
                      command=lambda v: self._set_surround(int(float(v))))
        sr.pack(side='left', padx=5)
        self.sr_label = tk.Label(master, text="0%", fg="#7c3aed", bg='#111118', font=("Helvetica", 9))
        self.sr_label.pack(side='left')
        sr.set(0)
        
        # Presets Grid
        pf = tk.LabelFrame(self.root, text="🎛️ Studio Presets", fg="#14b8a6", bg='#111118',
                           font=("Helvetica", 11, "bold"), padx=10, pady=10)
        pf.pack(fill='x', padx=20, pady=5)
        
        preset_btns = [
            ("🎸 Bass Boost", "bass_boost", "#854d0e"),
            ("🔊 Deep Bass", "deep_bass", "#713f12"),
            ("🎤 Vocal Clarity", "vocal_clarity", "#2563eb"),
            ("🗣️ Voice Boost", "voice_boost", "#0891b2"),
            ("🤘 Rock Guitar", "rock_guitar", "#dc2626"),
            ("💀 Metal", "metal", "#991b1b"),
            ("🎧 Hip Hop/Trap", "hiphop_trap", "#7c3aed"),
            ("🪩 EDM/Dance", "edm_dance", "#a21caf"),
            ("🎮 Gaming FPS", "gaming_fps", "#f59e0b"),
            ("🎬 Cinema/Movie", "cinema_movie", "#d97706"),
            ("🎻 Acoustic", "acoustic", "#16a34a"),
            ("🎙️ Podcast", "podcast_spoken", "#64748b"),
            ("✨ Treble Boost", "treble_boost", "#db2777"),
            ("🎷 Warm Jazz", "warm_jazz", "#ca8a04"),
            ("📢 Loudness", "loudness", "#eab308"),
            ("🪕 Flat", "flat", "#475569"),
        ]
        btn_row, btn_col = 0, 0
        for name, preset, color in preset_btns:
            tk.Button(pf, text=name, bg=color, fg="white", font=("Helvetica", 9, "bold"),
                     padx=10, pady=6, cursor="hand2", relief="flat",
                     command=lambda p=preset: self.load_preset(p)).grid(row=btn_row, column=btn_col, padx=4, pady=4, sticky='ew')
            btn_col += 1
            if btn_col > 3: btn_col = 0; btn_row += 1
        
        # EQ Sliders
        eq = tk.LabelFrame(self.root, text="🎚️ 15-Band Graphic Equalizer", fg="#14b8a6", bg='#111118',
                           font=("Helvetica", 12, "bold"), padx=15, pady=10)
        eq.pack(fill='both', expand=True, padx=20, pady=5)
        
        for i, band in enumerate(BAND_LABELS):
            frame = tk.Frame(eq, bg='#111118')
            frame.pack(fill='x', pady=1)
            
            lbl = tk.Label(frame, text="0", fg=BAND_COLORS[i], bg='#111118', font=("Helvetica", 8, "bold"), width=4)
            lbl.pack(side='left', padx=(0,5))
            self.labels[band] = lbl
            
            s = ttk.Scale(frame, from_=-20, to=20, length=500, value=0,
                         command=lambda v, b=band: self.slider_move(b, v))
            s.pack(side='left', padx=5)
            self.sliders[band] = s
            
            tk.Label(frame, text=band, fg="#94a3b8", bg='#111118', font=("Helvetica", 8), width=6, anchor='e').pack(side='left')
        
        # Bottom
        bot = tk.Frame(self.root, bg='#0a0a0f', padx=20, pady=10)
        bot.pack(fill='x')
        tk.Button(bot, text="💾 Save Preset", command=self.save_preset, bg="#14b8a6", fg="#0f172a",
                 font=("Helvetica", 10, "bold"), padx=15, pady=8, cursor="hand2").pack(side='left', padx=5)
        tk.Button(bot, text="🔄 Reset Flat", command=lambda: self.load_preset("flat"), bg="#334155",
                 fg="#e2e8f0", font=("Helvetica", 10), padx=15, pady=8, cursor="hand2").pack(side='left', padx=5)
        
        self.status_lbl = tk.Label(self.root, text="✅ Vinlizer Studio Ready", fg="#22c55e", bg='#111118', font=("Helvetica", 9), pady=5)
        self.status_lbl.pack(fill='x')
    
    def _set_bass_boost(self, val):
        self.bb_label.config(text=f"{val}dB")
        # Boost low frequencies (first 5 bands)
        boost_curve = [val, val*0.9, val*0.7, val*0.4, val*0.15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i, band in enumerate(BAND_LABELS):
            self.bands[BAND_LABELS[i]] = int(boost_curve[i])
            self.sliders[BAND_LABELS[i]].set(int(boost_curve[i]))
            self.labels[BAND_LABELS[i]].config(text=str(int(boost_curve[i])))
        self.apply_eq()
    
    def _set_surround(self, val):
        self.sr_label.config(text=f"{val}%")
        # Widen stereo image by boosting highs on opposite sides
        spread = int(val / 10)
        for i, band in enumerate(BAND_LABELS):
            if i >= 8:  # High frequencies
                self.bands[BAND_LABELS[i]] = spread
                self.sliders[BAND_LABELS[i]].set(spread)
                self.labels[BAND_LABELS[i]].config(text=str(spread))
        self.apply_eq()
    
    def _toggle(self):
        if self.enabled.get():
            self.apply_eq()
            self.status_lbl.config(text="✅ Vinlizer Studio Active", fg="#22c55e")
        else:
            if self.module_id:
                self._cmd(f"pactl unload-module {self.module_id}")
                self.module_id = None
            self.status_lbl.config(text="⏸️ Bypassed - Direct Audio", fg="#f59e0b")
    
    def _on_close(self):
        self.root.destroy()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    VinlizerStudio().run()
