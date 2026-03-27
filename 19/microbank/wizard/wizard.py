from odoo import api, fields, models

class LoanApplication(models.TransientModel):
    _name = 'loan.application.change.state'

    loan_ids = fields.Many2many(
        comodel_name='loan.application',
        string="Prestamos para aprobar o rechazar",
        default=lambda self: [(6, 0, self.env.context.get('active_ids', []))]
    )

    action = fields.Selection(
        selection=[('aprobar', 'Aprobar'), ('rechazar', 'Rechazar')],
    )

    def action_aprobar(self):
        for rec in self.loan_ids:
            rec.state = 'aprobado'

    def action_rechazar(self):
        for rec in self.loan_ids:
            rec.state = 'rechazado'