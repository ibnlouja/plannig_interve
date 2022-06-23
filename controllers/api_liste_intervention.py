# -*- coding: utf-8 -*-


from odoo import http
from odoo.http import request
import json
from odoo import api, SUPERUSER_ID


class ModuleApi(http.Controller):

    @http.route('/api/interventions', auth='public', methods=["GET"], csrf=False)
    def get_article(self, **kw):
        env = api.Environment(request.cr, SUPERUSER_ID, {})
        try:
            artice_stor = []
            product_ids = env['intervention.intervention'].sudo().search([])

            for product in product_ids:
                vals = {"num_intervention": product.num_intervention,
                        "id": product.client.id,
                        "name":product.client.name,
                        "collaborateur":product.collaborateur.nom}

                artice_stor.append(vals)
            return request.make_response(json.dumps(artice_stor),
                                         [('Content-Type', 'application/json'),
                                          ])

        except Exception as e:
            e = {'error': str(e)}
            return json.dumps(e)
