# -*- coding: utf-8 -*-

from odoo import models, fields, api
from json import loads ,dumps
import requests
import logging


class Collaborateur(models.Model):

    _name = 'intervention.collaborateur'
    _description = 'Collaborateur'

    code = fields.Char("Code")
    nom = fields.Char("Nom & Prénom")
    prenom = fields.Char("Prénom")


    def name_get(self):
        rec = []
        name = ""
        for record in self:
            rec.append((record.id,record.nom))
        return rec




