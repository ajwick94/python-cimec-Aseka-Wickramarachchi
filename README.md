🎧 ITD-based Sound Localization Experiment

This project simulates sound localization cues using Interaural Time Difference (ITD) and a simple Interaural Level Difference (ILD) model. It also implements a Just Noticeable Difference (JND) experiment to measure a listener’s sensitivity to spatial audio cues in the horizontal plane. Using plotting functions, participant performance in each trial is updated.

This is a simple experiment that mimics auditory perception research methods used to measure accuracy in sound localisation and spatial hearing. The idea behind this project was to primarily familiarise myself in building a simple localisation experiment using Python while being able to combing knowdledge from psychoacoustics and digital signal processing. 

📖 Overview

generate_ITD.py - class

Implements a psychoacoustic model (Woodworth’s ITD model) with fractional delay processing to spatialize audio over headphones.
Simulates ITDs based on average head radius and speed of sound.
Applies simple ILDs to mimic natural level differences between ears.
Can generate and play test tones or save stereo signals as WAV files.

jnd_experiment.py - class

Runs a 2-Alternative Forced Choice (2AFC) psychophysics experiment:
Participant hears two sounds (one centered, one shifted by an angle).
Task: identify which sound was further to the left.
Uses an adaptive staircase procedure to adjust difficulty.
Logs responses, tracks reversals, and plots localization performance.

🛠️ Installation

Install dependencies:
pip install numpy scipy matplotlib sounddevice

⚠️ Note:
A working sound output device (headphones are much recommended 🎧) is required.
sounddevice may require additional backend libraries depending on your OS.


