from utils.exts import db
from utils.logger import logger
from utils.errors import BaseError
import traceback

import time


def query_collection(obj_type, collection, field):
    session = db()
    try:
        objects = session.query(obj_type).filter(obj_type.id.in_(collection)).all()
    except Exception as e:
        session.close()
        logger.error(e)
        raise BaseError("查询失败", status_code=500)
    res = []
    for obj in objects:
        obj_dict = {}
        for column in field:
            if type(column) == str:
                obj_dict[column] = obj.__getattribute__(column)
            if type(column) == dict:
                column_name = column.get('name', None)
                if column_name is None:
                    session.close()
                    logger.error("缺少列名")
                    raise BaseError("缺少列名", status_code=500)
                if column.get('serializer', None):
                    if column['serializer'] == 'date':
                        obj_dict[column_name] = '' if obj.__getattribute__(column_name) is None else\
                            obj.__getattribute__(column_name).strftime('%Y-%m-%d')
                    elif column['serializer'] == 'datetime':
                        obj_dict[column_name] = '' if obj.__getattribute__(column_name) is None else\
                            obj.__getattribute__(column_name).strftime('%Y-%m-%d %H:%M:%S')
                    elif column['serializer'] == 'relation':
                        obj_dict[column_name] = [] if obj.__getattribute__(column_name) is None else\
                            [item.id for item in obj.__getattribute__(column_name).all()]
                    elif callable(column['serializer']):
                        obj_dict[column_name] = column['serializer'](obj.__getattribute__(column_name))
                    else:
                        session.close()
                        raise BaseError("缺少序列器", status_code=500)
        res.append(obj_dict)
    session.close()
    return res


def query_objects(obj_type, query, field):
    session = db()
    try:
        objects = session.query(obj_type).filter_by(**query).all()
    except Exception as e:
        session.close()
        traceback.format_exc()
        traceback.print_exc()
        logger.error(e)
        raise BaseError("查询失败", status_code=500)
    res = []
    for obj in objects:
        obj_dict = {}
        for column in field:
            if type(column) == str:
                obj_dict[column] = obj.__getattribute__(column)
            if type(column) == dict:
                column_name = column.get('name', None)
                if column_name is None:
                    session.close()
                    logger.error("缺少列名")
                    raise BaseError("缺少列名", status_code=500)
                if column.get('serializer', None):
                    if column['serializer'] == 'date':
                        obj_dict[column_name] = '' if obj.__getattribute__(column_name) is None else\
                            obj.__getattribute__(column_name).strftime('%Y-%m-%d')
                    elif column['serializer'] == 'datetime':
                        obj_dict[column_name] = '' if obj.__getattribute__(column_name) is None else\
                            obj.__getattribute__(column_name).strftime('%Y-%m-%d %H:%M:%S')
                    elif column['serializer'] == 'relation':
                        obj_dict[column_name] = [] if obj.__getattribute__(column_name) is None else\
                            [item.id for item in obj.__getattribute__(column_name).all()]
                    elif callable(column['serializer']):
                        obj_dict[column_name] = column['serializer'](obj.__getattribute__(column_name))
                    else:
                        session.close()
                        raise BaseError("缺少序列器", status_code=500)
        res.append(obj_dict)
    session.close()
    return res


def create_object(obj_type, data, field):
    session = db()
    obj_data = {}
    for column in field:
        if type(column) == str:
            obj_data[column] = data[column]
        elif type(column) == dict:
            if column.get('typer', None):
                column_name = column.get('name', None)
                if column_name is None:
                    session.close()
                    logger.error("缺少列名")
                    raise BaseError("缺少列名", status_code=500)
                if column['typer'] == 'date':
                    obj_data[column_name] = None if data[column_name] is None else time.strptime(data[column_name], '%Y-%m-%d')
                elif column['typer'] == 'datetime':
                    obj_data[column_name] = None if data[column_name] is None else time.strptime(data[column_name], '%Y-%m-%d %H:%M:%S')
                elif column['typer'] == 'relation':
                    relation_obj = column.get('relation', None)
                    if relation_obj is None:
                        session.close()
                        logger.error("缺少关系类%s" % column)
                        raise BaseError("缺少关系类", status_code=500)
                    try:
                        obj_data[column_name] = session.query(relation_obj).\
                            filter(relation_obj.id.in_(data[column_name].split(','))).all()
                    except Exception as e:
                        session.close()
                        logger.error(e)
                        raise BaseError("查询相关数据时出错", status_code=500)
                elif callable(column['typer']):
                    obj_data[column_name] = column['typer'](data[column_name])
    new_obj = obj_type(**obj_data)
    print(obj_data)
    session.add(new_obj)
    try:
        session.commit()
    except Exception as e:
        traceback.format_exc()
        traceback.print_exc()
        session.close()
        logger.error(e)
        raise BaseError("存储数据时发生错误", status_code=500)
    session.close()


def modify_obj(obj_type, query, data, field):
    session = db()
    try:
        obj = session.query(obj_type).filter_by(**query).first()
    except Exception as e:
        session.close()
        logger.error(e)
        raise BaseError("查询失败", status_code=500)
    if obj is None:
        session.close()
        raise BaseError("没有找到符合条件的数据", status_code=404)
    for column in field:
        if type(column) == str:
            obj.__setattr__(column, '' if data[column] == '' else (data[column] or obj.__getattribute__(column)))
        elif type(column) == dict:
            if column.get('typer', None):
                column_name = column.get('name', None)
                if column_name is None:
                    session.close()
                    logger.error("缺少列名")
                    raise BaseError("缺少列名", status_code=500)
                if column['typer'] == 'date':
                    obj.__setattr__(column_name,
                                    obj.__getattribute__(column_name) if data[column_name] is None else
                                        time.strptime(data[column_name], '%Y-%m-%d'))
                elif column['typer'] == 'datetime':
                    obj.__setattr__(column_name,
                                    obj.__getattribute__(column_name) if data[column_name] is None else
                                    time.strptime(data[column_name], '%Y-%m-%d %H:%M:%S'))
                elif column['typer'] == 'relation':
                    relation_obj = column.get('relation', None)
                    if relation_obj is None:
                        session.close()
                        logger.error("缺少关系类%s" % column)
                        raise BaseError("缺少关系类", status_code=500)
                    try:
                        obj.__setattr__(column_name, obj.__getattribute__(column_name)
                                        if data[column_name] is None else session.query(relation_obj).
                                        filter(relation_obj.id.in_(data[column_name].split(','))).all())
                    except Exception as e:
                        session.close()
                        logger.error(e)
                        raise BaseError("查询相关数据时出错", status_code=500)
                elif callable(column['typer']):
                    obj.__setattr__(column_name, column['typer'](data[column_name]) or
                                    obj.__getattribute__(column_name))
    try:
        session.commit()
    except Exception as e:
        session.close()
        logger.error(e)
        raise BaseError("修改数据时发生错误", status_code=500)
    session.close()


def delete_obj(obj_type, query):
    session = db()
    try:
        obj = session.query(obj_type).filter_by(**query).first()
    except Exception as e:
        session.close()
        logger.error(e)
        raise BaseError("查询失败", status_code=500)
    if obj is None:
        session.close()
        raise BaseError("没有找到符合条件的数据", status_code=404)
    session.delete(obj)
    try:
        session.commit()
    except Exception as e:
        session.close()
        logger.error(e)
        raise BaseError("删除数据时发生错误", status_code=500)
    session.close()
