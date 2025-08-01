from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    picking_ids = fields.Many2many(
        comodel_name='stock.picking',
        compute='_compute_picking_ids',
        store=False,
        string='Pickings',
    )

    @api.depends('name')
    def _compute_picking_ids(self):
        for order in self:
            order.picking_ids = self.env['stock.picking'].search([('origin', '=', order.name)])


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_secondary_uom = fields.Boolean(
        related='product_id.product_tmpl_id.is_secondary_uom',
        readonly=True
    )
    secondary_uom_id = fields.Many2one(
        'uom.uom',
        related='product_id.product_tmpl_id.secondary_uom_id',
        readonly=True
    )
    secondary_qty = fields.Float(
        string='Secondary Qty',
        compute='_compute_secondary_qty',
        readonly=True
    )

    @api.depends('product_uom_qty', 'secondary_uom_id')
    def _compute_secondary_qty(self):
        for line in self:
            if line.secondary_uom_id and line.secondary_uom_id.factor_inv:
                line.secondary_qty = line.product_uom_qty / line.secondary_uom_id.factor_inv
            else:
                line.secondary_qty = 0.0


# from odoo import models, fields, api
#
# class SaleOrderLine(models.Model):
#     _inherit = 'sale.order.line'
#     picking_ids = fields.One2many('stock.picking', 'origin', string="Pickings", readonly=True)
#
#     is_secondary_uom = fields.Boolean(
#         related='product_id.product_tmpl_id.is_secondary_uom',
#         readonly=True
#     )
#     secondary_uom_id = fields.Many2one(
#         'uom.uom',
#         related='product_id.product_tmpl_id.secondary_uom_id',
#         readonly=True
#     )
#     secondary_qty = fields.Float(
#         string='Secondary Qty',
#         compute='_compute_secondary_qty',
#         readonly=True
#     )
#
#     @api.depends('product_uom_qty', 'secondary_uom_id')
#     def _compute_secondary_qty(self):
#         for line in self:
#             if line.secondary_uom_id and line.product_uom_qty:
#                 line.secondary_qty = line.product_uom_qty / line.secondary_uom_id.factor_inv
#             else:
#                 line.secondary_qty = 0.0
