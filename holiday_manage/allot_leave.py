# -*- encoding: utf-8 -*-
import datetime
from openerp import _, api, fields, models
from openerp.exceptions import ValidationError, UserError


class Leave(models.Model):
    '''
    请假单
    '''
    _name = 'st.allot.leave'
    _description = 'Allot Leave'


    '''员工'''
    employee_window_name = fields.Many2one('st.employee')
    '''请假数'''
    leave_window_time = fields.Integer('Leave.Time')

    @api.multi
    def button_allot_leave_code(self):


        now = datetime.datetime.now().strftime('%H:%M:%S')
        for leave in self:
            if leave.leave_window_time > leave.employee_window_name.allot_time:
                raise ValidationError("发假天数不足以请假，不能请假!")

            self.env['allot.leave.record'].create({'record_name':leave.employee_window_name.id,
                                                   'record_time':leave.leave_window_time,
                                                   'code': now})
            self.env['res.users'].browse(self.env.uid)



