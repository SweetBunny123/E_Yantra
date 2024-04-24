import numpy as np
import sounddevice as sd
import soundfile as sf

# Parameters
bit_rate = 10  # Bit rate in bits per second
carrier_freq = 1000  # Carrier frequency in Hertz
duration = 5  # Duration of the signal in seconds

# Function to generate binary data
def generate_binary_data(duration, bit_rate):
    num_bits = int(duration * bit_rate)
    data = np.random.randint(0, 2, num_bits)
    return data

# Function to modulate binary data using OOK
def modulate_OOK(binary_data, carrier_freq, duration, fs):
    t = np.linspace(0, duration, duration * fs, endpoint=False)
    carrier_wave = np.sin(2 * np.pi * carrier_freq * t)

    modulated_signal = []
    for bit in binary_data:
        if bit == 1:
            modulated_signal.extend(carrier_wave)
        else:
            modulated_signal.extend(np.zeros(len(carrier_wave)))

    return np.array(modulated_signal)

# Function to demodulate OOK-modulated signal
def demodulate_OOK(modulated_signal, carrier_freq, duration, fs, bit_rate):
    num_samples_per_bit = int(fs / bit_rate)
    threshold = 0.5 * np.max(modulated_signal)
    demodulated_data = []

    for i in range(0, len(modulated_signal), num_samples_per_bit):
        bit_signal = modulated_signal[i:i + num_samples_per_bit]
        if np.mean(bit_signal) > threshold:
            demodulated_data.append(1)
        else:
            demodulated_data.append(0)

    return np.array(demodulated_data)

# Function to record audio from microphone
def record_audio(duration, fs):
    print("Recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait()
    print("Recording finished.")
    return recording.flatten()

# Function to play audio
def play_audio(signal, fs):
    sd.play(signal, samplerate=fs)
    sd.wait()

# Generate binary data
binary_data = generate_binary_data(duration, bit_rate)

# Modulate binary data using OOK
fs = 44100  # Sampling frequency
modulated_signal = modulate_OOK(binary_data, carrier_freq, duration, fs)

# Play the modulated signal
play_audio(modulated_signal, fs)

# Record audio from microphone
recorded_signal = record_audio(duration, fs)

# Demodulate OOK-modulated signal
demodulated_data = demodulate_OOK(recorded_signal, carrier_freq, duration, fs, bit_rate)

print("Original Binary Data:", binary_data)
print("Demodulated Binary Data:", demodulated_data)
