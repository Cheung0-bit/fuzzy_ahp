def bracketsSoup(str):
    startIndex = str.find('(') + 1
    endIndex = str.find(')')
    if endIndex == -1:
        return ''
    else:
        return str[startIndex:endIndex]