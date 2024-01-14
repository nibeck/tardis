    

def map_range(value, in_min, in_max, out_min, out_max):
    # Ensure the input value is within the specified range
    value = max(min(value, in_max), in_min)
    
    # Perform linear mapping
    mapped_value = (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    
    # Round the result to an integer (optional, depending on your needs)
    mapped_value = int(round(mapped_value))
    
    return mapped_value

print("1:",map_range(1, 0, 100, 50, 0))