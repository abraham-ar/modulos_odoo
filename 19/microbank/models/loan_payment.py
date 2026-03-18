from odoo import models, fields

class LoanPayment(models.Model):
    _name = 'loan.payment'
    _description = 'Pago de prestamo'

    loan_id = fields.Many2one(
        comodel_name='loan.application',
        string='Loan'
    )
    payment_date = fields.Datetime(
        string='Fecha de Pago'
    )
    amount = fields.Float(
        string='Monto pagado'
    )
    state = fields.Selection(
        string='Estado del pago',
        selection=[('borrador','Borrador'), ('confirmado', 'Confirmado'),
                   ('cancelado', 'Cancelado')],
        default='borrador'
    )

    def action_confirmar(self):
        for rec in self:
            rec.state = 'confirmado'

    def action_cancelar(self):
        for rec in self:
            rec.state = 'cancelado'