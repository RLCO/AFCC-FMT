##############################################################################
#
#    Odoo module for Transport Sale
#    Copyright (C) 2004-2010 Alien Group (<http://www.alien-group.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from odoo import models, fields, api,_
from odoo.tools.translate import _
from odoo.exceptions import UserError

class sale_order_fleet_vehicle(models.Model):
    _name = 'sale.order.fleet_vehicle'
    _description = 'All sales order and associated vehicles'
    sale_order_id=fields.Many2one('sale.order', string='Sale Order', ondelete='cascade')
    sales_date= fields.Date(string='Sales Date')
    partner_departure_id= fields. Many2one( 'res.partner', string='From')
    partner_destination_id= fields. Many2one( 'res.partner', string='To')
    delivery_date= fields.Date(string='Delivery Date', help='The date that will start to transport')
    return_date= fields.Date(string='Return Date', help='The expected date to finish all the transport')
    fleet_vehicle_id= fields. Many2one( 'fleet.vehicle', string='Vehicle', required=True,ondelete='restrict')
    license_plate= fields.Char('License Plate', size=64, required=False, store=True)
    internal_number= fields.Integer('Number')
    employee_driver_id= fields. Many2one( 'hr.employee', string='Driver', required=True,
                                       ondelete='restrict')
    employee_helper_id= fields. Many2one( 'hr.employee', string='helper', required=False,
                                       ondelete='restrict')
    fleet_trailer_id= fields. Many2one( 'fleet.vehicle', string='Trailer',
                                       ondelete='restrict', required=True)
    trailer_license_plate= fields.Char(string='Trailer License Plate', size=64, required=False, store=True)
    cargo_ids= fields.One2many('sale.order.cargo', 'sale_order_fleet_id',string='Cargo', required=True,help='All sale order transported cargo')


    def fleet_trailer_id_change(self,fleet_trailer_id):
        result={}

        if not fleet_trailer_id:
            return result

        trailer = self. env['fleet.vehicle'].browse(fleet_trailer_id)

        if trailer:
            result['trailer_license_plate'] = trailer.license_plate

        return result

    def fleet_vehicle_id_change(self ,fleet_vehicle_id,context):
        result={}

        if not fleet_vehicle_id:
            return result

        vehicle = self. env['fleet.vehicle'].browse(fleet_vehicle_id)
        sale_order = self. env['sale.order'].browse(self._context.get('sale_order_id'))

        if vehicle:
            result['license_plate'] =  vehicle.license_plate
            result['employee_driver_id'] = vehicle.emp_driver_id.id
            result['internal_number']=vehicle.internal_number


        if sale_order:
            #print "sale_date=" + sale_order.Date_order
            result['sales_date'] =  sale_order.Date_order
            #print "sale departure id=" + sale_order.partner_departure_id.id
            result['partner_departure_id'] =  sale_order.partner_departure_id.id
            #print "sale shipping id=" + sale_order.partner_shipping_id.id
            result['partner_destination_id'] =  sale_order.partner_shipping_id.id
            #print "deli date=" + sale_order.delivery_date
            result['delivery_date'] =  sale_order.delivery_date
            #print "deli date=" + sale_order.return_dae
            result['return_date'] =  sale_order.return_date

        return result

    def copy(self,default=None, context=None):

        if not default:
            default = {}

        return super(sale_order_fleet_vehicle, self).copy(default, context=context)



sale_order_fleet_vehicle()

class sale_order_cargo(models.Model):
    _name = 'sale.order.cargo'
    _description = 'Transport cargo from a sale order transport service'
     
    sale_order_fleet_id= fields.Many2one('sale.order.fleet_vehicle', string='Sale Order Vehicle',ondelete='cascade', required=True,readonly=True)
    transport_date= fields.Date(string='Transport Date', required=True,help='The day when the product was transported')
    cargo_product_id= fields. Many2one( 'product.product', string='Cargo', required=True)
    cargo_docport= fields.Char(string='Port Document', size=64, required=False, readonly=False,
                                help='Associated port document of the transported product if applicable.')
    brand= fields.Char('Brand', size=64, required=False, readonly=False,
                        help='Brand of the transported product if applicable.')
    model= fields.Char('Model', size=64, required=False, readonly=False,help='Model of the transported product if applicable.')
    cargo_ident= fields.Char('Identification', size=64, required=False, readonly=False,
                              help='Identification of the cargo.Ex:Id,License Plate,Chassi')
    sale_order_id= fields.Many2one( 'sale.order', string='Sale Order', required=True)
    transport_from_id= fields. Many2one( 'res.partner', string='From')
    transport_to_id= fields. Many2one('res.partner', string='To')
                    

    def cargo_id_change(self,cargo_product_id,context):

        result={}
        if not cargo_product_id:
            return result

        sale_order = self. env['sale.order'].browse(self._context.get('sale_order_id'))

        if sale_order:
            result['sale_order_id'] = self._context.get('sale_order_id')

