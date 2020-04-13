# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class TransportationOperation(models.Model):
    _name = "transportation.operation"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    product_ids = fields.One2many('transportation.product.line', 'transportation_product_id')
    operation_ids = fields.One2many('transportation.operation.line', 'transportation_operation_id')
    cost_ids = fields.One2many('transportation.cost.line', 'transportation_cost_id')
    name = fields.Char()
    sale_id = fields.Many2one("sale.order")
    from_id = fields.Many2one("res.partner")
    to_id = fields.Many2one("res.partner")
    departure_time = fields.Datetime()
    arrival_time = fields.Datetime()
    distance = fields.Float()
    # payment_count = fields.Float(comute='get_payment_count', store=True)
    description = fields.Text()
    state = fields.Selection(selection=[('draft', 'draft'),
                                        ('confirmed', 'confirmed'),
                                        ('in_progress', 'in progress'),
                                        ('done', 'done'),
                                        ('cancel', 'cancel'),
                                        ])

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('transportation.seq')
        res = super(TransportationOperation, self).create(vals)
        return res

    @api.constrains('arrival_time')
    def _constrains_arrival_time(self):
        for record in self:
            if record.arrival_time < record.departure_time:
                raise UserError(_("Arrival time must be greater than departure time"))

    def action_draft(self):
        for record in self:
            record.state = 'draft'

    def action_confirmed(self):
        for record in self:
            record.state = 'confirmed'

    def action_in_progress(self):
        for record in self:
            record.state = 'in_progress'

    # @api.onchange('state')
    # @api.depends('state')
    # def get_payment_count(self):
    #     print("111111")
    #     account_payment_id = self.env['account.payment'].search_count([('transportation_id', '=', self.id)])
    #     if account_payment_id:
    #         print("222222222", account_payment_id)
    #         for record in self:
    #             print("333333333333333", account_payment_id)
    #             record.payment_count = account_payment_id

    def action_view_payment(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Payment',
            'res_model': 'account.payment',
            # 'res_id': transportation_obj.id,
            'view_type': 'form',
            'view_mode': 'tree,form',
            'domain': [('transportation_id', '=', self.id)],
            'target': 'current',
        }

    def action_done(self):
        account_payment_id = self.env['account.payment']
        for record in self:
            for line in record.cost_ids:
                account_payment_id.create({
                    'payment_type': 'outbound',
                    'partner_type': 'supplier',
                    'payment_date': fields.date.today(),
                    'partner_id': line.vendor_id.id,
                    'journal_id': line.journal_id.id,
                    'payment_method_id': 1,
                    'amount': line.amount,
                    'communication': line.description,
                    'transportation_id': record.id,
                })
            record.state = 'done'

    def action_cancel(self):
        for record in self:
            record.state = 'cancel'


class TransportationOperationLine(models.Model):
    _name = "transportation.operation.line"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "transportation_operation_id"

    transportation_operation_id = fields.Many2one("transportation.operation", 'operation')
    helper_id = fields.Many2one("hr.employee")
    driver_id = fields.Many2one("hr.employee")
    vehicle_id = fields.Many2one("fleet.vehicle")
    from_id = fields.Many2one("res.partner")
    to_id = fields.Many2one("res.partner")
    departure_time = fields.Datetime()
    arrival_time = fields.Datetime()
    distance = fields.Float()
    state = fields.Selection(selection=[('draft', 'draft'),
                                        ('confirmed', 'confirmed'),
                                        ('in_progress', 'in progress'),
                                        ('done', 'done'),
                                        ('cancel', 'cancel'),
                                        ], default='draft')


class TransportationProductLine(models.Model):
    _name = "transportation.product.line"

    transportation_product_id = fields.Many2one("transportation.operation")
    product_id = fields.Many2one("product.product")
    quantity = fields.Float()


class TransportationCostLine(models.Model):
    _name = "transportation.cost.line"

    transportation_cost_id = fields.Many2one("transportation.operation")
    vendor_id = fields.Many2one("res.partner")
    journal_id = fields.Many2one("account.journal")
    description = fields.Char()
    vehicle_id = fields.Many2one("fleet.vehicle")
    employee_id = fields.Many2one("hr.employee")
    product_id = fields.Many2one("product.product")
    amount = fields.Float()


class FleetOccurrence(models.Model):
    _name = 'fleet.occurrence'
    _rec_name = "vehicle_id"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    vehicle_id = fields.Many2one('fleet.vehicle', 'Vehicle')
    operation_id = fields.Many2one('transportation.operation', 'Operation')
    driver_id = fields.Many2one("hr.employee")
    address = fields.Char()
    date = fields.Date()
    circumstance_id = fields.Many2one('fleet.circumstance')
    description = fields.Char()


class TransportOperationGate(models.Model):
    _name = 'transport.operation.gate'
    _rec_name = "operation_id"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    vehicle_id = fields.Many2one('fleet.vehicle', 'Vehicle')
    trailer_id = fields.Many2one('fleet.vehicle', 'Trailer')
    operation_id = fields.Many2one('transportation.operation', 'Operation')
    driver_id = fields.Many2one("hr.employee")
    date = fields.Datetime()
    from_id = fields.Many2one("res.partner")
    to_id = fields.Many2one("res.partner")
    description = fields.Char()
    vehicle_type = fields.Selection([('Vehicle', 'Vehicle'), ('Trailer', 'Trailer')], 'Type')
    in_out = fields.Selection([('In', 'In'), ('Out', 'Out')], 'In/Out')


# class QualityCheckTest(models.Model):
#     _name = "quality.check.test"
#     _rec_name = 'product_id'
#
#     product_id = fields.Many2one("product.product")
#     quality_test_ids = fields.One2many("quality.test.lines", "quality_check_id")


# class QualityTestLines(models.Model):
#     _name = "quality.test.lines"
#
#     quality_check_id = fields.Many2one("quality.check.test")
#     quality_test_id = fields.Many2one("quality.check")
#     question_id = fields.Many2one("question.type")
#     question_type = fields.Selection(selection=[('quantitative', 'Quantitative'),
#                                                 ('qualitative', 'qualitative'), ])
#     quantitative_value = fields.Float()
#     qualitative_id = fields.Many2one(comodel_name="qualitative.value", string="qualitative value")
#     q_from = fields.Float()
#     q_to = fields.Float()
#     specification = fields.Char()
#     is_success = fields.Boolean(compute='get_success_value', default=False,store=True)
#
#     @api.onchange('question_id')
#     def get_question_data(self):
#         self.question_type = self.question_id.question_type
#         self.q_from = self.question_id.q_from
#         self.q_to = self.question_id.q_to
#         self.specification = self.question_id.specification
#
#     @api.depends('quantitative_value', 'qualitative_id')
#     def get_success_value(self):
#         for record in self:
#             if record.question_type == 'quantitative' and \
#                             record.quantitative_value >= record.q_from and \
#                             record.quantitative_value <= record.q_to:
#                 record.is_success = True
#             elif record.question_type == 'qualitative':
#                 if record.specification == record.qualitative_id.name:
#                     record.is_success = True
