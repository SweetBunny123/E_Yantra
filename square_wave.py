import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import csv

# We will create a function that returns a array with values of y  for each x
def generate_square_wave(x, frequency, amplitude):
    y = np.array([1 if np.floor(2 * frequency * t) % 2 == 0 else -1 for t in x])
    return y * amplitude


def save_as_csv(x,y):
    data = np.column_stack((x, y))
    with open('data.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Time', 'Amplitude'])  # Write header
        writer.writerows(data)

#Creating a slider such that user can input frequency amplitude and sampling rate
initial_frequency = 1.0
initial_amplitude = 1.0
initial_sampling_rate = 100.0

#Generate time array based on initial sampling rate
duration = 10  # Duration of the signal
num_samples = int(duration * initial_sampling_rate)
x = np.linspace(0, duration, num_samples)

#Generate initial square wave
y = generate_square_wave(x, initial_frequency, initial_amplitude)

###################################################### APPLYING A THEME ########################################################

# Create a figure with window color background
window_color = (0.95, 0.95, 0.95)  # RGB color code for window color
fig, ax = plt.subplots(facecolor=window_color)  # Set background color to window color
# Adjust the position of the subplot to shift it above
plt.subplots_adjust(top=0.85, bottom = 0.3)
# Plot the initial square wave with contrasting grid lines and labels
line, = ax.plot(x, y, color='orange')  # Set line color


# Customize plot appearance for better contrast
ax.set_title(f'Square wave - {initial_frequency} Hz, Amplitude: {initial_amplitude}, Sampling Rate: {initial_sampling_rate} Hz', color='black')  # Set text color
ax.set_xlabel('Time (s)', color='black')  # Set x-axis label color
ax.set_ylabel('Amplitude', color='black')  # Set y-axis label color
ax.grid(True, which='both', color='lightgrey')  # Set grid color
ax.axhline(y=0, color='black')  # Set horizontal line color

##################################################### MAKING THE MATPLOT WINDOW ########################################################


ax.set_ylim(-initial_amplitude * 1.5, initial_amplitude * 1.5)

# Add sliders for frequency, amplitude, and sampling rate with contrasting colors
ax_freq = plt.axes([0.15, 0.08, 0.65, 0.03], facecolor='lightgrey')  # Set slider background color
ax_amp = plt.axes([0.15, 0.04, 0.65, 0.03], facecolor='lightgrey')  # Set slider background color
ax_rate = plt.axes([0.15, 0.0, 0.65, 0.03], facecolor='lightgrey')  # Set slider background color

slider_freq = Slider(ax_freq, 'Frequency (Hz)', 0.1, 10.0, valinit=initial_frequency, color='orange')  # Set slider color
slider_amp = Slider(ax_amp, 'Amplitude', 0.1, 10.0, valinit=initial_amplitude, color='orange')  # Set slider color
slider_rate = Slider(ax_rate, 'Sampling Rate (samples/s)', 10.0, 1000.0, valinit=initial_sampling_rate, color='orange')  # Set slider color

# Create a button axes
button_ax = plt.axes([0.8, 0.875, 0.1, 0.04])  # [left, bottom, width, height]

# Create the button
save_button = Button(button_ax, 'Save as CSV')

# Update function for sliders
def update(val):
    frequency = slider_freq.val
    amplitude = slider_amp.val
    sampling_rate = slider_rate.val

    # Generate updated time array based on new sampling rate
    num_samples = int(duration * sampling_rate)
    x = np.linspace(0, duration, num_samples)

    y = generate_square_wave(x, frequency, amplitude)

    line.set_xdata(x)
    line.set_ydata(y)
    save_button.on_clicked(lambda event:save_as_csv(x,y))
    ax.set_title(f'Square wave - {frequency} Hz, Amplitude: {amplitude}, Sampling Rate: {sampling_rate} Hz', color='black')
    ax.set_ylim(-amplitude * 1.5, amplitude * 1.5)
    fig.canvas.draw_idle()
    
slider_freq.on_changed(update)
slider_amp.on_changed(update)
slider_rate.on_changed(update)

plt.show()
