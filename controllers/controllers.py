# -*- coding: utf-8 -*-
from odoo import http
import logging
from datetime import datetime

class WebServiceSageX3(http.Controller):

	@http.route('/interlocuteur', methods=['POST'], type='json', auth="public", website=True)
	def set_interlocuteur(self,access_token=None, **post):
		data = http.request.jsonrequest
		logging.info(data)
		logging.info("data--------code")
		logging.info(data["code"])
		obj_interlocuteur=http.request.env["intervention.interlocuteur"].sudo().search([("code","=",data["code"])])

		if obj_interlocuteur:

			logging.info("tessssssssssssssst")

			logging.info(obj_interlocuteur)



			obj_interlocuteur.sudo().write({
			"nom":data["nom"],
			"prenom":data["prenom"],
			"telephone":data["telephone"],
			"mobile":data["mobile"],})

			return "modification effectue avec success"
		else :

			http.request.env["intervention.interlocuteur"].sudo().create({
			"code":data["code"],
			"nom":data["nom"],
			"prenom":data["prenom"],
			"telephone":data["telephone"],
			"mobile":data["mobile"],
			})

			return "Création effectue avec success"



	@http.route('/api/site', methods=['POST'], type='json', auth="public", website=True)
	def set_site(self,access_token=None, **post):
		data = http.request.jsonrequest
		logging.info(data)
		logging.info("data--------code")
		logging.info(data["code"])
		obj_company=http.request.env["res.company"].sudo().search([("code","=",data["code"])])

		if not obj_company:


			http.request.env["res.company"].sudo().create({

			"code":data["code"],
			"name":data["nom"],

			})

			return "Création effectue avec success"


	@http.route('/intervention/encours', methods=['POST'], type='json', auth="public", website=True)
	def set_inntervention_encours(self,access_token=None, **post):
		data = http.request.jsonrequest
		logging.info(data)
		logging.info("data--------id")
		logging.info(data["Num"])
		obj_intervention=http.request.env["intervention.intervention"].sudo().search([("num_intervention","=",data["Num"])])

		if obj_intervention:

			obj_intervention.sudo().write({
				"encour":True,
				"planifier":False,
				
				})


			return "Modification effectue avec success"


	@http.route('/client', methods=['POST'], type='json', auth="public", website=True)
	def set_client(self,access_token=None, **post):
		data = http.request.jsonrequest
		logging.info(data)
		logging.info("data--------id")
		logging.info(data["id"])
		obj_client=http.request.env["res.partner"].sudo().search([("code","=",data["id"])])

		if not obj_client:


			http.request.env["res.partner"].sudo().create({

			"code":data["id"],
			"name":data["raison_social"],

			})
		else :

			obj_client.sudo().write({


				"name":data["raison_social"],
				
				})


			return "Création effectue avec success"


	@http.route('/collaborateur', methods=['POST'], type='json', auth="public", website=True)
	def set_collaborateur(self,access_token=None, **post):
		data = http.request.jsonrequest
		logging.info(data)
		logging.info("data--------codeCollabourateur")
		logging.info(data["code"])
		obj_collaborateur=http.request.env["intervention.collaborateur"].sudo().search([("code","=",data["code"])])

		if not obj_collaborateur:


			http.request.env["intervention.collaborateur"].sudo().create({

			"code":data["code"],
			"nom":data["nom"],
			

			})

			return "Création effectue avec success"


	@http.route('/parc', methods=['POST'], type='json', auth="public", website=True)
	def set_parc(self,access_token=None, **post):
		data = http.request.jsonrequest
		logging.info(data)
		logging.info("data--------idparc")
		logging.info(data["id"])
		obj_parc=http.request.env["intervention.parc"].sudo().search([("parc","=",data["id"])])

		if  obj_parc:

			obj_parc.sudo().write({


				"parc":data["id"],
				"designation":data["designation"],
				"site":data["address"],
				"designation_site":data["designation_address"],
				
				})
		else :


			http.request.env["intervention.parc"].sudo().create({

				"parc":data["id"],
				"designation":data["designation"],
				"site":data["address"],
				"designation_site":data["designation_address"],
				

			

			})

			return "Création effectue avec success"


	@http.route('/intervention', methods=['POST'], type='json', auth="public", website=True)
	def set_intervention(self,access_token=None, **post):
		data = http.request.jsonrequest
		logging.info(data)

		logging.info("dateeeeeeeeeeeeeeeeeeeeee")
		
		hd = int(data["heureD"]) - 100

		hf = int(data["HeureF"]) - 100
		logging.info("heuuuuuuuuuuuuur")


		date_debut = data["DateD"] +" "+ str(hd) + "00"
		data_fin   = data["DateF"] +" "+ str(hf) + "00"

		
		date_time_debut = datetime.strptime(date_debut,'%Y%m%d %H%M%S')
		date_time_fin = datetime.strptime(data_fin,'%Y%m%d %H%M%S')
		logging.info(date_time_debut)


		site = http.request.env["res.company"].sudo().search([("code","=",data["Site"])])

		logging.info(site)


		client = http.request.env["res.partner"].sudo().search([("code","=",data["Client"])]).id

		client_id = int(client)

		# interlocuteur = http.request.env["intervention.interlocuteur"].sudo().search([("code","=",data["Interlocuteur"])]).id


		type_intervention = http.request.env["intervention.type_intervention"].sudo().search([("intitule","=",data["type_int"])]).id




		logging.info(client_id)

		obj_intervention=http.request.env["intervention.intervention"].sudo().search([("num_intervention","=",data["Num"])])

		if obj_intervention:

			effectue = False

			if "effectue" in data :
				if data["effectue"] == '2':

					logging.info("iiiiiiiiiiiiiiiiiiiiiiiiiFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFECCCCCCCCCCCC")


					effectue= True
					hdR = int(data["heureDR"]) - 100

					hfR = int(data["HeureFR"]) - 100
					logging.info("heuuuuuuuuuuuuur")


					date_debutR = data["DateDR"] +" "+ str(hdR) + "00"
					data_finR   = data["DateFR"] +" "+ str(hfR) + "00"


					date_time_debutR = datetime.strptime(date_debutR,'%Y%m%d %H%M%S')
					date_time_finR = datetime.strptime(data_finR,'%Y%m%d %H%M%S')


					logging.info(date_time_debutR)
					logging.info(date_time_finR)


					write_int = obj_intervention.sudo().write({

					"date_debut":date_time_debutR,
					"date_fin":date_time_finR,
					"effectue":effectue,


					})
				else :

					logging.info("EFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFECCCCCCCCCCCC")

					write_int = obj_intervention.sudo().write({

						"date_debut":date_time_debut,
						"date_fin":date_time_fin,		
						})

				if write_int :

					if "Rapport" in data :
						if data["Rapport"] :
							for i in data["Rapport"] :


								rapport = http.request.env["intervention.rapport_intervention"].sudo().search([("intervention_id","=",obj_intervention.id),("nom","=",i['nom'])])


								logging.info("raaaaaapppppppppppppppporrrrrrrrttttttttttt")
								logging.info(rapport)

								if not rapport :

									http.request.env["intervention.rapport_intervention"].sudo().create({

										"nom" :i['nom'],
										"url" :i['url'],
										"intervention_id" :obj_intervention.id
										})

					if data["parcs"] :
						for i in data["parcs"] :

							parc = http.request.env["intervention.parc"].sudo().search([("parc","=",i['id_parc'])])

							parc_ligne = http.request.env["intervention.parc_ligne"].sudo().search([("parc","=",parc.id),("intervention_id","=",obj_intervention.id)])

							if not parc_ligne :

								if parc :

								

									http.request.env["intervention.parc_ligne"].sudo().create({

										"parc" :parc.id,
										"rapport_int" :i['rapport_int'],
										"satisfaction_client" :i['st_client'],
										"intervention_id" :obj_intervention.id

										})

					if "consommation" in data :

						if data["consommation"] :
							for i in data["consommation"] :

								consommation =http.request.env["intervention.consommations"].sudo().search([("chorno","=",i['id'])])

								if not consommation :

									http.request.env["intervention.consommations"].sudo().create({

										"parc":i['parc'],
										"consommation":i['consommation'],
										"type_consommation":i['type_consommation'],
										"quantite_duree":i['quantit'],
										"unite":i['unite'],
										"montant_consomme":i['montant_consomme'],
										"montant_facturer":i['montant_facture'],
										"devise":i['devise'],
										"chorno":i['id'],
										"intervention_id" :obj_intervention.id,

									})

			return "Modification effectue avec success"
		else :

			intervention = http.request.env["intervention.intervention"].sudo().create({

 			"num_intervention":data["Num"],
			"demande_service":data["DService"],
 			"client":client_id,
 			"company_id" :site.id,
 			"type_intervention":type_intervention,
 			"N_int":data["nateur_int"],
			"date_debut":date_time_debut,
			"date_fin":date_time_fin,
			"adresse":data["adresse"],
			"designation":data["designation"],
			"mail":data["Email"],
			"telephone":data["Telephone"],
			"titre":data["Titre"],
			# "interlocuteur":interlocuteur.id,
			"categorie":data["categorie"]
			})

			logging.info("Creationnnnnnnnnnnnnnnnnnnnnnnn intervention")

			logging.info(intervention)
			if intervention :
				if data["parcs"] :
					for i in data["parcs"] :

						parc = http.request.env["intervention.parc"].sudo().search([("parc","=",i['id_parc'])])

						if parc :

							http.request.env["intervention.parc_ligne"].sudo().create({

								"parc" :parc.id,
								"rapport_int" :i['rapport_int'],
								"satisfaction_client" :i['st_client'],
								"intervention_id" :intervention.id,

								})

			return "Création effectue avec success"








			


