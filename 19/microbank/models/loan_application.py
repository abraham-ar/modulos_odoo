from datetime import timedelta
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta


class LoanApplication(models.Model):
    _name = 'loan.application'
    _description = 'Solicitud de prestamo'
    _rec_name = 'name'

    currency_id = fields.Many2one(
        comodel_name='res.currency',
        default=lambda self: self.env.company.currency_id
    )
    name = fields.Char(
        string='Numero de solicitud',
        default="New"
    )  # automatico
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string="Cliente"
    )
    loan_amount = fields.Monetary(
        string='Monto del préstamo',
        currency_field="currency_id"
    )
    interest_rate = fields.Float(
        string='Tasa de interés anual'
    )
    term_months = fields.Integer(
        string='Plazo en meses'
    )
    state = fields.Selection(
        string='Estado del prestamo',
        selection=[('borrador', 'Borrador'), ('aprobado', 'Aprobado'),
                   ('rechazado', 'Rechazado'), ('pagado', 'Pagado')],
        default='borrador'
    )
    monthly_payment = fields.Monetary(
        string='Pago mensual',
        currency_field="currency_id",
        compute="_compute_monthly_payment",
        store=True
    )  # calculado
    total_to_pay = fields.Monetary(
        string='Total a pagar',
        currency_field="currency_id",
        compute="_compute_total_to_pay",
        store=True
    )  # calcular
    approval_date = fields.Date(
        string='Fecha de aprobacion'
    )
    next_payment_date = fields.Date(
        string='Fecha del próximo pago'
    )
    loan_payment_ids = fields.One2many(
        comodel_name='loan.payment',
        inverse_name='loan_id',
        string='Pagos del prestamo'
    )
    progress = fields.Integer(
        string="Progreso de pago",
        compute="_compute_progress"
    )

    @api.model_create_multi
    def create(self, vals_list):
        # print('odoo ', vals_list)
        for vals in vals_list:
            if not vals.get('name') or vals['name'] == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('loan.application')
        return super().create(vals_list)

    def write(self, vals):

        old_states = {rec.id: rec.state for rec in self}

        res = super().write(vals)

        if 'state' in vals:

            for rec in self:

                old_state = old_states[rec.id]

                if old_state != rec.state:

                    if rec.state == 'aprobado':

                        template = self.env.ref(
                            'microbank.email_template_loan_approved'
                        )
                        template.send_mail(rec.id, force_send=True)

                    elif rec.state == 'rechazado':

                        template = self.env.ref(
                            'microbank.email_template_loan_rejected'
                        )
                        template.send_mail(rec.id, force_send=True)

        return res

    @api.depends('loan_amount', 'term_months', 'interest_rate', 'currency_id')
    def _compute_monthly_payment(self):
        for rec in self:
            if not rec.term_months or not rec.loan_amount:
                rec.monthly_payment = 0
            else:
                c = rec.interest_rate / 12 / 100
                n = rec.term_months
                L = rec.loan_amount

                if c == 0:
                    rec.monthly_payment = L / n
                else:
                    rec.monthly_payment = (L * (c * (1 + c) ** n)) / ((1 + c) ** n - 1)

    @api.depends('monthly_payment', 'term_months')
    def _compute_total_to_pay(self):
        for rec in self:
            rec.total_to_pay = rec.monthly_payment * rec.term_months

    @api.onchange('approval_date')
    def _onchange_approval_date(self):
        for rec in self:
            if rec.approval_date:
                rec.next_payment_date = rec.approval_date + relativedelta(months=1)

    @api.depends('total_to_pay', 'loan_payment_ids.amount')
    def _compute_progress(self):
        for rec in self:
            sum_payment = sum(rec.loan_payment_ids.mapped('amount'))
            if not rec.total_to_pay:
                rec.progress = 0
            else:
                progress = sum_payment * 100 / rec.total_to_pay
                rec.progress = progress

    def action_aprobar(self):
        for rec in self:
            #cambiar el estado del prestamo
            rec.state = 'aprobado'

            #generar el reporte PDF del contrato de prestamo
            return self.env.ref(
                'microbank.loan_application_contract_report'  # id externo de la accion
            ).report_action(self)

    def action_pagar(self):
        for rec in self:
            rec.state = 'pagado'

    def action_rechazar(self):
        for rec in self:
            rec.state = 'rechazado'
