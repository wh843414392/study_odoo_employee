# -*- encoding: utf-8 -*-
from openerp import _, api, fields, models
from openerp.exceptions import ValidationError, UserError


class AllotLeaveRecord(models.Model):
    '''
    请假记录
    '''

    _name = 'allot.leave.record'

    '''请假时间字段'''

    record_datetime = fields.Char('Code.Name')
    '''请假员工'''

    record_id = fields.Many2one('st.employee')

    '''请假天数字段'''

    record_date = fields.Integer('Record Time')
