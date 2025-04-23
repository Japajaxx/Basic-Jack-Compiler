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
           "-",
           "*",
           "/",
           "|"]

keywords = ["class",
            "function",
            "void",
            "static",
            "boolean",
            "var",
            "int",
            "let",
            "if",
            "else",
            "while",
            "do",
            "true",
            "false",
            "null",
            "return"]

comp = {"<": "&lt;"}

def parser(file_path):

    def remove_whitespace_and_labels():
        lines_new.append(f"<tokens>\n")
        for i in lines:
            if i[0] != "\n" and i[0] != "/" and i != "	\n":
                if "//" in i:
                    i = i.split("//")[0]

                while "/**" in i:
                    start = i.find("/**")
                    end = i.find("*/", start) + 2
                    if end > 1:
                        i = i[:start] + i[end:]
                    else:
                        i = i[:start]

                i = i.replace("	", "")
                temp = ""
                in_string = False
                for char in i:
                    if char == '"':
                        if in_string:
                            temp += char
                            lines_new.append(f"<stringConstant> {temp[1:-1]} </stringConstant>\n")
                            temp = ""
                            in_string = False
                        else:
                            if temp.strip():
                                if temp in keywords:
                                    lines_new.append(f"<keyword> {temp.strip()} </keyword>\n")
                                elif temp.isdigit():
                                    lines_new.append(f"<integerConstant> {temp.strip()} </integerConstant>\n")
                                elif temp in comp:
                                    lines_new.append(f"<symbol> {comp[temp]} </symbol>\n")
                                else:
                                    lines_new.append(f"<identifier> {temp.strip()} </identifier>\n")
                            temp = char
                            in_string = True
                    elif in_string:
                        temp += char
                    elif char in symbols:
                        if temp.strip():
                            if temp in keywords:
                                lines_new.append(f"<keyword> {temp.strip()} </keyword>\n")
                            elif temp.isdigit():
                                lines_new.append(f"<integerConstant> {temp.strip()} </integerConstant>\n")
                            elif temp in comp:
                                lines_new.append(f"<symbol> {comp[temp]} </symbol>\n")
                            else:
                                lines_new.append(f"<identifier> {temp.strip()} </identifier>\n")
                            temp = ""
                        lines_new.append(f"<symbol> {char} </symbol>\n")
                    elif char.isspace():
                        if temp.strip():
                            if temp in keywords:
                                lines_new.append(f"<keyword> {temp.strip()} </keyword>\n")
                            elif temp.isdigit():
                                lines_new.append(f"<integerConstant> {temp.strip()} </integerConstant>\n")
                            elif temp in comp:
                                lines_new.append(f"<symbol> {comp[temp]} </symbol>\n")
                            else:
                                lines_new.append(f"<identifier> {temp.strip()} </identifier>\n")
                            temp = ""
                    else:
                        temp += char
                if temp.strip() and not in_string:
                    if temp in keywords:
                        lines_new.append(f"<keyword> {temp.strip()} </keyword>\n")
                    elif temp.isdigit():
                        lines_new.append(f"<integerConstant> {temp.strip()} </integerConstant>\n")
                    elif temp in comp:
                        lines_new.append(f"<symbol> {comp[temp]} </symbol>\n")
                    else:
                        lines_new.append(f"<identifier> {temp.strip()} </identifier>\n")
        lines_new.append(f"</tokens>\n")

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

    parsed_lines = parser("Square.jack")
    code(parsed_lines, "Square")

hack_assembler()

