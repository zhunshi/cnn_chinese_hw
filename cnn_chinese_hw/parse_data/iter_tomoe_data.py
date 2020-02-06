from input.toolkit.io.file_tools import file_iter


def iter_tomoe_data(path):
    """
    Open the Tomoe handwriting data at path
    """
    cur_char = None
    LStrokes = []
    LCurStroke = []

    for line in file_iter(path):
        line = line.strip()
        
        if line.startswith('<utf8>'):
            if cur_char:
                if LCurStroke:
                    LStrokes.append(LCurStroke)
                    LCurStroke = []
                
                yield ord(cur_char), LStrokes
                LStrokes = []
            
            char = line.split('<utf8>&#x')[1].split(';')[0]
            char = int(char, 16)
            cur_char = chr(char)
        
        elif line.startswith('<stroke>'):
            if LCurStroke:
                LStrokes.append(LCurStroke)
                LCurStroke = []
        
        elif line.startswith('<point'):
            x = line.split('x="')[1].split('"')[0]
            y = line.split('y="')[1].split('"')[0]
            x = int(x)
            y = int(y)
            LCurStroke.append((x, y))

    if cur_char:
        if LCurStroke:
            LStrokes.append(LCurStroke)

        yield ord(cur_char), LStrokes