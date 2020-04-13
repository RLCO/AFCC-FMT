# -*- coding: utf-8 -*-

from odoo import models, fields, api,_


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    transportation_id = fields.Many2one('transportation.operation')
