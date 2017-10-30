# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, tools


class DarfboardReport(models.Model):
    """ Darfboard analysis """

    _name = "darfboard.entry.report"
    _description = "Darfboard entry report"
    _rec_name = 'id'
    _auto = False
    
    
    parameter = fields.Char(string="Parameter")
    journal = fields.Char(string="Journal")
    entry_date = fields.Date(string="Entry Date")
    entry_number = fields.Char(string="Entry code")
    entry_item_number = fields.Char(string="Entry item number")
    entry_item_debit_code = fields.Char(string="Account Char code")
    entry_item_debit_name = fields.Char(string="Account Char name")
    entry_item_debit_value = fields.Float(string="Debit")
    entry_item_quantity = fields.Float(string="Debit quantity")
    entry_item_credit_value = fields.Float(string="Credit")
   

    def init(self):
        tools.drop_view_if_exists(self._cr, 'darfboard_entry_report')
        self._cr.execute("""
            CREATE VIEW darfboard_entry_report AS (
                select
                    d.id,
                    d.parameter,
                    d.journal,
                    d.entry_number,
                    d.entry_item_number,
                    d.entry_date,
                    d.entry_item_debit_code,
                    d.entry_item_debit_name,
                    d.entry_item_debit_value,
                    d.entry_item_credit_value,
                    d.entry_item_quantity
                from
                    data_for_analysis d
            )""")
