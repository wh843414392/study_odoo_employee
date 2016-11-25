# -*- encoding: utf-8 -*-
import datetime
from openerp import _, api, fields, models
from openerp.exceptions import ValidationError, UserError


class StAllotLeave(models.Model):
    '''
    请假单
    '''
    _name = 'st.allot.leave'
    _description = 'Allot Leave'

    '''员工'''
    employee_window_id = fields.Many2one('st.employee')
    '''请假数'''
    leave_window_time = fields.Integer('Leave.Time')

    @api.multi
    def button_allot_leave_code(self):

        now = datetime.datetime.now().strftime('%H:%M:%S')
        for leave in self:
            '''如果总发假小于请假'''

            if leave.leave_window_time > leave.employee_window_id.allot_start_date:
                raise ValidationError("发假天数不足以请假，不能请假!")

            self.env['allot.leave.record'].create({'record_id': leave.employee_window_id.id,
                                                   'record_date': leave.leave_window_time,
                                                   'record_datetime': now})
