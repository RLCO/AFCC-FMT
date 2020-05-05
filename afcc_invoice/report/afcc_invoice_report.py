# -*- coding: utf-8 -*-

from odoo import api, models
from dateutil.relativedelta import relativedelta
import datetime
import re


class AccountMove(models.AbstractModel):
    _inherit = 'account.move'

    def add_sale_data(self):
        print("KKKKKKKKKKKKKKKKKKKKKKKKK")

    # @api.model
    def get_sale_orders(self):
        # date_from = data['form']['date_from']
        # date_to = data['form']['date_to']
        # customer_id = data['form']['customer_id']
        total_sale = 0.0
        period_value = ''
        # u = (re.findall(r'\d+', customer_id))
        # print(">>>>>>>>>>", u)
        # t = []
        # for i in u:
        #     t.append(int(i))
        # print(customer_id.split(" "))
        # print("kkkkkkkk", t)
        # print("kkkkkkkk", t[0])
        # print(customer_id['id'])
        # if period_status == 'per_date':
        #     if date_from and date_to:
        # domain = [('date_order', '>=', date_from),
        #           ('date_order', '<=', date_to),
        #           ('partner_id', '=', t[0])]


        for record in self:
            str = record.invoice_origin
            print("record>>>>>>>>", record.invoice_origin)
            str_spilit = str.split(',')
            print("record>>>>>>>>", str_spilit)
            sale_orders = []
            for i in str_spilit:
                print(i.strip())
                orders = self.env['sale.order'].search([('name', '=', i.strip())])
                # for order in orders:
                    # sale_orders.append({
                    #     'name': order.name,
                    #     'date_order': order.date_order,
                    #     'partner' : order.partner_id.name,
                    #     'amount_total' : order.amount_total
                    # })
                    # total_sale += order.amount_total
                p1 = 0.0
                p2 = 0.0
                p3 = 0.0
                p4 = 0.0
                p5 = 0.0
                p6 = 0.0
                p7 = 0.0
                for line in orders.order_line:
                    if line.product_id.name == "Transportation Charge":
                        p1 = line.price_subtotal
                    elif line.product_id.name == "Delay Charge":
                        p2 = line.price_subtotal
                    elif line.product_id.name == "Extra Customer":
                        p3 = line.price_subtotal
                    elif line.product_id.name == "Return Shipment":
                        p4 = line.price_subtotal
                    elif line.product_id.name == "Transfer to other Location":
                        p5 = line.price_subtotal
                    elif line.product_id.name == "Labour Charge":
                        p6 = line.price_subtotal
                    elif line.product_id.name == "Other Charge":
                        p7 = line.price_subtotal

                sale_orders.append({
                    'vehicle_type': orders.vehicle_type_id.name,
                    'vehicle_no': orders.vehicle_no,
                    'policy_no': orders.policy_no,
                    'Waybill': orders.Waybill,
                    'from': orders.from_id.name,
                    'to': orders.to_id.name,
                    'from_date': orders.departure_time.strftime('%Y-%m-%d') if orders.departure_time else False,
                    'to_date': orders.arrival_time.strftime('%Y-%m-%d') if orders.arrival_time else False,
                    'p1': p1,
                    'p2': p2,
                    'p3': p3,
                    'p4': p4,
                    'p5': p5,
                    'p6': p6,
                    'p7': p7,
                    'total': orders.amount_untaxed,
                    'tax_id': orders.amount_tax,

                    # 'name': order.name,
                    # 'date_order': order.date_order,
                    # 'partner': order.partner_id.name,
                    # 'amount_total': order.amount_total,
                    #
                    # 'product': line.product_id.name,
                    # 'p1': p1,
                    # 'p2': p2,
                    # 'price_subtotal': line.price_subtotal,
                    # 'partner': line.partner_id.name,
                    # 'amount_total': line.amount_total
                })
            print(">>>>>>>>", sale_orders)
            x1 = False
            x2 = False
            x3 = False
            x4 = False
            x5 = False
            x6 = False
            x7 = False
            for x in sale_orders:
                if x['p1'] > 0.0:
                    x1 = True
                if x['p2'] > 0.0:
                    x2 = True
                if x['p3'] > 0.0:
                    x3 = True
                if x['p4'] > 0.0:
                    x4 = True
                if x['p5'] > 0.0:
                    x5 = True
                if x['p6'] > 0.0:
                    x6 = True
                if x['p7'] > 0.0:
                    x7 = True
                print("XXXXXXXXXX", x)
                # print("XXXXXXXXXX", x['p6'])
            print("x1", x1)
            print("x2", x2)
            print("x3", x3)
            print("x4", x4)
            print("x5", x5)
            print("x6", x6)
            print("x7", x7)
            # p_name = False
            # p_street = False
            # p_city = False
            # p_state_id = False
            # p_country_id = False
            # partner_id = self.env['res.partner'].search([('id', '=', t[0])])
            # if partner_id:
            #     p_name = partner_id.name
            #     p_street = partner_id.street
            #     p_city = partner_id.city
            #     p_state_id = partner_id.state_id.id
            #     p_country_id = partner_id.country_id.id
            return {
                # 'doc_ids': data['ids'],
                # 'doc_model': data['model'],
                # 'period' : period_value,
                # 'date_from': date_from,
                # 'date_to': date_to,
                # 'customer_id': p_name,
                # 'street': p_street,
                # 'city': p_city,
                # 'state_id': p_state_id,
                # 'country_id': p_country_id,
                'sale_orders': sale_orders,
                'x1': x1,
                'x2': x2,
                'x3': x3,
                'x4': x4,
                'x5': x5,
                'x6': x6,
                'x7': x7,
                # 'total_sale' : total_sale,
            }


        # sale_orders = []
        # orders = self.env['sale.order'].search(domain)
        #
        # print("orders", orders)
        # for order in orders:
        #     # sale_orders.append({
        #     #     'name': order.name,
        #     #     'date_order': order.date_order,
        #     #     'partner' : order.partner_id.name,
        #     #     'amount_total' : order.amount_total
        #     # })
        #     # total_sale += order.amount_total
        #     p1 = 0.0
        #     p2 = 0.0
        #     p3 = 0.0
        #     p4 = 0.0
        #     p5 = 0.0
        #     p6 = 0.0
        #     p7 = 0.0
        #     for line in order.order_line:
        #         if line.product_id.name == "Transportation Charge":
        #             p1 = line.price_subtotal
        #         elif line.product_id.name == "Delay Charge":
        #             p2 = line.price_subtotal
        #         elif line.product_id.name == "Extra Customer":
        #             p3 = line.price_subtotal
        #         elif line.product_id.name == "Return Shipment":
        #             p4 = line.price_subtotal
        #         elif line.product_id.name == "Transfer to other Location":
        #             p5 = line.price_subtotal
        #         elif line.product_id.name == "Labour Charge":
        #             p6 = line.price_subtotal
        #         elif line.product_id.name == "Other Charge":
        #             p7 = line.price_subtotal
        #
        #     sale_orders.append({
        #         'vehicle_type': order.vehicle_type_id.name,
        #         'vehicle_no': order.vehicle_no,
        #         'from_date': order.departure_time,
        #         'to_date': order.arrival_time,
        #         'p1': p1,
        #         'p2': p2,
        #         'p3': p3,
        #         'p4': p4,
        #         'p5': p5,
        #         'p6': p6,
        #         'p7': p7,
        #         'total': order.amount_untaxed,
        #         'tax_id': order.amount_tax,
        #
        #         # 'name': order.name,
        #         # 'date_order': order.date_order,
        #         # 'partner': order.partner_id.name,
        #         # 'amount_total': order.amount_total,
        #         #
        #         # 'product': line.product_id.name,
        #         # 'p1': p1,
        #         # 'p2': p2,
        #         # 'price_subtotal': line.price_subtotal,
        #         # 'partner': line.partner_id.name,
        #         # 'amount_total': line.amount_total
        #     })
        # print(">>>>>>>>", sale_orders)
        # x1 = False
        # x2 = False
        # x3 = False
        # x4 = False
        # x5 = False
        # x6 = False
        # x7 = False
        # for x in sale_orders:
        #     if x['p1'] > 0.0:
        #         x1 = True
        #     if x['p2'] > 0.0:
        #         x2 = True
        #     if x['p3'] > 0.0:
        #         x3 = True
        #     if x['p4'] > 0.0:
        #         x4 = True
        #     if x['p5'] > 0.0:
        #         x5 = True
        #     if x['p6'] > 0.0:
        #         x6 = True
        #     if x['p7'] > 0.0:
        #         x7 = True
        #     print("XXXXXXXXXX", x)
        #     # print("XXXXXXXXXX", x['p6'])
        # print("x1", x1)
        # print("x2", x2)
        # print("x3", x3)
        # print("x4", x4)
        # print("x5", x5)
        # print("x6", x6)
        # print("x7", x7)
        # p_name = False
        # p_street = False
        # p_city = False
        # p_state_id = False
        # p_country_id = False
        # partner_id = self.env['res.partner'].search([('id', '=', t[0])])
        # if partner_id:
        #     p_name = partner_id.name
        #     p_street = partner_id.street
        #     p_city = partner_id.city
        #     p_state_id = partner_id.state_id.id
        #     p_country_id = partner_id.country_id.id
        # return {
        #     'doc_ids': data['ids'],
        #     'doc_model': data['model'],
        #     # 'period' : period_value,
        #     'date_from': date_from,
        #     'date_to': date_to,
        #     'customer_id': p_name,
        #     'street': p_street,
        #     'city': p_city,
        #     'state_id': p_state_id,
        #     'country_id': p_country_id,
        #     'sale_orders' : sale_orders,
        #     'x1': x1,
        #     'x2': x2,
        #     'x3': x3,
        #     'x4': x4,
        #     'x5': x5,
        #     'x6': x6,
        #     'x7': x7,
        #     # 'total_sale' : total_sale,
        # }
