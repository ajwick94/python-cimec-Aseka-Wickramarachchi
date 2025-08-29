import numpy as np
import sounddevice as sd
from scipy.io import wavfile
import os


class generate_ITD:
    """
    In order to localise the position of a sound source in the azimuth
    (horizontal plane) the auditory system employs ITDs(ILDs as well). Here we
    simulate the source motion using changes to ITDs and fractional sampling 
    to make shifts that are audible on headphones
    
    """
    #Initialisation
    
    def __init__(self, sample_rate=44100, avg_head_r = 0.0875, speed_of_sound = 343.0):
        self.sample_rate = sample_rate
        self.avg_head_r = avg_head_r
        self.speed_of_sound = speed_of_sound
        
    # The Psychoacoustic Model: 
    def woodworth_model(self, angle_deg):
        
        """
        The Woodworth model simplifies interaural time difference (ITD) 
        using a rigid, spherical head approximation where sound travels as a 
        plane wave. The formula for calculating the ITD is τ = (r/c) * (θ + sin(θ)), 
        where 'r' is the head radius, 'c' is the speed of sound, and 'θ' is 
        the sound source's azimuth in radians measured from the frontal hemifield. 
        This equation describes the extra path the sound takes 
        around the sphere to reach the "occluded" (far) ear, but it needs 
        different forms depending on the source's angular position relative 
        to the ears.  
        
        """
        theta = np.radians (angle_deg)
        theta_c = np.clip(theta, -np.pi/2, np.pi/2) #Here theta is clamped since we are only concerned about localisation in the frontal hemifield -90 to +90. This prevents sounds appearing from behind the head.
        it_d = (self.avg_head_r / self.speed_of_sound) * (theta_c + np.sin(theta_c)) #calculate the ITD
        return float(it_d)
    
    def simple_ild(self, angle_deg, max_ild =6.0):
        
        """
        Here we introduce a simple, frequency-independent ILD adjustment which 
        is optional since we are more concerned with ITDs.
        A positive angle = source is towards the right hemifield (also the 
        sound pressure level higher in the right ear).
        
        """
    
        return np.clip((angle_deg/90.0) * max_ild, -max_ild, max_ild)
        
      
    
    # DSP to simulate angular shifts in time
    
    def fractional_shift (self, x, sample_shift):
        
        """
        1D signal is shifted by a fractional (possibly negative) number of samples. 
        Positive shift = delay (moves signal to the right).
        Uses linear interpolation + zero padding. 
        Preserves length, avoids wraparound.
        
        """
        n = len(x)
        t = np.arange(n)
        t_src = t - sample_shift
        
        y = np.interp(t_src, t, x, left=0.0, right =0.0) #linear interpolation allows us to prevent the signal from having warps or artifacts while preserving the signal length.
        return y
    
    def apply_itd(self, mono_signal, angle_deg, use_ild = True):
        
        """
        Apply ITD (and a simple ILD manipulation to the mono signal; 
        returns a [N, 2] stereo. Here we have used the convention that
        positive angle = source to RIGHT. 
        We implement this by advancing the right or delaying the left. This can
        be done by splitting the interaural time delay symmetrically: 
        left delayed by +d/2, right by -d/2.
        
        """
        mono_sound = np.asarray(mono_signal, dtype = float)
        itd_sec = self.woodworth_model(angle_deg)
        d_samples = itd_sec * self.sample_rate
        
        #interaural delat is split equally to presever global onset of the sound.
        shift_left = +0.5 * abs(d_samples)
        shift_right = -0.5 * abs(d_samples)
        
        if angle_deg >= 0:
            #Source position to the right while left is delayed
            
            left = self.fractional_shift(mono_sound, +shift_left)
            right = self.fractional_shift(mono_sound, +shift_right)
            
        else:
            #Source position to the left while right is delayed
            left = self.fractional_shift(mono_sound, +shift_right)
            right = self.fractional_shift(mono_sound, +shift_left)
            
        
        #This is a simple ILD manipulation/ (optional)
        if use_ild:
            ild = self.simple_ild(angle_deg)
            
            increase_R = 10 ** ( (+ild / 20.0) / 2.0)
            increase_L = 10 ** ((-ild / 20.0 )/ 2.0)
            right *= increase_R
            left *= increase_L
            
            
            stereo_signal = np.column_stack([left,right])
            
            #Apply peak normalisation in order to avoid clipping and preserve ILD cues.
            peak_norm = np.max(np.abs(stereo_signal))
            if peak_norm > 1.0:
                stereo_signal = stereo_signal / peak_norm
            return stereo_signal
        
    
    #Generate a simple test tone, play and save the sound stimuli as a wavfile.
    def play_test_tone (self, freq = 750, duration = 0.2):
        
        """For our JND experiments we require a controlled sound stimulus. 
        First we Generate a sine wave of chosen frequency and duration. It is better to use frequencies below 1200 Hz for ITDs.
        Here we use f = 750 and t = 0.2 seconds.
        Then a 10 ms cosine ramp is added ( a slight fade-in/out effect) to avoid clicks in the tone generated. 
        The sound stimulus is returned as an array."""
        
        n = int(self.sample_rate * duration)
        t = np.arange(n) / self.sample_rate
        t_tone = np.sin(2* np.pi * freq * t )
        
        #Here we apply an on/off ramp of about 10ms
        ramp_x = 0.01
        ramp_y = max(1, int(self.sample_rate * ramp_x))
        window = np.ones(n)
        ramp_val = 0.5 * (1 - np.cos(np.linspace(0, np.pi, ramp_y)))
        window [:ramp_y] *= ramp_val
        window[-ramp_y:] *= ramp_val[::-1]
        
        return t_tone * window
    
    def tt_playback (self, stereo_signal):
        """ Playback of the test tone"""
        
        stereo_signal = np.asarray(stereo_signal, dtype=float)
        
        if stereo_signal.ndim != 2 or stereo_signal.shape[1] !=2:
            raise ValueError("Input signal should be in stereo (Nx2)")
        sd.play(stereo_signal, self. sample_rate, blocking=True)
        
    
    def save_soundfile (self, stereo_signal, filename):
        """Save the generated tone to the directory"""
        os.makedirs(os.path.dirname(filename) or ".", exist_ok =True)
        x = np.asarray(stereo_signal, dtype=float)
        peak_norm = np.max(np.abs(x))
        if peak_norm > 0:
            x = x / peak_norm * 0.95 #here we have multiplied the normalisation by 0.95 to leave "headroom". This avoids the loudest parts of the sound being too harsh (distorted or clipping) while maintaining the signal at a safe level.
        wavfile.write(filename, self.sample_rate, (x * 32767).astype(np.int16))
        
        
        
        
