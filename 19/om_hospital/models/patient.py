from odoo import models, fields


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread']
    _description = 'Patient Master'

    name = fields.Char(string='Name', required=True)
    date_of_birth = fields.Date(string='Date of Birth')
    gender = fields.Selection(selection=[('male', 'Male'), ('female', 'Female')], string='Gender')
    tags_ids = fields.Many2many('patient.tag', 'patient_tag_rel', 'patient_id', 'tag_id', string='Tags')
