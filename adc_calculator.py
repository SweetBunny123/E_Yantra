def adc_conversion(analog_voltage, resolution_bits, reference_voltage):
    # Calculate voltage step size (LSB)
    voltage_step = reference_voltage / (2**resolution_bits)
    
    # Calculate digital value
    digital_value = analog_voltage / voltage_step
    
    # Round the digital value down to the nearest integer
    digital_value_rounded = int(digital_value)
    
    # Convert digital value to binary
    binary_value = bin(digital_value_rounded)[2:].zfill(resolution_bits)
    
    return digital_value_rounded, binary_value

# Function to validate user input
def get_float_input(prompt):
    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            print("Invalid input. Please enter a valid number.")

# Get user input
analog_voltage = get_float_input("Enter the analog voltage to the ADC (in volts): ")
resolution_bits = int(input("Enter the number of bits in the ADC: "))
reference_voltage = get_float_input("Enter the reference voltage to the ADC (in volts): ")

# Perform ADC conversion
digital_value, binary_value = adc_conversion(analog_voltage, resolution_bits, reference_voltage)

# Display the results
print("Numeric Digital Output:", digital_value)
print("Binary Digital Output:", binary_value)
