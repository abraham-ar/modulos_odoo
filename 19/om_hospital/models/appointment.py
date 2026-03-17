from odoo import models, fields, api


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _inherit = ['mail.thread']
    _description = 'Hospital Appointment'
    _rec_name = 'patient_id'
    _rec_names_search = ['reference', 'patient_id']

    reference = fields.Char(
        string='Reference',
        default='New'
    )
    patient_id = fields.Many2one(
        comodel_name='hospital.patient',
        string='Patient'
    )
    date_appointment = fields.Date(
        string='Appointment'
    )
    note = fields.Text(
        string='Note'
    )
    state = fields.Selection(
        [('draft', 'Draft'), ('confirmed', 'Confirmed'),
         ('ongoing', 'Ongoing'), ('done', 'Done'), ('canceled', 'Canceled')],
        default='draft'
    )
    appointment_line_ids = fields.One2many(
        comodel_name='hospital.appointment.line',
        inverse_name='appointment_id',
        string='Lines'
    )

    @api.model_create_multi
    def create(self, vals_list):
        print('odoo ', vals_list)
        for vals in vals_list:
            if not vals.get('reference') or vals['reference'] == 'New':
                vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.appointment')
        return super().create(vals_list)

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirmed'

    def action_ongoing(self):
        for rec in self:
            rec.state = 'ongoing'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_cancel(self):
        for rec in self:
            rec.state = 'canceled'

class HospitalAppointmentLine(models.Model):
    _name = 'hospital.appointment.line'
    _description = 'Hospital Appointment Line'

    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product'
    )
    appointment_id = fields.Many2one(
        comodel_name='hospital.appointment',
        string='Appointment'
    )
    qty = fields.Float(string='Quantity')