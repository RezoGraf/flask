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


@api.route('/post4', methods=['POST'])
def post4():
    dict = request.json
    for firstkey, big_list in dict.items():
        print('print dict: ' + str(firstkey))
        for pair in big_list:
            print('print sets in dict: ' + str(pair))
            nextdict = pair
            for nextkey, small_list in nextdict.items():
                print('print each: ' + str(nextkey) + '->' + str(small_list))
                # address each one
                print('pull just data: ' + str(nextdict[nextkey]))
