# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Consommations(models.Model):

    _name = 'intervention.consommations'
    _description = 'Consommations'

    parc = fields.Char("Parc")
    consommation = fields.Char("Consommations")
    type_consommation = fields.Char("Type de consommation")

    version_majeure = fields.Char("Version_majeure")
    site_stockage = fields.Char("Site de stockage")
    quantite_duree = fields.Integer("Quantité/Durée")
    unite = fields.Char("Unité")

    effectue = fields.Datetime("Effectué le")
    duree_reel_h = fields.Integer("Durée réelle (Heures)")
    duree_reel_m = fields.Integer("Durée réelle (Minutes)")
    montant_consomme = fields.Float("Montant Consommé")
    montant_facturer = fields.Float("Montant à facturer")


    devise = fields.Char("Devise")
    point_debites=fields.Integer("Points débités")

    text = fields.Text("Text")

    chorno = fields.Char("Chrono")

    intervention_id = fields.Many2one("intervention.intervention","Intervention")


    def name_get(self):
        rec = []
        for record in self:
            rec.append((record.id,record.consommation))
        return rec

