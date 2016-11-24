# -*- encoding: utf-8 -*-

from openerp import _, api, fields, models
from openerp.exceptions import ValidationError, UserError


class Text(models.Model):
    '''
    发假单
    '''
    _name = 'st.allot'

    def idname_allot(self):
        return self.env['ir.sequence'].next_by_code('st.allot')

    '''公司编号字段'''
    company_id = fields.Char('Id', readonly=True, default=idname_allot)
    '''发假员工字段'''
    employee_id_name = fields.Many2one('st.employee')
    '''发假时间字段'''
    allot_id_time = fields.Integer('Time')
    '''state'''
    state = fields.Selection([('draft', '未发假'),
                              ('done', '已发假')],
                             default='draft', string='State')

    @api.multi
    def button_write_code(self):
        self.employee_id_name.do_allot = True
        self.write({'state': 'done'})

    '''发假后删除报错'''

    @api.multi
    def button_not_write_code(self):
        self.write({'state': 'draft'})
        for allot in self:

            if allot.employee_id_name.allot_time < allot.employee_id_name.leave_time:
                raise ValidationError("发假天数小与当前已经请假天数，不准撤销!")

    @api.multi
    def unlink(self):
        raise ValidationError("报错!")
