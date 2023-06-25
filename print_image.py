#!/usr/bin/env python3
""" print_image """

import argparse
import os
import subprocess

from PIL import Image
from numpy import asarray

# =============================================================================

class PrintImage():
    """ PrintImage """

    # -------------------------------------------------------------------------

    def __init__(self):
        """ __init__ """
        self._reset = TerminalUtilities.get_reset()
        self._background = [ 255, 251, 232 ]

    # -------------------------------------------------------------------------

    def print_image_grey(self, columns, rows, image):
        """ print_image_grey """
        raise NotImplementedError()

    # -------------------------------------------------------------------------

    def print_image_rgba(self, columns, rows, image):
        """ print_image_rgba """
        raise NotImplementedError()

    # -------------------------------------------------------------------------

    def apply_alpha(self, pixel):
        """ apply_alpha """
        result = [0] * 3

        alpha = pixel[3]

        for i in range(0, 3):
            result[i] = int((float(alpha) * pixel[i]) / 255.0)
            result[i] += int((float(255 - alpha) * self._background[i] / 255.0))

        return result

    # -------------------------------------------------------------------------

    def set_background(self, rgb_values):
        """ set_background """
        self._background = rgb_values

# =============================================================================

class PrintImageOnePixelPerLine(PrintImage):
    """ PrintImageOnePixelPerLine """

    # -------------------------------------------------------------------------

    def print_image_grey(self, columns, rows, image):
        """ Print Image Grey """

        numpydata = asarray(image)

        y_index = 0
        for rows in numpydata:
            x_index = 0
            for pixel in rows:
                if x_index * 2 < columns:
                    self.print_pixel_grey(x_index, y_index, pixel)
                x_index += 1
            print(self._reset)
            y_index += 1

    # -------------------------------------------------------------------------

    def print_image_rgba(self, columns, rows, image):
        """ Print Image RGBA """

        image_rgba = image.convert('RGBA')
        numpydata = asarray(image_rgba)

        y_index = 0
        for rows in numpydata:
            x_index = 0
            for pixel in rows:
                if x_index * 2 < columns:
                    self.print_pixel_rgba(x_index, y_index, pixel)
                x_index += 1
            print(self._reset)
            y_index += 1

    # -------------------------------------------------------------------------

    def print_pixel_grey(self, x_index, y_index, pixel):
        """ print_pixel_grey """
        raise NotImplementedError()

    # -------------------------------------------------------------------------

    def print_pixel_rgb(self, x_index, y_index, pixel):
        """ print_pixel_rgb """
        raise NotImplementedError()

    # -------------------------------------------------------------------------

    def print_pixel_rgba(self, x_index, y_index, pixel):
        """ print_pixel_rgba """
        raise NotImplementedError()

# =============================================================================

class PrintImageTwoPixelsPerLine(PrintImage):
    """ PrintImageTwoPixelsPerLine """

    # -------------------------------------------------------------------------

    def print_image_grey(self, columns, rows, image):
        """ Print Image Grey """

        numpydata = asarray(image)

        for y_index in range(0, len(numpydata), 2):
            row1 = numpydata[y_index]
            row2 = []

            if (y_index + 1) < len(numpydata):
                row2 = numpydata[y_index + 1]

            for x_index, pixel1 in enumerate(row1):
                if x_index < columns:

                    pixel2 = []

                    if len(row2) == len(row1):
                        pixel2 = row2[x_index]

                    self.print_pixels_grey(x_index, y_index, pixel1, pixel2)

            print(self._reset)

    # -------------------------------------------------------------------------

    def print_image_rgba(self, columns, rows, image):
        """ Print Image RGBA """

        image_rgba = image.convert('RGBA')
        numpydata = asarray(image_rgba)

        for y_index in range(0, len(numpydata), 2):
            row1 = numpydata[y_index]
            row2 =[]

            if (y_index + 1) < len(numpydata):
                row2 = numpydata[y_index + 1]

            for x_index, pixel1 in enumerate(row1):
                if x_index < columns:

                    pixel2 = []

                    if len(row2) == len(row1):
                        pixel2 = row2[x_index]

                    self.print_pixels_rgba(x_index, y_index, pixel1, pixel2)

            print(self._reset)

    # -------------------------------------------------------------------------

    def print_pixels_grey(self, x_index, y_index, pixel1, pixel2):
        """ print_pixels_grey """
        raise NotImplementedError()

    # -------------------------------------------------------------------------

    def print_pixels_rgb(self, x_index, y_index, pixel1, pixel2):
        """ print_pixels_rgb """
        raise NotImplementedError()

    # -------------------------------------------------------------------------

    def print_pixels_rgba(self, x_index, y_index, pixel1, pixel2):
        """ print_pixel_rgba """
        raise NotImplementedError()

# =============================================================================

