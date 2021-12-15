from flask import Blueprint, Flask, jsonify, request

api = Blueprint('api', __name__)


@api.route('/2')
def index():
    return "This is an example app"


tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]


@api.route('/get', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})


@api.route('/post', methods=['POST'])
def create_task():
    # if not request.json or not 'title' in request.json:
    #     abort(400)
    doc = {
        'DOC_ID': request.json['DOC_ID'],
        'DOC_DATE': request.json['DOC_DATE'],
        'DOC_SUM': request.json['DOC_SUM'],
        'DOC_NOM': request.json['DOC_NOM'],
        'DOG_NOM': request.json['DOG_NOM'],
        'DOC_TYPE_OPL': request.json['DOC_TYPE_OPL'],
        'DOC_SUM_NAL': request.json['DOC_SUM_NAL'],
        'DOC_SUM_BNAL': request.json['DOC_SUM_BNAL'],
        'CHECK_NUM': request.json['CHECK_NUM'],
        'KAS_KOD': request.json['KAS_KOD'],
        'KAS_FIO': request.json['KAS_FIO']
    }
    tasks.append(doc)
    print(tasks)
    return jsonify({'task': doc}), 201


@api.route('/post2', methods=['POST'])
def create_task2():
    print(request.json)
    return jsonify(request.json)


@api.route('post3', methods=['POST'])
def json_example():
    request_data = request.get_json()
    # request_data = request.json

    doc_id = None
    doc_date = None
    doc_sum = None
    doc_nom = None
    dog_nom = None
    doc_type_opl = None
    doc_sum_nal = None
    doc_sum_bnal = None
    check_num = None
    kas_kod = None
    kas_fio = None

    if request_data:
        if 'DOC_ID' in request_data:
            doc_id = request_data[" DOC_ID "]

        if 'DOC_ID' in request_data:
            doc_id = request_data([" DOC_ID "])

        if 'DOC_DATE' in request_data:
            doc_date = request_data['DOC_DATE']

        if 'DOC_SUM' in request_data:
            doc_sum = request_data['DOC_SUM']

        if 'DOC_NOM' in request_data:
            doc_nom = request_data['DOC_NOM']

        if 'DOG_NOM' in request_data:
            dog_nom = request_data['DOG_NOM']

        if 'DOC_TYPE_OPL' in request_data:
            doc_type_opl = request_data['DOC_TYPE_OPL']

        if 'DOC_SUM_NAL' in request_data:
            doc_sum_nal = request_data['DOC_SUM_NAL']

        if 'DOC_SUM_BNAL' in request_data:
            doc_sum_bnal = request_data['DOC_SUM_BNAL']

        if 'CHECK_NUM' in request_data:
            check_num = request_data['CHECK_NUM']

        if 'KAS_KOD' in request_data:
            kas_kod = request_data['KAS_KOD']

        if 'KAS_FIO' in request_data:
            kas_fio = request_data['KAS_FIO']

    return '''
           doc_id value is: {}
           doc_date value is: {}
           doc_sum value is: {}
           doc_nom value is: {}
           dog_nom value is: {}
           doc_type_opl value is: {}
           doc_sum_nal value is: {}
           doc_sum_bnal value is: {}
           check_num value is: {}
           kas_kod value is: {}
           kas_fio value is: {}'''.format(doc_id, doc_date, doc_sum,
                        doc_nom, dog_nom, doc_type_opl,
                        doc_sum_nal, doc_sum_bnal,
                        check_num, kas_kod, kas_fio)


@api.route('/oplata_1c', methods=['POST'])
def oplata_1c():
    doc_id = None
    doc_date = None
    doc_sum = None
    doc_nom = None
    dog_nom = None
    doc_type_opl = None
    doc_sum_nal = None
    doc_sum_bnal = None
    check_num = None
    kas_kod = None
    kas_fio = None

    otvet_list = ([])
    dict = request.json

    for firstkey, big_list in dict.items():
        # print('print dict: ' + str(firstkey))

        if str(firstkey) == "DOC":

            status = "OK"

            for pair in big_list:
                # print('print sets in dict: ' + str(pair))
                # print(type(pair))
                nextdict = pair
                for nextkey, small_list in nextdict.items():

                    if str(nextkey) == " DOC_ID ":
                        doc_id = str(nextdict[nextkey])
                    else:
                        doc_id = "Pusto"
                    if str(nextkey) == " DOC_DATE ":
                        doc_date = str(nextdict[nextkey])
                    if str(nextkey) == " DOC_SUM ":
                        doc_sum = str(nextdict[nextkey])
                    if str(nextkey) == " DOC_NOM ":
                        doc_nom = str(nextdict[nextkey])
                    if str(nextkey) == " DOG_NOM ":
                        dog_nom = str(nextdict[nextkey])
                    if str(nextkey) == " DOC_TYPE_OPL ":
                        doc_type_opl = str(nextdict[nextkey])
                    if str(nextkey) == " DOC_SUM_NAL ":
                        doc_sum_nal = str(nextdict[nextkey])
                    if str(nextkey) == " DOC_SUM_BNAL ":
                        doc_sum_bnal = str(nextdict[nextkey])
                    if str(nextkey) == " CHECK_NUM ":
                        check_num = str(nextdict[nextkey])
                    if str(nextkey) == " KAS_KOD ":
                        kas_kod = str(nextdict[nextkey])
                    if str(nextkey) == " KAS_FIO ":
                        kas_fio = str(nextdict[nextkey])

                        otvet = ([doc_id, doc_date, doc_sum, doc_nom, dog_nom, doc_type_opl, doc_sum_nal, doc_sum_bnal, check_num, kas_kod, kas_fio])
                        print(otvet)
                        otvet_list.append(otvet)
        else:
            status = f"Error (Неверная схема данных json, должно быть 'DOC' а получил {str(firstkey)})"

    return str(f"Status = {status}, DataADD: {otvet_list}")


@api.route('/oplata_1c2', methods=['POST'])
def oplata_1c2():
    dict = request.json

    key_chek = (" DOC_ID ", " DOC_DATE ", " DOC_SUM ", " DOC_NOM ", " DOG_NOM ", " DOC_TYPE_OPL ", " DOC_SUM_NAL ", " DOC_SUM_BNAL ", " CHECK_NUM ", " KAS_KOD ", " KAS_FIO ")
    key_model = list(key_chek)
    status = ([])
    otvet_list = ([])
    for firstkey, big_list in dict.items():

        for i, pair in enumerate(big_list):
            print(pair)
            print(i)
            keys = list(pair.keys())
            list_result = ([])

            res = [x for x in key_model + keys if x not in key_model or x not in keys]

            if not res:
                print("Структура соответствует")
                status.append(f"{i} - Структура соответствует")

                for i in range(0, len(pair)):
                    list_result.append(pair[key_model[i]])

            else:
                print(f"Структура НЕ соответствует по ячейкам {res} у массива: {str(pair)}")
                status.append(f"{i} - Структура НЕ соответствует по ячейкам {res} у массива: {str(pair)}")
            otvet_list.append(list_result)
        print(otvet_list)

    return (f"Status = {status}, DataADD: {otvet_list}")


