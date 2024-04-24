import math
import matplotlib.pyplot as plt
import csv

amplitude = int(input("Enter Amplitude: "))
frequency = float(input("Enter Frequency: "))
sampling_rate = int(input("Enter Sampling Rate: "))

vin = amplitude*(3/2)
out_high = amplitude 
out_low = 0
farads = 2/1000000   
ohms_a = 1000/(2*0.148*frequency)
ohms_b = 100000/(2*0.148*frequency)       
sim_time = 1      
step = sim_time / sampling_rate

def update_latch(latch, trigger, threshold, vin):
    if trigger < vin / 3:
        latch = True
    if threshold > vin * 2 / 3:
        latch = False
    return latch

def update_capacitor(cap, farads, res_a, res_b, vin, latch, step):
    if latch:
        tc = farads * (res_a + res_b)
        tp = step / tc
        pc = 1 - (1/math.e**tp)
        cap += (vin - cap) * pc
    else:
        tc = farads * res_b
        tp = step / tc
        pc = 1 - (1/math.e**tp)
        cap -= cap * pc
    return cap

def simulate(amplitude, frequency, step):
    out_high = amplitude
    out_low = 0
    vin = amplitude*(3/2)
    cap = 0
    latch = True
    vout = out_high
    cap_list = []
    out_list = []
    time_list = []
    time = 0
    while time < sim_time:
        cap = update_capacitor(cap, farads, ohms_a, ohms_b, vin, latch, step)
        latch = update_latch(latch, cap, cap, vin)
        if latch:
            vout = out_high
        else:
            vout = out_low
        cap_list.append(cap)
        out_list.append(vout)
        time_list.append(time)
        time += step
    return cap_list, out_list, time_list

cap_list, out_list, time_list = simulate(amplitude, frequency, step)

# Plot the graph
plt.plot(time_list, cap_list, label='Capacitor')
plt.plot(time_list, out_list, label='Output')
plt.xlabel('Time (Seconds)')
plt.ylabel('Volts')
plt.legend(loc='upper right')
plt.show()

# Save data to CSV file
output_file = 'simulation_data.csv'
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Time', 'Output'])
    for i in range(len(time_list)):
        writer.writerow([time_list[i], out_list[i]])

print("Data saved to:", output_file)


