def list_to_int(list_result):
    for s in list_result:
        string_result = ''.join(str(e) for e in list_result)
        string_result = string_result.replace('(', '')
        string_result = string_result.replace(')', '')
        string_result = string_result.replace(',', '')
        string_result = int(string_result)
        #string_result = string_result.append(s)
    return string_result