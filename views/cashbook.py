from utils import *

from flask import Blueprint, request, make_response
import uuid

cashbook = Blueprint('cashbook', __name__)


@cashbook.route('', methods=['GET', 'POST', 'PUT', 'DELETE'])
def cashbook_index():
    if request.method == 'GET':
        query = {
            'id': request.args.get('id', 'missed')
        }
        check_input(query)
        res = query_objects(Cashbook, query, [
            'id', 'title', 'content', 'template',
            {'name': 'accounting_date', 'serializer': 'date'},
        ])
        return make_json_response(res)
    elif request.method == 'POST':
        data = {
            'id': 'BOOK%s' % ''.join(uuid.uuid1().__str__().split('-'))[4:],
            'title': request.form.get('title', 'missed'),
            'template': request.form.get('template', 'missed'),
            'content': request.form.get('content', 'missed'),
            'accounting_date': request.form.get('accounting_date', 'missed'),
        }
        check_input(data)
        create_object(Cashbook, data, [
            'id', 'title', 'content', 'template',
            {'name': 'accounting_date', 'typer': 'date'},
        ])
        return make_json_response({
            'data': data['id'],
            'message': '账单添加成功'
        })
    elif request.method == 'PUT':
        data = {
            'id': request.form.get('id', 'missed'),
            'title': request.form.get('title', None),
            'content': request.form.get('content', None),
            'accounting_date': request.form.get('accounting_date', None),
        }
        check_input(data)
        modify_obj(Cashbook, {'id': data['id']}, data, [
            'id', 'title', 'content',
            {'name': 'accounting_date', 'typer': 'date'},
        ])
        return make_json_response({
            'data': data['id'],
            'message': '账单信息修改成功'
        })
    elif request.method == 'DELETE':
        query = {
            'id': request.args.get('id', 'missed')
        }
        check_input(query)
        delete_obj(Cashbook, query)
        return make_json_response({
            'data': query['id'],
            'message': '账单删除成功'
        })


@cashbook.route('/list', methods=['GET'])
def cashbook_list():
    query = {
        'template': request.args.get('template', None),
    }
    if (query['template'] is None) or (query['template'] == 'all'):
        query = {}
    res = query_objects(Cashbook, query, [
        'id', 'title', 'template', {'name': 'accounting_date', 'serializer': 'date'},
    ])
    return make_json_response(res)


@cashbook.route('/outlet', methods=['GET'])
def cashbook_outlet():
    data = {
        'id': request.args.get('id', 'missed'),
    }
    check_input(data)
    res = query_objects(Cashbook, data, [
        'id', 'title', 'content', 'template',
        {'name': 'accounting_date', 'serializer': 'date'},
    ])
    book_data = res[0]
    if book_data['template'] in ['平桥乡', '西市街道']:
        response = make_response(create_pingqiaoxiang_workbook(book_data))
    else:
        response = make_response(create_xiaohuashan_workbook(book_data))
    response.headers["Content-Disposition"] = "attachment; filename={}.xlsx".format(res[0]['id'])
    response.headers['Content-Type'] = 'application/x-xlsx'
    return response
