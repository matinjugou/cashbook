from utils.models import *
from utils.exts import engine, db
from utils.logger import logger
from utils.errors import *
from utils.crud import *
import settings

import xlsxwriter
import json
import jwt

import io
from flask import Response, json

Base.metadata.create_all(engine)


def check_input(input_dict):
    missed_key = []
    for key in input_dict:
        if input_dict[key] == 'missed':
            missed_key.append(key)
    if len(missed_key) > 0:
        logger.error('缺少参数%s' % ','.join(missed_key))
        raise BaseError('缺少参数%s' % ','.join(missed_key), status_code=400)


def sign_token(exp):
    payload = {
        'iat': int(time.time()),
        'exp': int(time.time()) + exp * 60,
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm='HS256').decode()


def verify_token(token):
    try:
        jwt.decode(token, settings.jwt_secret, algorithms='HS256')
        return True
    except Exception as e:
        logger.error(e)
        return False


def make_json_response(data):
    return Response(json.dumps(data), content_type='application/json')


def create_pingqiaoxiang_workbook(data):
    out_io = io.BytesIO()
    workbook = xlsxwriter.Workbook(out_io)
    worksheet = workbook.add_worksheet(data['accounting_date'])
    worksheet.set_paper(9)
    worksheet.center_horizontally()
    worksheet.set_row(0, 70)
    worksheet.set_column('A:A', 10)
    worksheet.set_column('B:B', 50)
    worksheet.set_column('C:C', 10)
    worksheet.set_column('D:D', 14)
    worksheet.set_column('E:E', 14)
    worksheet.set_column('F:F', 17)
    worksheet.set_column('G:G', 17)
    title_format = workbook.add_format({
        "font_name": "华文楷体",
        "font_size": 24,
        "align": "center",
        "valign": "vcenter",
    })
    title_format.set_text_wrap()
    worksheet.merge_range(0, 0, 0, 6, data['title'], title_format)
    header_format = workbook.add_format({
        "bold": True,
        "font_name": "仿宋",
        "font_size": 20,
        "border": 1,
        "align": "center",
        "valign": "vcenter",
    })
    worksheet.set_row(1, 50)
    worksheet.write_row('A2',
                        ['日期', '工程名称', '单位', '数量', '单价', '金额', '备注'],
                        header_format)
    cell_format = workbook.add_format({
        "font_name": "仿宋",
        "font_size": 20,
        "border": 1,
        "align": "center",
        "valign": "vcenter",
    })
    cell_format.set_text_wrap()
    content = json.loads(data['content'])
    row = 3
    for item in content['items']:
        worksheet.set_row(row - 1, 50)
        worksheet.write_row('A%d' % row,
                            [item['date'],
                             item['name'],
                             item['unit'],
                             item['count'],
                             item['price'],
                             item['amount'],
                             item['backup']],
                            cell_format)
        row += 1
    row -= 1
    worksheet.set_row(row, 50)
    worksheet.merge_range(2, 6, row, 6, '', cell_format)
    worksheet.write(row, 0, '合计', cell_format)
    worksheet.merge_range(row, 1, row, 4, content['amount_chies'], cell_format)
    worksheet.write(row, 5, content['amount'], cell_format)
    worksheet.write(row, 6, '', cell_format)
    row += 2
    date_data = data['accounting_date'].split('-')
    worksheet.set_row(row, 50)
    time_cell_format = workbook.add_format({
        "font_size": 20,
        "align": "center",
        "valign": "vcenter",
    })
    worksheet.write(row, 5, date_data[0] + '年' + date_data[1] + '月' + date_data[2] + '日', time_cell_format)
    worksheet.fit_to_pages(1, 1)
    workbook.close()
    out_io.seek(0)
    return out_io.getvalue()


