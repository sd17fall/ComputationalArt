"""TODO: Put your header comment here."""

import random
from PIL import Image
import math
pi = 3.14
def prod(a,b): #Returns the product of two values
    return a * b

def avg(a,b):           #returns the average of two values
   return 0.5 * (a + b)

def cos_pi(a):              #returns the cosine of a value
    return math.cos(pi * a)

def sin_pi(a):
    return math.sin(pi * a) #returns the sine of a value

def findx(a , b):           #returns the x value
    return a

def findy(a,b):             #returns the y value
    return b
def times_neg_1(a):         #returns the negitive 
    return -1 * a
def mean(a,b):               #returns the the geometric mean
    return (abs(a) * abs(b)) ** 0.5






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
    depth = random.randint(min_depth,max_depth);

    allfunc = ['prod','avg','cos_pi','sin_pi','x','y','times_neg_1','mean']
    xory = ['y','x']
    func = random.choice(allfunc)
    #print (func, depth)

    if depth == 1:
        return random.choice(xory)
    if func == 'prod':
        return ['prod',build_random_function(depth-1, depth-1),build_random_function(depth-1, depth-1)]
    elif func == 'avg':
        return ['avg',build_random_function(depth-1, depth-1),build_random_function(depth-1, depth-1)]
    elif func == 'mean':
        return ['mean',build_random_function(depth-1, depth-1),build_random_function(depth-1, depth-1)]
    elif func == 'cos_pi':
        return ['cos_pi',build_random_function(depth-1, depth-1)]
    elif func == 'sin_pi':
        return ['sin_pi',build_random_function(depth-1, depth-1)]
    elif func == 'times_neg_1':
        return ['times_neg_1',build_random_function(depth-1, depth-1)]
    elif func == 'x':
        return ['x',build_random_function(depth-1, depth-1),build_random_function(depth-1, depth-1)]
    elif func == 'y':
        return ['y',build_random_function(depth-1, depth-1),build_random_function(depth-1, depth-1)]
    else:
        print ("error")



  #  prod = ['prod',build_random_function(depth-1, depth-1),build_random_function(depth-1, depth-1)]
  #  avg = ['avg',build_random_function(depth-1, depth-1),build_random_function(depth-1, depth-1)]
  #  cos = ['cos_pi',build_random_function(depth-1, depth-1)]
  #  sin = ['sin_pi',build_random_function(depth-1, depth-1)]
  #  x = ['x',build_random_function(depth-1, depth-1),build_random_function(depth-1, depth-1)]
  #  y = ['y', build_random_function(depth-1, depth-1),build_random_function(depth-1, depth-1)]
  
  

    # TODO: implement this

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
    """
    #if (f[0] == 'x') | (f[0] == 'X'):
    #    return x
    #elif (f[0] == 'y') | (f[0] == 'y'):
    #    return y
    #else:
    #    return "Error"
    #TODO: implement this
    #print (f)
    e = evaluate_random_function #dummy function to make the code take up less room
    if len(f) == 1:              # only happens on the inner most layer when the list is [x] or [y]
        if f[0] == 'x':
            return x
        elif f[0] == 'y':
            return y
        else:
            print ("Evaluating Error", f[0])        #if somthing other than x or y is found somthing went wrong

    elif f[0] == 'prod':
        return prod(e(f[1],x,y),e(f[2],x,y))
    elif f[0] == 'avg':
        return avg(e(f[1],x,y),e(f[2],x,y))
    elif f[0] == 'cos_pi':
        return cos_pi(e(f[1],x,y))
    elif f[0] == 'sin_pi':
        return sin_pi(e(f[1],x,y))
    elif f[0] == 'x':
        return findx(e(f[1],x,y),e(f[2],x,y))
    elif f[0] == 'y':
        return findy(e(f[1],x,y),e(f[2],x,y))
    elif f[0] == 'mean':
        return mean(e(f[1],x,y),e(f[2],x,y))
    elif f[0] == 'times_neg_1':
        return times_neg_1(e(f[1],x,y))
    else:
        print ("Evaluation Error", f[0]) # #if somthing other than the above options is found somthing went wrong
    





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

    difference = val-input_interval_start
    difference = difference/ (input_interval_end - input_interval_start)
    difference = difference * (output_interval_end - output_interval_start)
    difference = difference + output_interval_start
    return difference
    # TODO: implement this
    pass


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
    red_function = build_random_function(9, 15)
    green_function = build_random_function(9, 15)
    blue_function = build_random_function(9, 15)
    x = random.uniform(0, 1)
    y = random.uniform(0, 1)
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
    #print(build_random_function(7,9))
   # doctest.run_docstring_examples(remap_interval, globals(), verbose=True)

    # Create some computational art!
    # TODO: Un-comment the generate_art function call after you
    #       implement remap_interval and evaluate_random_function
    for i in range(10):
        generate_art("Test6." + str(i) + ".png")

    # Test that PIL is installed correctly
    # TODO: Comment or remove this function call after testing PIL install
    #test_image("noise1.png")
