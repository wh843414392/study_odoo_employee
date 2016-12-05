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
    allot_start_date = fields.Integer('Set.Time', store=True, compute='settime')
    allot_study_date = fields.One2many('st.allot', 'employee_id')
    '''请假数记录字段'''
    leave_ids = fields.One2many('allot.leave.record', 'record_id')
    '''active'''
    active = fields.Boolean('active', default=True)

    @api.multi
    @api.depends('leave_ids', 'allot_study_date', 'allot_study_date.state', 'allot_study_date.employee_id',
                 'allot_study_date.allot_id_time')
    def settime(self):
        '''计算发假'''

        for employee in self:
            employee_allot = self.env['st.allot'].search(
                ['&', ('employee_id', '=', employee.id), ('state', '=', 'done')])
            allot_record_date = 0
            for allot_record in employee_allot:
                allot_record_date += allot_record.allot_id_time
            employee.allot_start_date = allot_record_date
            record_date = self.env['allot.leave.record'].search([('record_id', '=', employee.id)])
            leave_record_date = 0
            for allot_record in record_date:
                leave_record_date += allot_record.record_date
            employee.allot_start_date = employee.allot_start_date - leave_record_date
        if self.allot_start_date < 0:
            raise ValidationError("你已经没有发假时间!")



    @api.multi
    def unlink(self):
        self.active = False
