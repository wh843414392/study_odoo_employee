# -*- encoding: utf-8 -*-
from openerp import _, api, fields, models
from openerp.exceptions import ValidationError, UserError


class Record(models.Model):
    '''
    请假记录
    '''
    _name = 'allot.leave.record'

    '''请假时间字段'''
    code = fields.Char('Code')
    '''请假员工'''
    record_name = fields.Many2one('st.employee')

    '''请假天数字段'''
    record_time = fields.Integer('Record Time')





