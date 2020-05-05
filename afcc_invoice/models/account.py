# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    def get_line_with_vat(self):
        total_with_vat = 0
        total_without_vat = 0
        for rec in self:
            for line in rec.invoice_line_ids:
                if line.tax_ids:
                    total_with_vat += line.price_subtotal
                else:
                    total_without_vat += line.price_subtotal
        vals= {'total_with_vat': total_with_vat ,'total_without_vat': total_without_vat,}
        return vals

    def get_sale_order_data(self):
        for record in self:
            if record.invoice_origin:
                vals = {}
                str = record.invoice_origin
                print("record>>>>>>>>", record.invoice_origin)
                str_spilit = str.split(',')
                print("record>>>>>>>>", str_spilit)
                # sale_orders = []
                # for i in str_spilit:
                #     print(i.strip())
                orders = self.env['sale.order'].search([('name', 'in', str_spilit)])
                if orders:
                    vals = {
                        'from': orders.from_id.name if orders.from_id else False,
                        'to': orders.to_id.name if orders.to_id else False,
                        'departure': orders.departure_time.strftime('%Y-%m-%d') if orders.departure_time else False,
                        'arrival': orders.arrival_time.strftime('%Y-%m-%d') if orders.arrival_time else False,
                        'vehicle': orders.vehicle_id.name if orders.to_id else False,
                        'vehicle_type': orders.vehicle_type_id.name if orders.to_id else False,
                        'vehicle_no': orders.vehicle_no,
                        'helper': orders.helper_id.name if orders.to_id else False,
                        'driver': orders.driver_id.name if orders.to_id else False,
                        'policy_no': orders.policy_no,
                        'waybill': orders.Waybill,
                    }
                    print("orders: ", orders)
                    print("id: ", orders.id)
                print("vals:", vals)
                print("vvvv:", vals['from'])
                return vals