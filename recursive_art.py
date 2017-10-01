"""TODO: Put your header comment here."""

import random
from PIL import Image
from math import cos, sin, pi

def build_random_function(min_depth, max_depth, movie):
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
    functions = ['prod', 'avg', 'acos_pi', 'asin_pi', 'cos_pi', 'sin_pi', 'cubed'] # possible operations

    if movie:
        variables = [['x'],['y'],['t']]  # three variables when making a movie
    else:
        variables = [['x'],['y']]

    if max_depth == 0:
        return variables[random.randint(0,len(variables)-1)]  # if maxed depth is reached, stop recursion

    rand_func = functions[random.randint(0,len(functions)-1)]  # pick a random function

    if rand_func in functions[0:4]: # for the two-variable functions
        return [rand_func, build_random_function(min_depth-1,max_depth-1,movie), build_random_function(min_depth-1,max_depth-1,movie)]
    else:  # for one variable functions
        return [rand_func, build_random_function(min_depth-1,max_depth-1,movie)]



def evaluate_random_function(f, x, y, t):
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
    """
    if f == ['x']:
        return x
    if f == ['y']:
        return y
    if f == ['t']:
        return t
    if f[0] == 'prod':
        return evaluate_random_function(f[1],x,y,t)*evaluate_random_function(f[2],x,y,t)
    if f[0] == 'avg':
        return .5*(evaluate_random_function(f[1],x,y,t)+evaluate_random_function(f[2],x,y,t))
    if f[0] == 'acos_pi':
        return evaluate_random_function(f[1],x,y,t) * cos(pi * evaluate_random_function(f[2],x,y,t))
    if f[0] == 'asin_pi':
        return evaluate_random_function(f[1],x,y,t) * sin(pi * evaluate_random_function(f[2],x,y,t))
    if f[0] == 'sin_pi':
        return sin(pi * evaluate_random_function(f[1],x,y,t))
    if f[0] == 'cos_pi':
        return cos(pi * evaluate_random_function(f[1],x,y,t))
    if f[0] == 'cubed':
        return evaluate_random_function(f[1],x,y,t)**3

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
    return output_interval_start + ( val - input_interval_start) * ( output_interval_end - output_interval_start ) / float( input_interval_end - input_interval_start)


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
    red_function = build_random_function(7, 9, False)
    green_function = build_random_function(7, 9, False)
    blue_function = build_random_function(7, 9, False)
    t = 0
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                color_map(evaluate_random_function(red_function, x, y, t)),
                color_map(evaluate_random_function(green_function, x, y, t)),
                color_map(evaluate_random_function(blue_function, x, y, t))
            )

    im.save(filename)

def generate_movie(pathname, frames, x_size=500, y_size=500):
    """Generate computational GIF and save as folder of images.

    Args:
        filename: string filename for image (should be .png)
        frames: number of frames to have in the movie
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(4, 7, True)
    green_function = build_random_function(4, 7, True)
    blue_function = build_random_function(4, 7, True)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for n in range(frames):
        t = remap_interval(n, 0, frames, -1, 1)
        for i in range(x_size):
            for j in range(y_size):
                x = remap_interval(i, 0, x_size, -1, 1)
                y = remap_interval(j, 0, y_size, -1, 1)
                pixels[i, j] = (
                    color_map(evaluate_random_function(red_function, x, y, t)),
                    color_map(evaluate_random_function(green_function, x, y, t)),
                    color_map(evaluate_random_function(blue_function, x, y, t))
                )
        print("%s//frame%d.png" % (pathname, n))
        im.save("%s//frame%d.png" % (pathname, n))

if __name__ == '__main__':
#    import doctest
#    doctest.testmod(verbose=True)

#   Create some computational art!
    frames = 100
    generate_movie("C://Users//iblancett//Documents//SoftwareDesign//ComputationalArt//movie", frames, 350, 350)

#    test_image("noise.png")
