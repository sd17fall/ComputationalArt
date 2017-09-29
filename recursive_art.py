"""TODO: Put your header comment here."""

import random
import math
from PIL import Image


def build_random_function(min_depth, max_depth):
    """Build a random function.

    Builds a random function of depth at least min_depth and depth at most
    max_depth. (See the assignment write-up for the definition of depth
    in this context)

    Args:
        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function

    Returns:
        The randomly generated function represented as a nested list.
        (See the assignment writ-eup for details on the representation of
        these functions)
    """
    if min_depth == 1: # to get a variable depth,
        rand = random.randint(0, max_depth - min_depth)                         # pick an int between 0 and the diff of max and min depth - this is how many times you will keep going
        if rand == 0:                                                           # if 0, stop here
            rand = random.randint(0, 1)
            if rand == 0:
                return ["x"]
            return ["y"]
    if max_depth == 1:                                                          # if max depth gets to 1, stop here
        rand = random.randint(0, 1)
        if rand == 0:
            return ["x"]
        return ["y"]
    func = [ "prod", "avg", "cos_pi", "sin_pi", "cube", "sin_5pi"]
    rand = random.randint(0, len(func) - 1)
    chosenfunc = func[rand]

    # make sure to pass function two arguments if it needs it
    if chosenfunc == "prod" or chosenfunc == "avg":
        return [chosenfunc,  build_random_function(min_depth - 1, max_depth - 1), build_random_function(min_depth - 1, max_depth - 1)]
    return [chosenfunc,  build_random_function(min_depth - 1, max_depth - 1) ]


def evaluate_random_function(f, x, y):
    """Evaluate the random function f with inputs x,y.

    The representation of the function f is defined in the assignment write-up.

    Args:
        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function

    Returns:
        The function value

    Examples:
        >>> evaluate_random_function(["x"],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02)
        0.02
        >>> evaluate_random_function( ["sin_pi", ["x"]], 0.0,  0.3)
        0.0
        >>> evaluate_random_function( ["cos_pi", ["y"]], 0.3,  0.0)
        1.0
        >>> evaluate_random_function(["cos_pi", ["sin_pi", ["x"]]], 0.0,  0.3)
        1.0
        >>> evaluate_random_function(["prod", ["x"], ["y"]], 0.1,  0.5)
        0.05
        >>> evaluate_random_function(["avg", ["x"], ["y"]], 0.2,  0.5)
        0.35
        >>> evaluate_random_function(["cube", ["y"]], 0.1, -1.0)
        -1.0
        >>> evaluate_random_function( ["sin_5pi", ["x"]], 0.078,  0.8)
        0.9408807689542255
    """
    fname = f[0]
    if fname == "x":
        return x
    if fname == "y":
        return y
    if fname == "sin_pi":
        return math.sin( math.pi * evaluate_random_function(f[1], x, y) )
    if fname == "cos_pi":
        return math.cos( math.pi * evaluate_random_function(f[1], x, y) )
    if fname == "prod":
        return evaluate_random_function(f[1], x, y) * evaluate_random_function(f[2], x, y)
    if fname == "avg":
        return 0.5 * (evaluate_random_function(f[1], x, y) + evaluate_random_function(f[2], x, y))
    if fname == "cube":
        return evaluate_random_function(f[1], x, y) ** 3
    if fname == "sin_5pi":
        return math.sin( math.pi * 5 * evaluate_random_function(f[1], x, y) )

def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """Remap a value from one interval to another.

    Given an input value in the interval [input_interval_start,
    input_interval_end], return an output value scaled to fall within
    the output interval [output_interval_start, output_interval_end].

    Args:
        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values

    Returns:
        The value remapped from the input to the output interval

    Examples:
        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    input_interval_length = input_interval_end - input_interval_start
    output_interval_length = output_interval_end - output_interval_start

    val_in = val - input_interval_start

    input_pos = val_in/input_interval_length
    output_pos = input_pos * output_interval_length
    return output_interval_start + output_pos


def color_map(val):
    """Maps input value between -1 and 1 to an integer 0-255, suitable for use as an RGB color code.

    Args:
        val: value to remap, must be a float in the interval [-1, 1]

    Returns:
        An integer in the interval [0,255]

    Examples:
        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """Generate a test image with random pixels and save as an image file.

    Args:
        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename, x_size=350, y_size=350):
    """Generate computational art and save as an image file.

    Args:
        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!

    min_depth = 2
    max_depth = 9

    red_function = build_random_function(min_depth, max_depth)
    print("RED: ", red_function)
    green_function = build_random_function(min_depth, max_depth)
    print("GREEN: ", green_function)
    blue_function = build_random_function(min_depth, max_depth)
    print("BLUE: ", blue_function)



    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                color_map(evaluate_random_function(red_function, x, y)),
                color_map(evaluate_random_function(green_function, x, y)),
                color_map(evaluate_random_function(blue_function, x, y))
            )

    im.save(filename)


if __name__ == '__main__':
    import doctest
    doctest.testmod()


    # Create some computational art!
    generate_art("myart21.png")

    # Test that PIL is installed correctly
    #test_image("noise.png")
