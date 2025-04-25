#Call with "python jack_compiler.py <filename>"

import sys
import os

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
           "|",
           "~"]

keywords = ["class",
            "method",
            "function",
            "void",
            "static",
            "boolean",
            "field",
            "constructor",
            "var",
            "int",
            "char",
            "let",
            "if",
            "else",
            "while",
            "do",
            "true",
            "false",
            "null",
            "this",
            "return"]

comp = {"<": "&lt;",
        ">": "&gt;",
        "&": "&amp;"}

def parser(file_path):

    def token():
        lines_new.append(f"<tokens>\n")
        for i in lines:
            if i[0] != "\n" and i[0] != "/" and i != "	\n" and i[0] != "*":
                if "//" in i:
                    i = i.split("//")[0]

                if "/**" in i:
                    i = i.split("/**")[0]

                if "*" in i:
                    i= i.strip()
                    if i[0] == "*":
                        continue


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
    token()

    return lines_new
            

def code(parsed_lines, filename):

    xml_file_T = open(filename + ("T.xml"), "a")
    xml_file = open(filename + (".xml"), "a")

    indent = "  "
    indendNum = 0

    for i in parsed_lines:
        xml_file_T.write(i);
        if "token" in i:
            continue
        if "class" in i:
            xml_file.write("<class>\n")
            indendNum += 1
        xml_file.write((indendNum * indent) + i)
        
    xml_file_T.close()
    xml_file.close()
        

def hack_assembler():
    if len(sys.argv) != 2:
        print("Usage: python jack_compiler.py <folder_path>")
        return
    
    folder_path = sys.argv[1]

    if not os.path.isdir(folder_path):
        print(f"Error: {folder_path} is not a valid directory.")
        return

    for filename in os.listdir(folder_path):
        if filename.endswith(".jack"):
            file_path = os.path.join(folder_path, filename)
            parsed_lines = parser(file_path)
            code(parsed_lines, os.path.splitext(file_path)[0])

hack_assembler()

