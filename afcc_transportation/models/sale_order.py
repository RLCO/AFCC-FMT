# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    sale_order_id = fields.Many2one('sale.order')
    from_id = fields.Many2one("sale.location")
    to_id = fields.Many2one("sale.location")
    departure_time = fields.Datetime()
    arrival_time = fields.Datetime()
    vehicle_id = fields.Many2one("fleet.vehicle")
    vehicle_type_id = fields.Many2one("fleet.vehicle.model")
    vehicle_no = fields.Char()
    policy_no = fields.Char('Policy No.')
    Waybill = fields.Char('Waybill')
    helper_id = fields.Many2one("hr.employee")
    driver_id = fields.Many2one("hr.employee")


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    is_driver = fields.Boolean('Driver')


class SaleOrder(models.Model):
    _inherit = "sale.order"

    from_id = fields.Many2one("sale.location")
    to_id = fields.Many2one("sale.location")
    departure_time = fields.Datetime()
    arrival_time = fields.Datetime()
    vehicle_id = fields.Many2one("fleet.vehicle")
    vehicle_type_id = fields.Many2one("fleet.vehicle.model")
    vehicle_no = fields.Char()
    policy_no = fields.Char('Policy No.')
    Waybill = fields.Char('Waybill')
    helper_id = fields.Many2one("hr.employee")
    driver_id = fields.Many2one("hr.employee")
    total_cost = fields.Float(compute="get_total_transportation_cost", store=True)
    profit = fields.Float(compute="get_profit_transportation_cost")
    transportation_cost_ids = fields.One2many('transportation.cost.line', 'transportation_cost_id', string='Transfers')
    is_journal = fields.Boolean()

    @api.constrains('arrival_time')
    def constrain_arrival_time(self):
        for record in self:
            if record.arrival_time and record.departure_time:
                if record.arrival_time < record.departure_time:
                    raise UserError(_("Arrival Time Must Be Greater Than Departure Time"))

    @api.onchange('vehicle_id')
    def onchange_vehicle_id(self):
        for record in self:
            record.vehicle_type_id = record.vehicle_id.model_id
            record.vehicle_no = record.vehicle_id.license_plate

    @api.depends('transportation_cost_ids')
    def get_total_transportation_cost(self):
        for record in self:
            record.total_cost = sum(line.amount for line in record.transportation_cost_ids)

    @api.depends('total_cost', 'amount_total')
    def get_profit_transportation_cost(self):
        for record in self:
            record.profit = record.amount_total - record.total_cost

    def action_create_journal(self):
        journal = self.env['account.move']
        journal_obj = journal.search([('sale_order_id', '=', self.id)])
        if journal_obj:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Journal Entries',
                'res_model': 'account.move',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'domain': [('sale_order_id', '=', self.id)],
                'target': 'current',
            }
        journals = []
        for record in self:
            for line in record.transportation_cost_ids:
                journals.append({
                    'journal': line.journal_id.id,
                    'account_id': line.account_id.id,
                    'name': line.description,
                    'debit': line.amount,
                    'credit': 0.0,
                    'account_id1': line.journal_id.default_credit_account_id.id,
                    'name1': line.description,
                    'debit1': 0.0,
                    'credit1': line.amount,
                    # 'analytic_account_id': emp.analytic_account.id,
                })
        print(journals)
        if journals:
            for rec in journals:
                journal_id = journal.create({
                    'journal_id': rec['journal'],
                    'sale_order_id': self.id,
                })
                journalline = self.with_context(dict(self._context, check_move_validity=False)).env['account.move.line']
                journalline.create({
                    'move_id': journal_id.id,
                    'account_id': rec['account_id'],
                    'name': rec['name'],
                    'debit': rec['debit'],
                    'credit': 0.0,
                    # 'analytic_account_id': emp.analytic_account.id,
                })
                journalline.create({
                    'move_id': journal_id.id,
                    'account_id': rec['account_id1'],
                    'name': rec['name1'],
                    'debit': 0.0,
                    'credit': rec['credit1'],
                })
            self.is_journal=True

    def action_view_invoice(self):
        res = super(SaleOrder, self).action_view_invoice()
        res['context'].update({
            'default_from_id': self.from_id.id,
            'default_to_id': self.to_id.id,
            'default_departure_time': self.departure_time,
            'default_arrival_time': self.arrival_time,
            'default_vehicle_id': self.vehicle_id.id,
            'default_vehicle_type_id': self.vehicle_type_id.id,
            'default_vehicle_no': self.vehicle_no,
            'default_policy_no': self.policy_no,
            'default_Waybill': self.Waybill,
            'default_helper_id': self.helper_id.id,
            'default_driver_id': self.driver_id.id,
        })
        return res


class TransportationCostLine(models.Model):
    _name = "transportation.cost.line"

    transportation_cost_id = fields.Many2one("sale.order")
    # vendor_id = fields.Many2one("res.partner")
    journal_id = fields.Many2one("account.journal")
    description = fields.Char()
    # vehicle_id = fields.Many2one("fleet.vehicle")
    # employee_id = fields.Many2one("hr.employee")
    product_id = fields.Many2one("product.product")
    account_id = fields.Many2one("account.account")
    amount = fields.Float()


class SaleLocation(models.Model):
    _name = "sale.location"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char()


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def create_invoices(self):
        invoice = super(SaleAdvancePaymentInv, self).create_invoices()
        sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))
        if len(sale_orders) == 1:
            account_move = self.env['account.move'].search([('invoice_origin', '=', sale_orders.name)])
            if account_move:
                account_move.update({
                    'from_id': sale_orders.from_id.id,
                    'to_id': sale_orders.to_id.id,
                    'departure_time': sale_orders.departure_time,
                    'arrival_time': sale_orders.arrival_time,
                    'vehicle_id': sale_orders.vehicle_id.id,
                    'vehicle_type_id': sale_orders.vehicle_type_id.id,
                    'vehicle_no': sale_orders.vehicle_no,
                    'policy_no': sale_orders.policy_no,
                    'Waybill': sale_orders.Waybill,
                    'helper_id': sale_orders.helper_id.id,
                    'driver_id': sale_orders.driver_id.id,
                })
        return invoice
