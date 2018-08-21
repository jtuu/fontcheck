# fontcheck

## Usage:
`fontcheck input.txt font1.ttf font2.ttf ...`

Finds characters that exist in the input file that are not included in any of the given font files.
Only one input file can be used. It must be the first argument. It can be any UTF-8 text file.
One or many font files can be used. They must be TrueType fonts.

Depends on fonttools (pip install fonttools).
