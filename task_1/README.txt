main.py

usage: main.py [-h] [-s STUDENTS] [-r ROOMS] [-f FORMAT] [-res RESULT]

optional arguments:
  -h, --help                        show this help message and exit
  -s STUDENTS, --students STUDENTS  Path to students-file
  -r ROOMS, --rooms ROOMS           Path to rooms-file
  -f FORMAT, --format FORMAT        Format output file
  -res RESULT, --result RESULT      Name output file. Enter the name of the resulting file without the extension

EXAMPLE:

python main.py -s data/students.json -r data/rooms.json -f json -res result

python main.py -s data/students.json -r data/rooms.json -f xml -res result
