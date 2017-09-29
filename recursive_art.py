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

    if min_depth < 1:
        var = random.randint(1,2)
        if var == 1:
            return "x"
        else:
            return "y"

    min_depth -= 1
    max_depth -= 1

    #varies the depth of the function
    d_range = max_depth - min_depth
    if d_range > 0:
        n = random.randint(1, d_range)
        if n==1:
            min_depth +=1

    rand_int = random.randint(1,7)
    print(rand_int)
    single_inputs = ["sin_pi", "cos_pi", "x_3", "cos_30pi"]
    double_inputs = ["prod", "avg", "hypot_n"]

    up_to = len(single_inputs) + 1
    num_funcs = len(single_inputs) + len(double_inputs)

    if rand_int in range (1,up_to):
        return [single_inputs[rand_int - 1], [build_random_function(min_depth, max_depth)]]

    if rand_int in range (up_to, num_funcs + 1):
        return [double_inputs[rand_int - up_to], [build_random_function(min_depth, max_depth), build_random_function(min_depth, max_depth)]]

    print('error')
    pass


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
        >>> evaluate_random_function(["avg", ["x", "y"]],5,10)
        7.5
        >>> evaluate_random_function(["prod", ["x", "y"]],3,5)
        15
        >>> evaluate_random_function(["cos_pi", ["x"]], 2 ,5)
        1.0
        >>> evaluate_random_function(["sin_pi", ["y"]], 3 , 3.5)
        -1.0
        >>> evaluate_random_function(["prod", [["sin_pi", ["y"]], "x"]], 3 , 3.5)
        -3.0
    """
    func = f[0]
    if func == "x":
        return x
    if func == "y":
        return y
    if func == "avg":
        in_func = f[1]
        return .5*(evaluate_random_function(in_func[0], x, y) + evaluate_random_function(in_func[1], x, y))
    if func == "x_3":
        return x**3
    if func == "prod":
        in_func = f[1]
        return evaluate_random_function(in_func[0], x, y) * evaluate_random_function(in_func[1], x, y)
    if func == "sin_pi":
        in_func = f[1]
        return math.sin(evaluate_random_function(in_func[0], x, y)*math.pi)
    if func == "cos_pi":
        in_func = f[1]
        return math.cos(evaluate_random_function(in_func[0], x, y)*math.pi)
    if func == "cos_30pi":
        in_func = f[1]
        return math.cos(evaluate_random_function(in_func[0], x, y)*math.pi*30)
    #nonlinear scaling of hypotenuse function
    if func == "hypot_n":
        in_func = f[1]
        hypotenuse = math.hypot(evaluate_random_function(in_func[0], x, y), evaluate_random_function(in_func[1], x, y))
        if hypotenuse > 1:
            hypotenuse = 1
        if hypotenuse < -1:
            hypotenuse = -1
        return hypotenuse
    else:
        pass

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
    initial_range = input_interval_end - input_interval_start
    final_range = output_interval_end - output_interval_start
    initial_mag = val - input_interval_start
    ratio = initial_mag / initial_range
    end_mag = ratio * final_range
    end_value = end_mag + output_interval_start

    return end_value


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
    #red_function = ["x"]
    #green_function = ["y"]
    #blue_function = ["x"]
    red_function = build_random_function(7, 9)
    green_function = build_random_function(7, 9)
    blue_function = build_random_function(7, 9)

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
    #doctest.run_docstring_examples(evaluate_random_function, globals(), verbose=True)

    # Create some computational art!
    # TODO: Un-comment the generate_art function call after you
    #       implement remap_interval and evaluate_random_function
    generate_art("myart.png")

    # Test that PIL is installed correctly
    # TODO: Comment or remove this function call after testing PIL install
    #test_image("noise.png")
