"""TODO: Put your header comment here."""
""" By John Wen"""

import math
import random
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
    list = []
    functionsnoxy = ["avg","prod","cos_pi","sin_pi","square","cube"]
    functionsxy = ["x","y"]
    functionsall = functionsxy + functionsnoxy
    randomfunction = random.choice(functionsnoxy)
    if min_depth <= 1:
        randomfunction = random.choice(functionsall)
        if max_depth == 1:
            randomfunction = random.choice(functionsxy)
    if randomfunction in ["avg","prod"]:
        list.append(randomfunction)
        list.append(build_random_function(min_depth-1,max_depth-1))
        list.append(build_random_function(min_depth-1,max_depth-1))
    if randomfunction in ["cos_pi","sin_pi","square","cube"]:
        list.append(randomfunction)
        list.append(build_random_function(min_depth-1,max_depth-1))
    if randomfunction in ["x","y"]:
        list.append(randomfunction)
    return list



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
        >>> evaluate_random_function(["prod"],4,2)
        8
        >>> evaluate_random_function(["prod", ["x"], ["y"]], 0, 0)
        0
        >>> evaluate_random_function(["prod", ["avg", ["x"],["y"]], ["x"]], 2, 2)
        4
        >>> evaluate_random_function(["avg", ["prod", ["avg", ["x"],["y"]], ["x"]], ["prod", ["x"], ["y"]]], 0, 0)
        0.0
        >>> evaluate_random_function(["sin_pi", ["avg", ["prod", ["avg", ["x"],["y"]], ["x"]], ["prod", ["x"], ["y"]]]], 0, 0)
        0.0
        >>> evaluate_random_function(['sin_pi', ['cos_pi', ['cos_pi', ['x']]]], -1, -1)
        0.0
    """
    if len(f) == 2:
        evaluate_random_function(f[0],evaluate_random_function(f[1],x,y),y)
    if len(f) == 3:
        evaluate_random_function(f[0],
                                 evaluate_random_function(f[1],x,y),
                                 evaluate_random_function(f[2],x,y))
    if f == ["x"]:
        # print("return : ", x)
        return x
    elif f == ["y"]:
        # print("return : ", y)
        return y
    elif f[0]  == "prod":
        return x * y
    elif f[0] == "cos_pi":
        # print("return : ", math.cos(math.pi * f[1]))
        return math.cos(math.pi * x)
    elif f[0] == "sin_pi":
        # print("return : ", math.sin(math.pi * f[1]))
        return math.sin(math.pi * x)
    elif f[0] == "avg":
        # print("return : ", (f[1] + f[2] / 2))
        return (x + y) / 2
    elif f[0] == "square":
        # print("return : ", f[1]**2 )
        return x ** 2
    elif f[0] == "cube":
        # print("return : ", f[1]**3 )
        return x ** 3


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
    inputscale = (val - input_interval_start) / (input_interval_end - input_interval_start)
    outputscale = (output_interval_end - output_interval_start)
    return inputscale * outputscale + output_interval_start



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
    red_function = build_random_function(10,15)
    green_function = build_random_function(10,15)
    blue_function = build_random_function(10,15)

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
    # doctest.testmod(verbose=True)
    # doctest.run_docstring_examples(evaluate_random_function, globals(), verbose=True)
    # doctest.testmod()
    # print(evaluate_random_function(["prod", ["x"], ["y"]], 2 ,3))
    generate_art("myart.png")
