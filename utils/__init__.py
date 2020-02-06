from utils.models import *
from utils.exts import engine, db
from utils.logger import logger
from utils.errors import *
from utils.crud import *
import settings

import xlwt
import xlsxwriter
import json
import io
import mimetypes

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
    worksheet.center_horizontally()
    worksheet.center_vertically()
    worksheet.set_paper(9)
    worksheet.set_row(0, 70)
    worksheet.set_column('A:A', 15)
    worksheet.set_column('B:B', 15)
    worksheet.set_column('C:C', 100)
    title_format = workbook.add_format({
        "font_name": "宋体",
        "bold": True,
        "font_size": 24,
        "align": "center",
        "valign": "vcenter",
    })
    title_format.set_text_wrap()
    worksheet.merge_range(0, 0, 0, 2, data['title'], title_format)
    header_format = workbook.add_format({
        "font_name": "宋体",
        "font_size": 20,
        "border": 1,
        "align": "center",
        "valign": "vcenter",
    })
    cell_format = workbook.add_format({
        "font_name": "宋体",
        "font_size": 20,
        "border": 1,
        "align": "left",
        "valign": "vcenter",
    })
    cell_format.set_text_wrap()
    worksheet.set_row(1, 50)
    worksheet.set_row(2, 50)
    worksheet.set_row(3, 50)
    worksheet.set_row(4, 50)
    worksheet.set_row(5, 50)
    worksheet.set_row(6, 50)
    worksheet.set_row(7, 50)
    worksheet.set_row(8, 50)
    worksheet.set_row(9, 50)
    worksheet.merge_range(1, 0, 1, 1, '整治项目', header_format)
    worksheet.merge_range(2, 0, 2, 1, '时间', header_format)
    worksheet.merge_range(3, 0, 3, 1, '地点', header_format)
    worksheet.merge_range(4, 0, 4, 1, '参与人数', header_format)
    worksheet.merge_range(5, 0, 5, 1, '投入机械设备', header_format)
    worksheet.merge_range(6, 0, 7, 0, '经费', header_format)
    worksheet.write(6, 1, '材料机械', header_format)
    worksheet.write(7, 1, '人工', header_format)
    worksheet.merge_range(8, 0, 8, 1, '误餐情况', header_format)
    worksheet.merge_range(9, 0, 9, 1, '合计', header_format)
    content = json.loads(data['content'])
    date_data = data['accounting_date'].split('-')
    worksheet.write_column('C2', [
        content['project'],
        date_data[0] + '年' + date_data[1] + '月' + date_data[2] + '日',
        content['position'],
        content['employee'],
        content['device'],
        content['cost_device'],
        content['cost_employee'],
        content['other'],
        '合计' + content['amount_chies'] + '    ' + content['amount'] + '元'
    ], cell_format)
    worksheet.set_landscape()
    worksheet.fit_to_pages(1, 1)
    workbook.close()
    out_io.seek(0)
    return out_io.getvalue()
