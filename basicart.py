""" Basic Art"""

red_function = ["x"]
green_function = ["y"]
blue_function = ["x"]

im = Image.new("RGB", (x_size, y_size))
pixels = im.load()
for i in range(x_size):
    for j in range(y_size):
        x = remap_interval(i, 0, x_size, -1, 1)
        y = remap_interval(j, 0, y_size, -1, 1)
        pixels[i,j] = (
            color_map(evaluate_random_function(red_function, x, y))
            color_map(evaluate_random_function(green_function, x, y))
            color_map(evaluate_random_function(blue_function, x, y)))


im.save(filename)
