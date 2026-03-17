from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    loan_count = fields.Integer(
        string='Numero de prestamos',
        compute="_compute_loan_amount",
        store=True
    )
    total_loan_amount = fields.Float(
        string='Monto total de prestamos',
        compute="_compute_total_loan_amount",
        store=True
    ) #calculado
    #relacion inversa para calcular loan_count y total_loan_amount
    loan_ids = fields.One2many(
        comodel_name='loan.application',
        inverse_name='partner_id',
        string='Prestamos'
    )

    @api.depends('loan_ids')
    def _compute_loan_amount(self):
        for rec in self:
            rec.loan_count = len(rec.loan_ids)

    @api.depends('loan_ids.loan_amount')
    def _compute_total_loan_amount(self):
        for rec in self:
            rec.total_loan_amount = sum(rec.loan_ids.mapped('loan_amount'))


