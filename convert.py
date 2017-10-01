def toPython(unicodeCode):
    python = []
    for x in unicodeCode:
        x.encode('UTF8')
        python.append(x)
    return python
