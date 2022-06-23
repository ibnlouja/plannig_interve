# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Site(models.Model):

    _name = 'intervention.site'
    _description = 'Site'

    code = fields.Char("Code")
    nom = fields.Char("Nom de site")


    def name_get(self):
        rec = []
        for record in self:
            rec.append((record.id,record.code))
        return rec

class InheritCompany(models.Model):

   	_inherit = 'res.company'

   	code = fields.Char("Code")



class InheritPartner(models.Model):

   	_inherit = 'res.partner'

   	code = fields.Char("Code")