# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Interlocuteur(models.Model):

    _name = 'intervention.interlocuteur'
    _description = 'Interlocuteur'

    code = fields.Char("Code")
    nom = fields.Char("Nom")
    prenom = fields.Char("Prénom")
    telephone = fields.Char("Téléphone")
    mobile =fields.Char("Mobile")
    email = fields.Char("Email")

    client = fields.Many2one("res.partner","Client")









    def name_get(self):
        rec = []
        for record in self:
            rec.append((record.id,record.code))
        return rec


