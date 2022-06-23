# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Article(models.Model):

    _name = 'intervention.article'
    _description = 'Article'

    code = fields.Char("Code article")
    intitule = fields.Char("Intitulé")

    categorie = fields.Char("Catégorie")
    unite_stock =fields.Char("Unité stock")
    marque = fields.Char("Marque")




    def name_get(self):
       	rec = []
        for record in self:
            rec.append((record.id,record.Code))
        return rec