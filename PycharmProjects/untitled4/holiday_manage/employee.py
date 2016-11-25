# -*- encoding: utf-8 -*-
import datetime
from openerp import _, api, fields, models
from openerp.exceptions import ValidationError, UserError


class StEmployee(models.Model):
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
    allot_start_date = fields.Integer('Set.Time', compute='settime')
    '''请假数记录字段'''
    leave_ids = fields.One2many('allot.leave.record', 'record_id')
    '''active'''
    active = fields.Boolean('active', default=True)

    @api.multi
    @api.depends('allot_start_date', 'leave_ids')
    def settime(self):
        '''计算发假'''

        for mov in self:
            send_count = sum(
                [wa.allot_id_time for wa in mov.env['st.allot'].search([('employee_id', '=', mov.id)])
                 if mov.env['st.allot'].search([('state', '=', 'done')])
                 ])

            leave_ids = sum(
                [we.record_date for we in mov.env['allot.leave.record'].search([('record_id', '=', mov.id)])])
            mov.allot_start_date = send_count - leave_ids

    @api.multi
    def unlink(self):
        self.active = False
