import numpy as np
import matplotlib.pyplot as plt

class AstableMultivibrator:
    def __init__(self, R1, R2, R, C, V_sat):
        self.R1 = R1
        self.R2 = R2
        self.R = R
        self.C = C
        self.V_sat = V_sat
        self.time_period = 0.001
        self.v_minus = -V_sat * (0.5)
        self.v_plus = V_sat * (0.5)
        self.vout = V_sat

    def update(self, num_cycles):
        t = np.linspace(0, num_cycles * self.time_period, 1000)
        result = []
        capacitance = []
        Vc = np.zeros_like(t)
        Vout = np.zeros_like(t)
        for i in range(len(t)):
            self.v_plust = 0.5*self.vout
            if self.is_high_period(t[i]):
                self.vout = self.V_sat
            else:
                self.vout = -self.V_sat
            print(self.v_minus-self.v_plus)
            self.v_minus = (self.v_minus - self.vout) * (np.exp(-(t[i] % (self.time_period / 2)) / (self.R* self.C))) + self.vout
            Vout[i] = self.vout
            Vc[i] = self.v_minus  # Voltage across the capacitor
            capacitance.append(self.v_minus)
            result.append(self.vout)
        return t, Vc, Vout, capacitance

    def is_high_period(self, time):
        return time % self.time_period < self.time_period / 2

# Component values
R1 = 10e3   # Resistance 1 (ohms)
R2 = 10e3   # Resistance 2 (ohms)
R = 4.5e3   # Resistor R (ohms)
C = 10e-6   # Capacitance (farads)
V_sat = 5.0 # Saturation voltage level

# Create astable multivibrator
astable = AstableMultivibrator(R1, R2, R, C, V_sat)

# Number of cycles to simulate
num_cycles = 5

# Update waveforms
t, Vc, Vout, capacitance = astable.update(num_cycles)

# Plot the waveforms
plt.figure(figsize=(10, 6))

# Plot Voltage across Capacitor (Vc) and Output Voltage (Vout) overlapped
plt.plot(t, Vc, label='Voltage across Capacitor (Vc)', color='blue')
plt.plot(t, Vout, label='Output Voltage (Vout)', color='red')
plt.title('Astable Multivibrator Output')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.legend()
plt.grid(True)

plt.show()
