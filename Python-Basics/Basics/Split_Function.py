def mysplit(string) :   
    
    result = []
    word = ''
    space = ' '
    
    string = string.strip()
    if string == word:
        string = []
        return string
    
    elif string.isspace() == False:
        string = [string]
        return string    
    
    for c in string:
        if c == space:
            result.append(word)
            word =''
        elif c:
            word = word + c

    if word:
        result.append(word)

    return result

print(mysplit("To be or not to be, that is the question"))
print(mysplit("To be or not to be,that is the question"))
print(mysplit("   "))
print(mysplit(" abc "))
print(mysplit(""))