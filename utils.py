# def list_to_int(list_result):
#     for s in list_result:
#         string_result = ''.join(str(e) for e in list_result)
#         string_result = string_result.replace('(', '')
#         string_result = string_result.replace(')', '')
#         string_result = string_result.replace(',', '')
#         string_result = int(string_result)
#         #string_result = string_result.append(s)
#     return string_results


def list_to_int(list_result):
    string_result = ''.join(str(e) for e in list_result)
    string_result = string_result.replace('(', '')
    string_result = string_result.replace(')', '')
    string_result = string_result.replace(',', '')
    string_result = int(string_result)
    #string_result = string_result.append(s)
    return string_result


def list_to_str(list_result):
    string_result = ''.join(str(e) for e in list_result)
    string_result = string_result.replace('(', '')
    string_result = string_result.replace(')', '')
    string_result = string_result.replace(',', '')
    string_result = string_result.replace("'", '')
    #string_result = string_result.append(s)
    return string_result
