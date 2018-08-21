#!/usr/bin/env python3

# Based on https://stackoverflow.com/a/19438403

import sys
from fontTools.ttLib import TTFont
from fontTools.unicode import Unicode

def fontcheck(input_filename, font_filenames):
    """fontcheck

Usage:
fontcheck input.txt font1.ttf font2.ttf ...
Finds characters that exist in the input file that are not included in any of the given font files.
Only one input file can be used. It must be the first argument. It can be any UTF-8 text file.
One or many font files can be used. They must be TrueType fonts.
Depends on fonttools (pip install fonttools)."""
    num_fonts = 0
    font_chars = dict()
    for filename in font_filenames:
        try:
            font = TTFont(filename, 0, allowVID=0, ignoreDecompileErrors=True, fontNumber=-1)
        except Exception as ex:
            sys.stderr.write("%s: %s\n" % (filename, ex))
        else:
            num_fonts += 1
            for ctable in font["cmap"].tables:
                for code in ctable.cmap:
                    font_chars[code] = True
            font.close()

    if num_fonts < 1:
        return 1

    if len(font_chars) < 1:
        sys.stderr.write("Zero characters found in fonts. Check that given fonts are valid TrueType fonts.\n")
        return 1

    missing_chars = dict()
    try:
        input_file = open(input_filename, "r")
    except Exception as ex:
        sys.stderr.write("%s: %s\n" % (input_filename, ex))
        return 1
    else:
        for char in input_file.read():
            code = ord(char)
            if code not in font_chars:
                missing_chars[code] = char

    if len(missing_chars) > 0:
        print("The following characters could not be found in the fonts:")
        for code in missing_chars:
            print("{0:#0{1}x} {2:}".format(code, 6, repr(missing_chars[code])))

    return 0

if __name__ == "__main__":
    try:
        input_filename = sys.argv[1]
        font_filenames = sys.argv[2:]
    except:
        print(fontcheck.__doc__)
        exit(1)

    if not input_filename or len(font_filenames) < 1:
        print(fontcheck.__doc__)
        exit(1)
    else:
        exit(fontcheck(input_filename, font_filenames))
