import colorsys

def rgb_to_hls(r, g, b):
    # Ensure that the RGB values are in the range [0, 255]
    r = min(255, max(0, int(r)))
    g = min(255, max(0, int(g)))
    b = min(255, max(0, int(b)))

    # Normalize RGB values to the range [0, 1]
    r_normalized = r / 255.0
    g_normalized = g / 255.0
    b_normalized = b / 255.0

    # Convert RGB to HLS
    h, l, s = colorsys.rgb_to_hls(r_normalized, g_normalized, b_normalized)

    # Convert hue to degrees (0-360)
    h_degrees = int(h * 360)

    return {
        'hue': h_degrees,
        'saturation': s,
        'luminance': l
    }

# Example usage:
r_value = 255
g_value = 0
b_value = 0

result = rgb_to_hls(r_value, g_value, b_value)
print("Input RGB values:", (r_value, g_value, b_value))
print("Hue:", result['hue'])
print("Saturation:", result['saturation'])
print("Luminance:", result['luminance'])