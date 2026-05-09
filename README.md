cat > /mnt/storage/app_projects/vinlizer/README.md << 'EOF'
# 🎵 Vinlizer Studio

**Professional System-Wide Audio Equalizer for Linux**

![Vinlizer](https://img.shields.io/badge/Vinlizer-Studio-%2314b8a6?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square)
![Linux](https://img.shields.io/badge/Linux-Debian%20%7C%20Ubuntu%20%7C%20Parrot-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

Built by [Vinnius Mbuthia](https://vinnius-portfolio-4bcd.vercel.app/) | [TechGlobal](https://github.com/Vinnias-3)

---

## 📸 Screenshot
┌─────────────────────────────────────────────────┐
│ 🎵 Vinlizer Studio │
│ Professional System-Wide Equalizer │
│ │
│ 🎧 Active 🔊 Bass Boost: ████░░ 8dB │
│ 🌐 Surround: ██░░░░ 30% │
│ │
│ 🎛️ Studio Presets │
│ [🎸 Bass Boost] [🔊 Deep Bass] [🎤 Vocal] │
│ [🤘 Rock] [💀 Metal] [🎧 HipHop] [🪩 EDM] │
│ [🎮 Gaming] [🎬 Cinema] [🎻Acoustic] [📢 Loud]│
│ │
│ 🎚️ 15-Band Equalizer │
│ 50Hz: ████░░░░░░░ +8dB │
│ 100Hz: ███░░░░░░░░ +6dB │
│ ... │
└─────────────────────────────────────────────────┘

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎛️ **15-Band EQ** | Full control from 50Hz to 10kHz |
| 🔊 **Bass Boost** | 0-20dB variable bass enhancement |
| 🌐 **3D Surround** | 0-100% stereo widening |
| 🎸 **16 Presets** | Bass Boost, Rock, Metal, Hip Hop, EDM, Gaming, Cinema, Jazz, Podcast & more |
| ⚡ **Instant Apply** | Native PipeWire + LADSPA engine — no external apps |
| 🎧 **System-Wide** | Affects ALL audio — browsers, music players, games, everything |
| 💾 **Custom Presets** | Save and load your own EQ curves |
| 🎨 **Dark Theme** | Professional studio-inspired dark UI |
| 🐧 **Linux Native** | Built for Debian/Ubuntu/Parrot OS |

---

## 🚀 Quick Install

```bash
# Clone the repository
git clone https://github.com/Vinnias-3/vinlizer.git
cd vinlizer

# Install system dependencies
sudo apt update
sudo apt install -y ladspa-sdk swh-plugins python3-tk python3-pip

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate

# Launch Vinlizer Studio
python3 vinlizer.py
🎹 Presets Guide
Preset	Best For	Sound Profile
🎸 Bass Boost	Hip-hop, EDM, trap	Heavy low-end punch
🔊 Deep Bass	Sub-bass music, dubstep	Earthquake subwoofer
🎤 Vocal Clarity	Podcasts, audiobooks, lectures	Crystal clear voices
🗣️ Voice Boost	Video calls, meetings	Enhanced speech presence
🤘 Rock Guitar	Rock, alternative, indie	Mid-range crunch
💀 Metal	Metal, hardcore, thrash	Aggressive guitar tone
🎧 Hip Hop/Trap	Rap, trap, R&B	808-heavy with crisp highs
🪩 EDM/Dance	Electronic, house, techno	Club-ready sound
🎮 Gaming FPS	First-person shooters	Footstep clarity
🎬 Cinema/Movie	Films, Netflix, YouTube	Surround experience
🎻 Acoustic	Folk, classical, jazz	Natural instrument tone
🎙️ Podcast	Spoken word, radio	Broadcast-quality voice
✨ Treble Boost	Detail listening	Airy, bright highs
🎷 Warm Jazz	Jazz, blues, soul	Smooth, rich warmth
📢 Loudness	Low-volume listening	Full sound at any level
🪕 Flat	Reference / bypass	No EQ applied
🔧 How It Works
Vinlizer uses PipeWire's LADSPA module to insert a 15-band equalizer (mbeq_1197) directly into your system's audio pipeline. No external apps run. Sliders write directly to the PipeWire graph.

text
Audio Source → PipeWire → [Vinlizer LADSPA EQ] → Speakers/Headphones
                (Browser,           (Real-time
                 Spotify,           15-band
                 Games)             processing)
📋 Requirements
OS: Debian / Ubuntu / Parrot OS / Kali (any Debian-based Linux)

Audio: PipeWire or PulseAudio

Python: 3.8 or higher

Packages: ladspa-sdk swh-plugins python3-tk
🛠️ Troubleshooting
Problem	Solution
No sound after closing Vinlizer	Run: pactl set-default-sink @DEFAULT_SINK@
EQ not affecting audio	Ensure Vinlizer is the default sink: pactl set-default-sink vinlizer_eq
Module fails to load	Install LADSPA: sudo apt install ladspa-sdk swh-plugins
GUI won't open	Install tkinter: sudo apt install python3-tk
🗺️ Roadmap
Convolution reverb engine

Compressor/limiter

System tray minimize

Auto-start on boot

Flatpak package

VST plugin support

👤 Author
Vinnius Mbuthia Njuguna

🌐 Portfolio: vinnius-portfolio-4bcd.vercel.app

🐙 GitHub: github.com/Vinnias-3

📧 Email: techglobal824@gmail.com

📱 WhatsApp: +254 748 702 891

📍 Makutano, Embu County, Kenya

📄 License
MIT License — Build, modify, share freely. Built with ❤️ in Kenya.

"If it can be equalized, Vinlizer can do it."
EOF

Push the README
cd /mnt/storage/app_projects/vinlizer
git add README.md
git commit -m "Added comprehensive README with install guide and presets"
git push origin main

Paste the output. This README has:
- Badges (version, Python, Linux, license)
- Feature table
- Quick install commands
- Full presets guide with descriptions
- Architecture diagram
- Troubleshooting table
- Roadmap
- Author contact

It will look professional on your GitHub repo.
