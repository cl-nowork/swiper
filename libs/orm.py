from datetime import date, datetime

from django.db.models import QuerySet, Model

from libs.cache import rds
from commons.keys import MODEL_KEY_FORMAT


def get(self, *args, **kwargs):
    '''给get添加了缓存层功能'''
    pk = kwargs.get('pk') or kwargs.get('id') or kwargs.get('session_key')
    if pk is not None:
        # 检查从缓存中获取
        key = MODEL_KEY_FORMAT % (self.model.__name__, pk)
        model_obj = rds.get(key)
        if isinstance(model_obj, self.model):
            print('从缓存中获取数据')
            return model_obj
    # 从数据库中获取
    model_obj = self._get(*args, **kwargs)
    print('从数据中获取数据')
    # 存入缓存
    key = MODEL_KEY_FORMAT % (self.model.__name__, pk)
    rds.set(key, model_obj)
    print('将数据存入缓存')
    return model_obj


def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    '''给save添加缓存层'''
    # 存入数据库
    self._save(force_insert, force_update, using, update_fields)
    # 修改缓存
    key = MODEL_KEY_FORMAT % (self.__class__.__name__, self.pk)
    rds.set(key, self)


def to_dict(self, *exclude_fields):
    '''序列化器'''
    attr_dict = {}
    for field in self.__class__._meta.fields:
        k = field.attname
        if k in exclude_fields:
            continue
        v = getattr(self, k)
        if isinstance(v, (date, datetime)):
            v = str(v)
        attr_dict[k] = v
    return attr_dict


def patch_orm():
    '''以monkey patch形式给orm添加缓存'''
    QuerySet._get = QuerySet.get
    QuerySet.get = get
    Model._save = Model.save
    Model.save = save
    Model.to_dict = to_dict
