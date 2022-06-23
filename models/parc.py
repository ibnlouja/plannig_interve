# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Parc(models.Model):

    _name = 'intervention.parc'
    _description = 'Parc'

    parc = fields.Char("Numéro Parc")
    designation = fields.Char("Désignation")
    
    site = fields.Char("Site d'installation")
    designation_site =fields.Char("Designation site")
    article =fields.Char("Article")

    marque =fields.Char("Marque")

    num_serie =fields.Char("Numéro de série")

    client = fields.Many2one("res.partner","Client")

    
    intervention_id = fields.Many2one("intervention.intervention","Intervention")

    parc_ligne_ids = fields.One2many("intervention.parc_ligne","parc")


    def name_get(self):
       	rec = []
        for record in self:
            rec.append((record.id,record.parc))
        return rec



class Parc_ligne(models.Model):

	_name = 'intervention.parc_ligne'
	_description = 'Parc'
	parc = fields.Many2one("intervention.parc","Parc")
	rapport_int = fields.Char("Rapport intervention")
	satisfaction_client = fields.Char("Satisfaction client")

	designation = fields.Char(related="parc.designation",store=True)

	site = fields.Char(related="parc.site",store=True)

	designation_site =fields.Char(related="parc.designation_site",store=True)

	intervention_id = fields.Many2one("intervention.intervention","Intervention")

	date_debut = fields.Datetime(related="intervention_id.date_debut",store=True)

	date_fin = fields.Datetime(related="intervention_id.date_fin",store=True)

	type_intervention =fields.Many2one(related="intervention_id.type_intervention",store=True)

	def name_get(self):

		rec = []

		for record in self:

			rec.append((record.id,record.parc))

		return rec