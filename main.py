import sounddevice as sd
import numpy as np
import time

# Define recording parameters
fs = 44100  # Sample rate
duration = 0.5  # Recording duration in seconds
channels = 1

# start recording
recording = sd.rec(int(fs * duration), samplerate=fs, channels=channels)

# record audio in a loop
t_end = time.time() + 10
max_decibel = 0
sum = 0
i = 0

while time.time() < t_end:    
    recording = sd.rec(int(fs * duration), samplerate=fs, channels=channels)
    sd.wait(0.1)
    # Calculate RMS of audio
    rms = np.sqrt(np.mean(recording**2))
    # Calculate noise pollution level in decibels using a reference SPL of 20 micro pascals
    noise_level = 20 * np.log10(rms / 2e-5)
    # check if noise level is negative
    if noise_level < 0:
        noise_level = 0
    print("Noise pollution level: {:.2f} dB".format(noise_level))
    max_decibel = max(max_decibel,noise_level)
    sum += noise_level
    i += 1
    
print("Maximum Noise pollution level: {:.2f} dB".format(max_decibel))
print("Average Noise pollution level: {:.2f} dB".format(sum/i))


