# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Defaut(models.Model):

    _name = 'intervention.defaut'
    _description = 'Defaut'

    code = fields.Char("Code Defaut")
    intitule = fields.Char("Intitulé")
    intervention_id = fields.Many2one("intervention.intervention","Intervention")


    def name_get(self):
       	rec = []
        for record in self:

            rec.append((record.id,record.Code))

        return rec