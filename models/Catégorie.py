# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Catégorie(models.Model):

    _name = 'intervention.categorie'
    _description = 'Catégorie'

    code = fields.Char("Code")
    intitule = fields.Char("intitulé")


    def name_get(self):
        rec = []
        for record in self:
            rec.append((record.id,record.code))
        return rec