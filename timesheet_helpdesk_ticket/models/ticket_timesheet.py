from odoo import models, fields, api

class TicketTimesheet(models.Model):
    _inherit = 'helpdesk.ticket'

    partner_phone = fields.Char(
        string='Contact Phone',
        related='partner_id.mobile',
        store=True,
        readonly=False,
    )
    project_id = fields.Many2one(
        comodel_name='project.project',
        string='Project',
    )
    task_id = fields.Many2one(
        comodel_name='project.task',
        string='Task',
    )
    timesheet_ids = fields.One2many(
        comodel_name='account.analytic.line',
        inverse_name='ticket_id',
        string='Timesheet',
    )

    total_hours = fields.Float(
        compute='impute_hours',
    )

    @api.depends('timesheet_ids.unit_amount')
    def impute_hours(self):
        for record in self:
            record.total_hours_ticket = sum(record.timesheet_ids.mapped('unit_amount'))

    @api.constrains('project_id')
    def _constrains_project(self):
        self.task_id = False
        for record in self:
            record.timesheet_ids.update({'project_id': record.project_id.id})
            record.timesheet_ids.update({'task_id': False})

    @api.constrains('task_id')
    def _constrains_project(self):
        for record in self:
            record.timesheet_ids.update({'task_id': record.task_id.id})