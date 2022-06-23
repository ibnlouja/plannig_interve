# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Ressources(models.Model):

    _name = 'intervention.ressources'
    _description = 'Ressources'

    reservation = fields.Char("reservation")
    ressource = fields.Char("Ressource")
    date_debut = fields.Datetime("Date début")
    date_fin = fields.Datetime("Date fin")
    intervention_id = fields.Many2one("intervention.intervention","Intervention")


    

    def name_get(self):
        rec = []
        for record in self:
            rec.append((record.id,record.ressource))
        return rec