class PrintImageTwoPixelsPerLine256Colour(PrintImageTwoPixelsPerLine):
    """ PrintImageTwoPixelsPerLine256Colour """

    # -------------------------------------------------------------------------

    def print_pixels_grey(self, x_index, y_index, pixel1, pixel2):
        """ Print Pixel Grey """

        index1 = Colour256Utilities.quantize_grey(x_index, y_index, pixel1)
        index2 = None

        if pixel2:
            index2 = Colour256Utilities.quantize_grey(x_index, 
                                                      y_index + 1, 
                                                      pixel2)

        self.print_pixels_rgb(x_index, y_index, index1, index2)

    # -------------------------------------------------------------------------

    def print_pixels_rgb(self, x_index, y_index, pixel1, pixel2):
        """ Print Pixel RGB """

        if pixel2:
            # background
            print(f"\033[48;5;{pixel2}m", end="")
        else:
            print(self._reset, end="")

        # foreground
        print(f"\033[38;5;{pixel1}m", end="")
        print("▀", end="")

    # -------------------------------------------------------------------------

    def print_pixels_rgba(self, x_index, y_index, pixel1, pixel2):
        """ Print Pixel RGBA """

        p_1 = self.apply_alpha(pixel1)
        p_1 = Colour256Utilities.quantize_rgb(x_index, y_index, p_1)

        p_2 = []

        if len(pixel2) == 4:
            p_2 = self.apply_alpha(pixel2)
            p_2 = Colour256Utilities.quantize_rgb(x_index, y_index + 1, p_2)

        self.print_pixels_rgb(x_index, y_index, p_1, p_2)

# =============================================================================

class PrintImageOnePixelPerLine256Colour(PrintImageOnePixelPerLine):
    """ PrintImageOnePixelPerLine256Colour """

    # -------------------------------------------------------------------------

    def print_pixel_grey(self, x_index, y_index, pixel):
        """ Print Pixel Grey """

        index = Colour256Utilities.quantize_grey(x_index, y_index, pixel)
        self.print_pixel_rgb(x_index, y_index, index)

    # -------------------------------------------------------------------------

    def print_pixel_rgb(self, x_index, y_index, pixel):
        """ Print Pixel RGB """

        print(f"\033[48;5;{pixel}m  ", end="")

    # -------------------------------------------------------------------------

    def print_pixel_rgba(self, x_index, y_index, pixel):
        """ Print Pixel RGBA """

        pixel_rgb = self.apply_alpha(pixel)
        index = Colour256Utilities.quantize_rgb(x_index, y_index, pixel_rgb)
        self.print_pixel_rgb(x_index, y_index, index)

# =============================================================================

class PrintImageTwoPixelsPerLineTrueColour(PrintImageTwoPixelsPerLine):
    """ PrintImageTwoPixelsPerLineTrueColour """

    # -------------------------------------------------------------------------

    def print_pixels_grey(self, x_index, y_index, pixel1, pixel2):
        """ Print Pixel Grey """

        pixel1 = [ pixel1, pixel1, pixel1 ]
        pixel2 = [ pixel2, pixel2, pixel2 ]

        self.print_pixels_rgb(x_index, y_index, pixel1, pixel2)


    # -------------------------------------------------------------------------

    def print_pixels_rgb(self, x_index, y_index, pixel1, pixel2):
        """ Print Pixel RGB """

        if len(pixel2) == 3:
            # background
            print(f"\033[48;2;{pixel2[0]};{pixel2[1]};{pixel2[2]}m", end="")
        else:
            print(self._reset, end="")

        # foreground
        print(f"\033[38;2;{pixel1[0]};{pixel1[1]};{pixel1[2]}m", end="")

        print("▀", end="")

    # -------------------------------------------------------------------------

    def print_pixels_rgba(self, x_index, y_index, pixel1, pixel2):
        """ Print Pixel RGBA """

        p_1 = self.apply_alpha(pixel1)

        if len(pixel2) == 4:
            p_2 = self.apply_alpha(pixel2)
        else:
            p_2 = []

        self.print_pixels_rgb(x_index, y_index, p_1, p_2)


# =============================================================================

class PrintImageOnePixelPerLineTrueColour(PrintImageOnePixelPerLine):
    """ PrintImageOnePixelPerLineTrueColour """

    # -------------------------------------------------------------------------

    def print_pixel_grey(self, x_index, y_index, pixel):
        """ Print Pixel Grey """

        pixel = [ pixel, pixel, pixel ]
        self.print_pixel_rgb(x_index, y_index, pixel)

    # -------------------------------------------------------------------------

    def print_pixel_rgb(self, x_index, y_index, pixel):
        """ Print Pixel RGB """

        print(f"\033[48;2;{pixel[0]};{pixel[1]};{pixel[2]}m  ", end="")

    # -------------------------------------------------------------------------

    def print_pixel_rgba(self, x_index, y_index, pixel):
        """ Print Pixel RGBA """

        pixel_rgb = self.apply_alpha(pixel)
        self.print_pixel_rgb(x_index, y_index, pixel_rgb)

# =============================================================================

