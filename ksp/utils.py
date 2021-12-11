# (Для int) Из выборки списка удалить лишние символы и оставить только число
def list_to_list(list_result):
    for s in list_result:
        string_result = ''.join(str(e) for e in list_result)
        string_result = string_result.replace('(', '')
        string_result = string_result.replace(')', '')
        string_result = string_result.replace(',', '')
        string_result = int(string_result)
        string_result = string_result.append(s)
    return string_result
