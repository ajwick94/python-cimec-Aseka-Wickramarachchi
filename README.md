🎧 **ITD-based Sound Localization Experiment**

This is a simple experiment that mimics auditory perception research methods used to measure accuracy in sound localisation and spatial hearing. The idea behind this project was to primarily familiarise myself in building a simple localisation experiment using Python while being able to combine knowledge from psychoacoustics and digital signal processing. It also implements a Just Noticeable Difference (JND) experiment to measure a listener’s sensitivity to spatial audio cues in the horizontal plane. 

🧠 **Background**

<img width="850" height="352" alt="Image" src="https://github.com/user-attachments/assets/5475cac6-a1d3-4701-9abf-598dbb6f1309" />

For normal-hearing listeners (NH), the ability of sound localisation is dependent on binaural cues, such as interaural time differences (ITDs; the difference in arrival timing of the sound signal at each ear) and interaural level differences (ILDs; the difference between the sound pressure levels at each ear). 

* ITD (Interaural Time Difference):
    Time difference in arrival of a sound at each ear, strongest cue for localization at low frequencies.

* ILD (Interaural Level Difference):
    Difference in sound level between ears, stronger cue at high frequencies.

* JND (Just Noticeable Difference):
    The smallest change in ITD that a listener can reliably detect.

Here I have presented a framework for exploring these psychoacoustic phenomena experimentally with the use of a simple ITD manipulation.

📖 **Overview of the Code**

# **generate_ITD.py - class**

* Implements a psychoacoustic model (Woodworth’s ITD model) with fractional delay processing to spatialize audio over headphones.

* Simulates ITDs based on average head radius and speed of sound. 

* Applies simple ILDs to mimic natural level differences between ears.

* Can generate and play test tones or save stereo signals as WAV files.


# **jnd_experiment.py - class**

* Use this script to run the 2-Alternative Forced Choice (2AFC) psychophysics experiment:
    Participant will hear two sounds (one centered, one shifted by an angle).

* Task: identify which sound was further to the left.

* Uses an adaptive staircase procedure to adjust the level of difficulty.

* Logs responses, tracks reversals, and plots localization performance of the participant in each trial.


🛠️ **Installation of Dependencies**

pip install numpy scipy matplotlib sounddevice

⚠️ **Note:**
A working sound output device (headphones are much recommended 🎧) is required.


💭 **Possible Future Implementations**

* Addition of head-related transfer functions (HRTFs) with datasets containing acoustically measured or numerically simulated HRTFs for specific individuals (individualised HRTFs) or standardized models (generic HRTFs) which are used to simulate spatial audio experiences by filtering sound based on a listener's unique head and ear geometry. (Eg: SONICOM Dataset)
  
* GUI for running perceptual tests, possible implementation with psychopy.
  
* Exporting data from participants for psychometric function fitting and further analysis.




