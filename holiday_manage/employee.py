# -*- encoding: utf-8 -*-
import datetime
from openerp import _, api, fields, models
from openerp.exceptions import ValidationError, UserError


class Employee(models.Model):
    '''
    员工表
    '''
    _name = 'st.employee'
    _description = 'employee'
    _rec_name = 'employee_name'

    '''员工姓名字段'''
    employee_name = fields.Char('Name')
    '''是否发假字段'''
    do_allot = fields.Boolean('Do.allot', default=False)
    '''总发假时间字段'''
    allot_time = fields.Integer('Set.Time', compute='settime')
    '''请假数记录字段'''
    leave_time = fields.One2many('allot.leave.record', 'record_name')




    @api.multi
    @api.depends('allot_time', 'leave_time')
    def settime(self):
        '''计算发假'''
        for mov in self:
            send_count = sum(
                [wa.allot_id_time for wa in mov.env['st.allot'].search([('employee_id_name', '=', mov.id)])])
            leave_time = sum(
                [we.record_time for we in mov.env['allot.leave.record'].search([('record_name', '=', mov.id)])])
            mov.allot_time = send_count - leave_time