class Colour256Utilities():
    """ Colour256Utilities """

    # -------------------------------------------------------------------------

    @staticmethod
    def dither4x4(x_index, y_index, value):
        """ dither 4x4 """

        ordered = [
            [  0,  8,  2, 10 ],
            [ 12,  4, 14,  6 ],
            [  3, 11,  1,  9 ],
            [ 15,  7, 13,  5 ]
        ]

        test = ordered[y_index % 4][x_index % 4]
        distance = int(((value % 24) * 15.0) / 23.0)

        level = int(((value + 0.5) / 255.0) * 24.0)

        if distance > test:
            level += 1

        if level < 0:
            level = 0
        elif level > 24:
            level = 24

        return level

    # -------------------------------------------------------------------------

    @staticmethod
    def dither8x8(x_index, y_index, value):
        """ dither 8x8 """

        ordered = [
            [  0,  47,  12,  59,   3,  50,  15,  62 ],
            [ 32,  16,  43,  28,  34,  19,  46,  31 ],
            [  8,  55,   4,  51,  11,  58,   7,  54 ],
            [ 39,  24,  35,  20,  42,  27,  38,  23 ],
            [  2,  49,  14,  61,   1,  48,  13,  60 ],
            [ 33,  18,  45,  30,  32,  17,  44,  29 ],
            [ 10,  57,   6,  53,   9,  56,   5,  52 ],
            [ 41,  26,  37,  22,  40,  25,  36,  21 ]
        ]

        test = ordered[y_index % 8][x_index % 8]
        distance = int(((value % 51) * 63.0) / 50.0)

        level = int(value / 51.0)

        if distance > test:
            level += 1

        if level < 0:
            level = 0
        elif level > 5:
            level = 5

        return level

    # -------------------------------------------------------------------------

    @staticmethod
    def quantize_grey(x_index, y_index, value):
        """ quantize grey """

        index = Colour256Utilities.dither4x4(x_index, y_index, value)

        if index == 0:
            index = 16
        else:
            index += 231

        return index

    # -------------------------------------------------------------------------

    @staticmethod
    def quantize_rgb(x_index, y_index, pixel):
        """ quantize RGB """

        red = Colour256Utilities.dither8x8(x_index, y_index, pixel[0])
        green = Colour256Utilities.dither8x8(x_index, y_index, pixel[1])
        blue = Colour256Utilities.dither8x8(x_index, y_index, pixel[2])

        return 16 + (red * 36) + (green * 6) + blue

# =============================================================================

class TerminalUtilities():
    """ TerminalUtilities """

    # -------------------------------------------------------------------------

    @staticmethod
    def get_terminal_value(name):
        """ get_terminal_value """

        with subprocess.Popen(["/usr/bin/tput", name], stdout=subprocess.PIPE) as proc:
            value = int(proc.communicate()[0])

        return value

    # -------------------------------------------------------------------------

    @staticmethod
    def get_terminal_size():
        """ get_terminal_size """

        columns = TerminalUtilities.get_terminal_value("cols")
        rows = TerminalUtilities.get_terminal_value("lines")

        return (columns, rows)

    # -------------------------------------------------------------------------

    @staticmethod
    def get_reset():
        """ get_reset """
        result = subprocess.run(['/usr/bin/tput', 'sgr0'],
                                 check = False,
                                 stdout = subprocess.PIPE,
                                stderr = subprocess.PIPE)

        return result.stdout.decode()

    # -------------------------------------------------------------------------

    @staticmethod
    def has_true_colour():
        """ hase_true_colour """

        result = False
        color_term = os.getenv('COLORTERM')

        if color_term in ( 'truecolor', '24bit'):
            result = True

        return result


# =============================================================================

def main():
    """main"""

    # -------------------------------------------------------------------------

    colours = "true"
    lines = 2

    # -------------------------------------------------------------------------

    if not TerminalUtilities.has_true_colour():
        colours = "256"

    # -------------------------------------------------------------------------

    parser = argparse.ArgumentParser()

    parser.add_argument('-b', '--background', help='background r,g,b', default=None)
    parser.add_argument('-c', '--colours', help='true or 256 colours', default=colours)
    parser.add_argument('-l', '--lines', type = int, help='pixels per line', default=lines)
    parser.add_argument('name', help='image file name')

    args = parser.parse_args()

    colours = args.colours
    lines = args.lines

    # -------------------------------------------------------------------------

    printer = None

    if colours == "256":
        if lines == 1:
            printer = PrintImageOnePixelPerLine256Colour()
        else:
            printer = PrintImageTwoPixelsPerLine256Colour()
    else:
        if lines == 1:
            printer = PrintImageOnePixelPerLineTrueColour()
        else:
            printer = PrintImageTwoPixelsPerLineTrueColour()

    # -------------------------------------------------------------------------

    if args.background:
        rgb_values = [int(e) for e in args.background.split(',')]
        printer.set_background(rgb_values)

    # -------------------------------------------------------------------------

    (columns, rows) = TerminalUtilities.get_terminal_size()

    # -------------------------------------------------------------------------

    image = Image.open(args.name)

    # -------------------------------------------------------------------------

    if image.mode == "L":
        printer.print_image_grey(columns, rows, image)
    else:
        printer.print_image_rgba(columns, rows, image)

# =============================================================================

if __name__ == '__main__':
    main()
