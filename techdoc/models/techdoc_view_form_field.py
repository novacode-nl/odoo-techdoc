# -*- coding: utf-8 -*-
# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ViewFormField(models.Model):
    _name = 'techdoc.view.form.field'
    _order = 'sequence ASC'

    model_id = fields.Many2one('ir.model')
    model_name = fields.Char(related='model_id.model')
    field_id = fields.Many2one('ir.model.fields')
    field_description = fields.Char(related='field_id.field_description', string='Field')
    field_name = fields.Char(related='field_id.name', string='Field Name')
    field_type = fields.Char(string='Field Type')
    sequence = fields.Integer()

    form_groups = fields.Char(string='Form <group, .../>')

    view_id = fields.Many2one('ir.ui.view')
    view_name = fields.Char(related='view_id.name')
    view_xml_id = fields.Char(related='view_id.xml_id')
    view_type = fields.Char(compute='_compute_view_fields')
    
    widget = fields.Char(string='widet=')
    options = fields.Char(string='options=')
    groups = fields.Char(string='groups=') # res_group_ids (many2many) ?
    on_change = fields.Char(string='on_change=')


    attrs = fields.Char(string='attrs=')
    # attrs_invisible = fields.Char()
    # attrs_readonly = fields.Char()
    # attrs_required = fields.Char()

    domain = fields.Char(string='domain=')
    context = fields.Char(string='context=')
    readonly = fields.Char(string='readonly=')
    required = fields.Char(string='required=')
    invisible = fields.Char(string='invisible=')

    @api.depends('view_id')
    def _compute_view_fields(self):
        for r in self:
            r.view_type = r.view_id.type
