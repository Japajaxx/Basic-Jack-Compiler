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


    indentLayer = []
    indent = "  "
    indendNum = 0
    inClass = False
    funcDec = False
    inState = False
    expressionOn = False
    inIf = False

    for i in parsed_lines:
        xml_file_T.write(i);

        if i != "<tokens>\n" and i != "</tokens>\n":

            if i == "<keyword> class </keyword>\n":
                inClass = True
                xml_file.write((indent * indendNum) + "<class>\n")
                indendNum += 1
                xml_file.write((indent * indendNum) + i)
                indentLayer.append("</class>\n")

            elif i == "<keyword> static </keyword>\n" or i == "<keyword> var </keyword>\n":
                if inClass:
                    xml_file.write((indent * indendNum) + "<classVarDec>\n")
                    indentLayer.append("</classVarDec>\n")
                else:
                    xml_file.write((indent * indendNum) + "<varDec>\n")
                    indentLayer.append("</varDec>\n")
                indendNum += 1
                xml_file.write((indent * indendNum) + i)
                
            elif i == "<symbol> ; </symbol>\n":
                xml_file.write((indent * indendNum) + i)
                indendNum += -1
                xml_file.write((indent * indendNum) + indentLayer[-1])
                indentLayer.pop()
            
            elif i == "<keyword> function </keyword>\n":
                xml_file.write((indent * indendNum) + "<subroutineDec>\n")
                indendNum += 1
                indentLayer.append("</subroutineDec>\n")
                funcDec = True
                inClass = False
                xml_file.write((indent * indendNum) + i)

            elif i == "<symbol> ( </symbol>\n":
                xml_file.write((indent * indendNum) + i)
                if funcDec:    
                    xml_file.write((indent * indendNum) + "<parameterList>\n")
                    indentLayer.append("</parameterList>\n")
                elif inIf:
                    xml_file.write((indent * indendNum) + "<expression>\n")
                    indendNum += 1
                    xml_file.write((indent * indendNum) + "<term>\n")
                    expressionOn = True
                else:
                    xml_file.write((indent * indendNum) + "<expressionList>\n")
                    indentLayer.append("</expressionList>\n")
                indendNum += 1
                
            elif i == "<symbol> ) </symbol>\n":
                if not inIf:
                    indendNum -= 1
                    xml_file.write((indent * indendNum) + indentLayer[-1])
                    indentLayer.pop()
                xml_file.write((indent * indendNum) + i)

            elif i == "<symbol> { </symbol>\n":
                if funcDec:
                    xml_file.write((indent * indendNum) + "<subroutineBody>\n")
                    indentLayer.append("</subroutineBody>\n")
                    indendNum += 1
                    funcDec = False
                    xml_file.write((indent * indendNum) + i)
                elif inIf:
                    xml_file.write((indent * indendNum) + i)
                    xml_file.write((indent * indendNum) + "<statements>\n")
                    indentLayer.append("</statements>\n")
                else:
                    xml_file.write((indent * indendNum) + i)


            elif i == "<symbol> } </symbol>\n":
                if indentLayer:
                    if indentLayer[-1] == "</statements>\n":
                        indendNum -= 1
                        xml_file.write((indent * indendNum) + indentLayer[-1])
                        indentLayer.pop()
                    xml_file.write((indent * indendNum) + i)
                    if not inIf:
                        indendNum -= 1
                    xml_file.write((indent * indendNum) + indentLayer[-1])
                    indentLayer.pop()

                if indentLayer:
                    if indentLayer[-1] == "</subroutineDec>\n":
                        indendNum -= 1
                        xml_file.write((indent * indendNum) + indentLayer[-1])
                        indentLayer.pop()

            
            elif i == "<keyword> let </keyword>\n" or i == "<keyword> if </keyword>\n":
                inState = True
                xml_file.write((indent * indendNum) + "<statements>\n")
                indentLayer.append("</statements>\n")
                indendNum += 1

                if i == "<keyword> let </keyword>\n":
                    xml_file.write((indent * indendNum) + "<letStatement>\n")
                    indentLayer.append("</letStatement>\n")
                elif i == "<keyword> if </keyword>\n":
                    xml_file.write((indent * indendNum) + "<ifStatement>\n")
                    indentLayer.append("</ifStatement>\n")
                    inIf = True

                indendNum += 1
                xml_file.write((indent * indendNum) + i)

            elif i == "<symbol> = </symbol>\n":
                xml_file.write((indent * indendNum) + i)
                if inState:
                    xml_file.write((indent * indendNum) + "<expression>\n")
                    indendNum += 1
                    xml_file.write((indent * indendNum) + "<term>\n")
                    indendNum += 1
                    expressionOn = True

            elif i == "<keyword> do </keyword>\n":
                xml_file.write((indent * indendNum) + "<doStatement>\n")
                indendNum += 1
                xml_file.write((indent * indendNum) + i)
                indentLayer.append("</doStatement>\n")

            elif i =="<keyword> return </keyword>\n":
                xml_file.write((indent * indendNum) + "<returnStatement>\n")
                indendNum += 1
                xml_file.write((indent * indendNum) + i)
                indentLayer.append("</returnStatement>\n")

            elif expressionOn:
                xml_file.write((indent * indendNum) + i)
                indendNum -= 1
                xml_file.write((indent * indendNum) + "</term>\n")
                indendNum -= 1
                xml_file.write((indent * indendNum) + "</expression>\n")
                expressionOn = False

            else:
                xml_file.write((indent * indendNum) + i)

        
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

