import random
import time
import numpy as np
import matplotlib.pyplot as plt
from itd_generate import generate_ITD

class jnd_experiment:
    
    """
    Just Noticeable Difference experiments using ITDs
    are conducted to determine the smallest detectable changes in the 
    time difference between sounds reaching the two ears, 
    which helps us understand the precision of the auditory system's 
    sound localization ability and how this sensitivity changes with 
    factors such as frequency, enabling the design of 
    hearing aids and analysis of spatial hearing.
    
    """ 
    
    def __init__ (self, max_trials = 10, start_angle = 10.0, min_angle = 0.0, max_angle = 90.0):
        self.generator = generate_ITD()
        self.tone = self.generator.play_test_tone(duration = 0.2)
        
        #staircase param
        self.angle  = start_angle
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.max_trials = max_trials
        
        self.correct_streak  = 0
        self.reversals = 0
        self.last_direction = None
        
        #log
        self.history_angle = []
        self.history_correct = []
        
        #plotting performance in each trial
        plt.ion()
        self.fig, self.ax = plt.subplots(figsize=(8,4))
        self.line, = self.ax.plot([],[],'-o', label = 'angle mag in deg')
        self.scatter = None
        self.ax.set_xlabel('Trial')
        self.ax.set_ylabel('diff in angle')
        self.ax.set_title ('Localisation Perfromance in each Trial')
        self.ax.legend()
        self.ax.set_ylim(0, max_angle * 1.1)
        
    def trial_run(self):
        
    """Here we run the experiment as a 2 Alternative-Forced-Choice Trial"""
        
        target_angle = random.choice([-1,1]) * self.angle
        
        
        order = random.choice ([0, 1])
        if order == 0:
            sound_a = self.generator.apply_itd(self.tone, 0)
            sound_b = self.generator.apply_itd(self.tone, target_angle)
            correct_response = '2' if target_angle < 0 else '1'
        else:
            sound_a = self.generator.apply_itd(self.tone, target_angle)
            sound_b = self.generator.apply_itd(self.tone, 0)
            correct_response = '1' if target_angle <0 else '2'
            
        
        print ("\nPlaying the first sound...")
        self.generator.tt_playback(sound_a)
        time.sleep(0.4)
        print("\nPlaying the second sound...")
        self.generator.tt_playback(sound_b)
        time.sleep(0.2)
        
        
        #Get responses from the participant 
        pp_response = input (" Which sound did you perceive as further to your left? 1 = first 2 = second: ").strip()
        if pp_response not in ["1", '2']:
            print("Invalid Response")
            is_correct = False
        else:
            is_correct = (pp_response == correct_response)
            
        
        #Updating the Adaptive Staricase
        if is_correct:
            self.correct_streak += 1
            if self.correct_streak >=2:
                self.adjust_angle (difficulty = False) 
                
        #Logging of the history of target angles and correct responses
        self.history_angle.append(target_angle)
        self.history_correct.append(is_correct)
        
        #Update the plot
        self.update_plot()
        
        return is_correct, target_angle
        
    def adjust_angle (self, difficulty):
        old_angle = self.angle
        if difficulty:
            self.angle = max(self.min_angle, self.angle * 0.8)
            new_direction = 'down'
        
        else:
            self.angle = min(self.max_angle, self.angle * 1.25)
            new_direction = 'up'
        
    #Count the change of directions
        if self.last_direction and new_direction != self.last_direction:
            self.reversals += 1
        self.last_direction = new_direction
        print(f"Adjusting difficulty: angle {old_angle:.2f}° → {self.angle:.2f}°")
    
    def run(self):
        print("Localisation Experiment")
        print("Please use headphones for this experiment. Identify out of the two sounds presented which was further to your LEFT. Respond whether it's the first or second")

        trial = 0
        while trial < self.max_trials and self.reversals < 10:
            correct, angle = self.trial_run()
            print(f"Trial {trial+1}: {'✓ Correct' if correct else '✗ Incorrect'} (angle {angle:.2f}°)")
            trial += 1

        print("\nExperiment is now complete.")
        plt.ioff()
        plt.show()
        return self.history_angle, self.history_correct

    def update_plot(self):
        trials = np.arange(1, len(self.history_angle)+1)
        abs_angles = np.abs(self.history_angle)

        self.line.set_data(trials, abs_angles)
        if self.scatter:
            self.scatter.remove()

        colors = ["green" if c else "red" for c in self.history_correct]
        self.scatter = self.ax.scatter(trials, abs_angles, c=colors, s=60, zorder=3)

        self.ax.set_xlim(0, len(trials)+1)
        self.ax.figure.canvas.draw()
        self.ax.figure.canvas.flush_events()


if __name__ == "__main__":
    exp = jnd_experiment(max_trials=10)
    exp.run()
    
    
        
    
            
        