def create_xiaohuashan_workbook(data):
    out_io = io.BytesIO()
    workbook = xlsxwriter.Workbook(out_io)
    worksheet = workbook.add_worksheet(data['accounting_date'])
    date_data = data['accounting_date'].split('-')
    month_word = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '十一', '十二']
    worksheet.center_horizontally()
    worksheet.set_paper(9)
    worksheet.set_row(0, 70)
    worksheet.set_column('A:A', 10)
    worksheet.set_column('B:B', 10)
    worksheet.set_column('C:C', 120)
    content = json.loads(data['content'])
    title_format = workbook.add_format({
        "font_name": "宋体",
        "bold": True,
        "font_size": 24,
        "align": "left",
        "valign": "bottom",
    })
    title_format.set_text_wrap()
    worksheet.merge_range(0, 0, 0, 2, '裕安支队小华山大队%s月份市容环境整治情况' % month_word[int(date_data[1]) - 1],
                          title_format)
    header_format = workbook.add_format({
        "font_name": "宋体",
        "font_size": 14,
        "border": 1,
        "align": "center",
        "valign": "vcenter",
    })
    cell_format = workbook.add_format({
        "font_name": "宋体",
        "font_size": 14,
        "border": 1,
        "align": "left",
        "valign": "vcenter",
    })
    cell_format.set_text_wrap()
    worksheet.set_row(1, 40)
    worksheet.set_row(2, 40)
    worksheet.set_row(3, 40)
    worksheet.set_row(4, 40)
    worksheet.set_row(5, 40)
    worksheet.set_row(6, 80)
    worksheet.set_row(7, 80)
    worksheet.set_row(8, 40)
    worksheet.set_row(9, 40)
    worksheet.merge_range(1, 0, 1, 1, '整治项目', header_format)
    worksheet.merge_range(2, 0, 2, 1, '时间', header_format)
    worksheet.merge_range(3, 0, 3, 1, '地点', header_format)
    worksheet.merge_range(4, 0, 4, 1, '参与人数', header_format)
    worksheet.merge_range(5, 0, 5, 1, '投入机械设备', header_format)
    worksheet.merge_range(6, 0, 7, 0, '经费', header_format)
    worksheet.write(6, 1, '材料机械', header_format)
    worksheet.write(7, 1, '人工', header_format)
    worksheet.merge_range(8, 0, 8, 1, '其他', header_format)
    worksheet.merge_range(9, 0, 9, 1, '合计', header_format)
    worksheet.write_column('C2', [
        content['project'],
        date_data[0] + '年' + date_data[1] + '月' + date_data[2] + '日',
        content['position'],
        content['employee'],
        content['device'],
        content['cost_device'],
        content['cost_employee'],
        content['other'],
        '合计' + content['amount_chies'] + '    计' + str(content['amount']) + '元'
    ], cell_format)
    worksheet.set_landscape()
    worksheet.fit_to_pages(1, 1)
    workbook.close()
    out_io.seek(0)
    return out_io.getvalue()


def create_chengnanzhne_workbook(data):
    out_io = io.BytesIO()
    workbook = xlsxwriter.Workbook(out_io)
    worksheet = workbook.add_worksheet(data['accounting_date'])
    worksheet.center_horizontally()
    worksheet.set_paper(9)
    worksheet.set_row(0, 70)
    worksheet.set_column('A:A', 80)
    content = json.loads(data['content'])
    title_format = workbook.add_format({
        "font_name": "微软雅黑",
        "font_size": 24,
        "align": "center",
        "valign": "vcenter",
    })
    title_format.set_text_wrap()
    worksheet.write(0, 0, '城南镇文明创建临时用工用车申报单', title_format)
    cell_format = workbook.add_format({
        "font_name": "仿宋",
        "font_size": 15,
        "border": 1,
        "align": "left",
        "valign": "top",
    })
    cell_format.set_text_wrap()
    worksheet.set_row(1, 80)
    worksheet.set_row(2, 40)
    worksheet.set_row(3, 340)
    worksheet.set_row(4, 120)
    worksheet.set_row(5, 80)
    worksheet.write(1, 0, '申报事项：%s' % content['cause'], cell_format)
    worksheet.write(2, 0, '申报时间：%s年%s月%s日%s时  至  %s年%s月%s日%s时'
                    % (content['start_time'][0], content['start_time'][1], content['start_time'][2],
                       content['start_time'][3],
                       content['end_time'][0], content['end_time'][1], content['end_time'][2],
                       content['end_time'][3]),
                    cell_format)
    content_text = '申报内容：\n\r1、车辆：\n\r'
    for item in content['vehicle_items']:
        content_text += '%s，%s辆，%s元；\n\r' % (item['name'], item['count'], item['amount'])
    content_text += '2、工人：\n\r'
    for item in content['employee_items']:
        content_text += '%s%s人，%s元；\n\r' % (item['name'], item['count'], item['amount'])
    content_text += '3、机械：\n\r'
    for item in content['device_items']:
        content_text += '%s，%s元；\n\r' % (item['name'], item['amount'])
    content_text += '\n\r\n\r合计：%s元' % str(content['amount'])
    worksheet.write(3, 0, '%s' % content_text, cell_format)
    worksheet.write(4, 0, '\n\r申报人：______________，______________（签字）\n\r\n\r审核人：______________（签字）', cell_format)
    worksheet.write(5, 0, '备注：%s' % content['amount_chies'], cell_format)
    worksheet.fit_to_pages(1, 1)
    workbook.close()
    out_io.seek(0)
    return out_io.getvalue()

