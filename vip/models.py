from django.db import models


class Vip(models.Model):
    '''会员表'''
    name = models.CharField(max_length=16, unique=True, verbose_name='会员名称')
    level = models.IntegerField(default=0, verbose_name='会员等级')
    price = models.FloatField(default=0.0, verbose_name='购买会员价格')
    days = models.IntegerField(default=0, verbose_name='会员有效时长(天)')

    class Meta:
        db_table = 'vip'


class Permission(models.Model):
    '''权限表'''
    name = models.CharField(max_length=16, verbose_name='权限名称')

    class Meta:
        db_table = 'permission'


class VipPermRelation(models.Model):
    '''会员和权限的关系表'''
    vip_id = models.IntegerField(verbose_name='会员的ID')
    perm_id = models.IntegerField(verbose_name='权限的ID')

    class Meta:
        db_table = 'vippermrelation'
