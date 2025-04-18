#Call with "python jack_compiler.py <filename>"

import sys

symbols = [";",
           ",",
           "{{".format(),
           "}}".format(),
           "(",
           ")",
           "[",
           "]",
           "=",
           ".",
           "+",
           "-"]

def parser(file_path):

    def remove_whitespace_and_labels():
        for i in lines:
            if i[0] != "\n" and i[0] != "/" and i != "	\n":
                i = i.replace("	", "")
                i = i.split(" ")
                for j in i:
                    if j != "":
                        j = j.replace("\n", "")
                        if j in symbols:
                            lines_new.append(f"<symbol> {j} <symbol>\n")
                        elif j == "<":
                            lines_new.append("<symbol> &lt; <symbol>\n")
                        else:
                            lines_new.append(f"<keyword> {j} <keyword>\n")


    file = open(file_path, 'r')
    lines = file.readlines()
    file.close()

    lines_new = []
    remove_whitespace_and_labels()

    return lines_new

def code(parsed_lines, filename):

    xml_file = open(filename + (".xml"), "a")

    for i in parsed_lines:
        for j in i:
            xml_file.write(j);

def hack_assembler():
    #if len(sys.argv) != 2:
    #    print("Usage: python jack_compiler.py <filename>")
    #    return
    
    #filename = sys.argv[1]

    parsed_lines = parser("Main.jack")
    code(parsed_lines, "Main")

hack_assembler()