#             if [ product sale_order_fleet_idfor product in sale_order.order_line if cargo_product_id == product.product_id]:

        return  result

    def copy(self, default=None, context=None):

        if not default:
            default = {}
#         default.update({
#         })

        res_id = super(sale_order_cargo, self).copy(default, context)
        return res_id

class sale_order(models.Model):
    _inherit = 'sale.order'
    #Do not touch _name it must be same as _inherit
    #_name = 'sale.order'
     
    fleet_vehicles_ids= fields.One2many( 'sale.order.fleet_vehicle', 'sale_order_id',string='Transport Vehicles', required=True)
    partner_departure_id= fields. Many2one('res.partner', string='From', required=True)
    delivery_date= fields.Date('Transport Start',required=True,help='Expected Transport start date.')
    return_date= fields.Date('Transport Finish',required=True,help='Expected Transport finish date.')
    cargo_ids= fields.One2many( 'sale.order.cargo', 'sale_order_id',string='Cargo Manifest', required=False,help='All transported cargo manifest.')
               

    def _validate_data(self):
        for dates in self.browse(self):
            if dates.return_date < dates.delivery_date:
                return False
            else:
                return True
    #TODO : check condition and return Boolean accordingly

    def _validate_cargo_products(self):

        result = True
        cargo_products_ids = []

        sale_order = self.browse([0])

        if sale_order:
            cargo_products_ids = [cargo.cargo_product_id.id for cargo in sale_order.cargo_ids]

            if not cargo_products_ids:
                result = True
            else:
                line_products_ids = [line.product_id.id for line in sale_order.order_line]
                result = set(cargo_products_ids) == set(line_products_ids)

        return result

    def _validate_cargo_products_qty(self):

        result = True
        msg_format=""
        line_product_ids = []
        line_product_qts = []

        sale_order = self.browse([0])

        if sale_order:
            cargo_product_ids = [cargo.cargo_product_id.id for cargo in sale_order.cargo_ids]

            #give all products for order line
            line_product_ids = [line.product_id.id for line in sale_order.order_line]
            line_product_qts = [line.product_uom_qty for line in sale_order.order_line]

            line_product_ids_qts = {}
            line_product_dif_ids = {}

            for idx,prod_id in enumerate(line_product_ids):
                if prod_id in line_product_ids_qts.keys():
                    line_product_ids_qts[prod_id]+= line_product_qts[idx]
                else:
                    line_product_ids_qts[prod_id] = line_product_qts[idx]

            if not cargo_product_ids:
                result = True
            else:
                for cargo_product_id in set(cargo_product_ids):
                    line_product_ids_dict = { prod_id:qtd  for prod_id,qtd in line_product_ids_qts.iteritems()
                                         if prod_id == cargo_product_id
                                         and int(line_product_ids_qts[prod_id]) != cargo_product_ids.count(cargo_product_id)}

                    line_product_dif_ids.update(line_product_ids_dict)

                if len(line_product_dif_ids) > 0:

                    line_product_names = self. env['product.product'].name_get(line_product_dif_ids.keys(),context=None)
                    cargo_product_qts = [ cargo_product_ids.count(cargo_product_id) for cargo_product_id in line_product_dif_ids.keys()]
                    for product_name in line_product_names:
                        index= line_product_names.index(product_name)

                        msg_format =  _("""Product:%s\n\tOrder=%s vs Cargo=%s\n""") % (product_name[1],
                                                                                       int(line_product_dif_ids[product_name[0]]),
                                                                                       cargo_product_qts[index])

                    message = _("""The following products quantities in cargo don't match\n quantities in sales order line:\n%s
                                    """) % (msg_format)

                    raise UserError(_('Error'), message)
                    result = False
                else:
                    result = True
        return result

    _constraints = [(_validate_data,'Error: Invalid return date', ['delivery_date','return_date']),
                    (_validate_cargo_products,"Error: There is a cargo product that doesn't belongs to the sale order line!",['cargo_ids','order_line']),
                    (_validate_cargo_products_qty,"Error: In products quantities",['cargo_ids','order_line'])]

sale_order()

class fleet_vehicle(models.Model):
    _inherit = 'fleet.vehicle'
    #Do not touch _name it must be same as _inherit
    #_name = 'fleet.vehicle'

    sales_order_ids= fields.One2many( 'sale.order.fleet_vehicle', 'fleet_vehicle_id', string='Vehicle Sales')
    internal_number= fields.Integer(string='Internal Number')
    is_trailer= fields.Boolean(string='Is Trailer',required=False)
                
fleet_vehicle()


class hr_employee_driver_sales(models.Model):
    _inherit = 'hr.employee'
    #Do not touch _name it must be same as _inherit
    #_name = 'hr.employee'

 
    sales_order_ids= fields.One2many( 'sale.order.fleet_vehicle','employee_driver_id', string='Driver Sales')
    is_driver= fields.Boolean('Is Driver', required=False)
                   

hr_employee_driver_sales()
