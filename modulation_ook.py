import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import butter, lfilter

# Input parameters
F1 = int(input('Enter the frequency of carrier: '))
F2 = int(input('Enter the frequency of pulse: '))
A = 3  # Amplitude
t = np.arange(0, 1, 0.001)

# Generating the carrier signal
x = A * np.sin(2 * np.pi * F1 * t)

# Generating the square wave pulses
u = []
b = [0.2, 0.4, 0.6, 0.8, 1.0]
s = 1
for i in t:
    if i == b[0]:
        b.pop(0)
        if s == 0:
            s = 1
        else:
            s = 0
    u.append(s)

# Generating the ASK signal
v = A * np.sin(2 * np.pi * F1 * t) * np.array(u)

# Demodulation function
def demodulate_ask(signal, threshold):
    # Rectify the signal
    rectified_signal = np.abs(signal)
    
    # Apply thresholding to extract binary signal
    binary_signal = [1 if sample > threshold else 0 for sample in rectified_signal]
    
    return binary_signal

def rectified(signal):
    rectified_signal = np.abs(signal)
    return rectified_signal

def butter_lowpass_filter(data, cutoff, fs, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = lfilter(b, a, data)
    return y

# Demodulating the ASK signal
threshold = 2.5  # Adjust this threshold as needed
binary_signal = rectified(v)
cutoff_frequency = 5  # Adjust cutoff frequency as needed
fs = 1000  # Sample rate
order = 6  # Filter order
filtered_signal = butter_lowpass_filter(binary_signal, cutoff_frequency, fs, order)

# Demodulated signal
demodulated_signal = [1 if filtered_signal[i] > filtered_signal[i-1] else 0 for i in range(1, len(filtered_signal))]
demodulated_signal = [0] + demodulated_signal  # Add the first element as 0

# Plotting all signals
plt.figure(figsize=(12, 10))

# Carrier signal
plt.subplot(321)
plt.plot(t, x)
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.title('Carrier Signal')
plt.grid(True)

# Square wave pulses
plt.subplot(322)
plt.plot(t, u)
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.title('Square Wave Pulses')
plt.grid(True)

# ASK signal
plt.subplot(323)
plt.plot(t, v)
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.title('ASK Signal')
plt.grid(True)

# Rectified signal
plt.subplot(324)
plt.plot(t, binary_signal, color='orange')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.title('Rectified Signal')
plt.grid(True)

# Low-pass filtered signal
plt.subplot(325)
plt.plot(t, filtered_signal, color='green')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.title('Low-pass Filtered Signal')
plt.grid(True)

# Demodulated signal
plt.subplot(326)
plt.plot(t, demodulated_signal, color='blue')
plt.xlabel('Time')
plt.ylabel('Binary Signal')
plt.title('Demodulated Signal (1 for increasing part, 0 for decreasing part)')
plt.grid(True)

plt.tight_layout()
plt.show()
