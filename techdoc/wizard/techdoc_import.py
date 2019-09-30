# -*- coding: utf-8 -*-
# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full copyright and licensing details.

import logging

from lxml import etree

from odoo import api, fields, models, tools

_logger = logging.getLogger(__name__)

ATTRS = [
    'groups', 'required', 'readonly', 'invisible', 'on_change', 'attrs',
    'domain', 'options', 'context', 'widget'
]


class TechDocImport(models.TransientModel):
    _name = "techdoc.import"
    _description = "TechDoc Import"

    model_id = fields.Many2one('ir.model')
    # view_ids = fields.Many2many('ir.ui.view')
    overwrite = fields.Boolean()

    @api.multi
    def techdoc_import(self):
        obj = self[0]
        obj = obj.with_context(overwrite=obj.overwrite)

        View = self.env['ir.ui.view']

        # TODO domain mode (form, tree)
        # Assume active is True
        domain = [
            ('model', '=', obj.model_id.model),
            ('mode', '=', 'primary'),
            ('type', '=', 'form')]
        view = View.search(domain, limit=1)
        self._parse_import_view(view)

    def _parse_import_view(self, view):
        ModelField = self.env['ir.model.fields']
        FormField = self.env['techdoc.view.form.field']
        obj = self[0]

        # Delete first
        FormField.search([('model_id', '=', obj.model_id.id)]).unlink()

        # Start XML parsing
        combined = view.read_combined()
        root = self._parse_view_xml(combined['arch'])
        
        fields_el = root.xpath('//field')
        fields_el_dict = {field.get('name'): {'field': field, 'sequence': idx} for idx, field in enumerate(fields_el)}

        domain = [
            ('model_id', '=', obj.model_id.id),
            ('name', 'in', fields_el_dict.keys())]
        fields = ModelField.search(domain)

        for f in fields:
            field_el = fields_el_dict[f.name]['field']
            sequence = fields_el_dict[f.name]['sequence'] + 1
            vals = {
                'model_id': obj.model_id.id,
                'field_id': f.id,
                'field_type': f.ttype, # related fields.Selection is unhandy; requires all options
                'sequence': sequence
            }
            form_groups_val = []
            form_groups_iter = field_el.iterancestors(tag='group')
            for form_group_el in form_groups_iter:
                if form_group_el.attrib:
                    attrib_fmt = ' '.join(['%s="%s"' % (k, v) for (k, v) in form_group_el.attrib.items()])
                else:
                    attrib_fmt = ''

                form_group_repr = '<{tag} {attrib}/>'.format(
                    tag=form_group_el.tag,
                    attrib=attrib_fmt)
                form_groups_val.insert(0, form_group_repr)

            if form_groups_val:
                vals['form_groups'] = ''.join(form_groups_val)
                                 
            for attr in ATTRS:
                field_attr = field_el.get(attr)
                if field_attr:
                    # TODO prefix field names (model and view too)?
                    # key = 'field_%s' % attr
                    vals[attr] = str(field_attr)
            FormField.create(vals)

    def _parse_view_xml(self, xml):
        if not xml:
            return False
        parser = etree.XMLParser(
            ns_clean=True,
            recover=True,
            encoding='utf-8',
            remove_blank_text=True)
        root = etree.XML(xml, parser=parser)
        return root

