#Call with "python hack_assembler.py <filename>"

import sys

def parser(file_path):

    def remove_whitespace_and_labels():
        for i in lines:
            if i[0] != "\n":
                i = i.strip()
                if i[0] != "/":

    file = open(file_path, 'r')
    lines = file.readlines()
    file.close()

    lines_new = []
    remove_whitespace_and_labels()
    symbols()

    return lines_new

def hack_assembler():
    if len(sys.argv) != 2:
        print("Usage: python jack_compiler.py <filename>")
        return
    
    filename = sys.argv[1]
    parsed_lines = parser(filename)
    code(parsed_lines, filename.replace(".jack", ""))

hack_assembler()

