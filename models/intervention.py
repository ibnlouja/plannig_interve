# -*- coding: utf-8 -*-

from odoo import models, fields, api,_

from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning

import logging
from datetime import datetime
from json import loads ,dumps
import requests





class intervention(models.Model):

    _name = 'intervention.intervention'
    _description = 'Intervention'


    num_intervention = fields.Char("Numéro Intervention",required=True)
    color = fields.Char("Color",default="#661CA6",compute="get_state" ,store=True)


    site = fields.Many2one("intervention.site","Site")
    nom_site = fields.Char(related="site.nom", string="Nom site")

    company_id = fields.Many2one("res.company","Site")
    company_name = fields.Char(related="company_id.name", string="Nom site")

    chrono = fields.Char("Chrono")
    demande_service = fields.Char("Demande de service",)
    client = fields.Many2one("res.partner","Client",required=True)
    interlocuteur = fields.Many2one("intervention.interlocuteur","Interlocuteur")
    nom_interlocuteur = fields.Char(string="Nom interlocuteur",compute="get_interlocuteur" ,store=True)
    effectue = fields.Boolean("Effectué")
    collaborateur = fields.Many2one("intervention.collaborateur","Collaborateur")
    nom_collaborateur = fields.Char(string="Nom collaborateur",compute="get_collaborateur" ,store=True)

    collaborateur2 = fields.Many2one("intervention.collaborateur","Collaborateur 2")
    nom_collaborateur2 = fields.Char(string="Nom collaborateur 2",compute="get_collaborateur" ,store=True)

    date_debut = fields.Datetime("Date début Réel",required=True)
    date_fin = fields.Datetime("Date fin Réel",required=True)


    date_invisible= fields.Date("Date",compute="get_data",store=True)

    date_invisible_fin= fields.Date("Date fin",compute="get_data",store=True)



    date_debut_planifier = fields.Datetime("Date début planifier",compute="get_data",store=True)
    date_fin_planifier = fields.Datetime("Date fin planifier",compute="get_data",store=True)

    semaine =fields.Integer("Semaine")
    categorie = fields.Char("Catégorie",readonly=True)
    pays = fields.Many2one("res.country")

    adresse = fields.Char("Adresse",readonly=True)
    designation =fields.Char("designation",readonly=True)
    code_postal = fields.Integer("Code postal",readonly=True)
    ville = fields.Char("Ville",readonly=True)
    telephone = fields.Char("Téléphone",readonly=True)
    portable = fields.Char("Portable")
    mail = fields.Char("Adresse e-mail",readonly=True)
    distance = fields.Char("Distance")
    duree = fields.Char("Durée",readonly=True)
    duree_adresse = fields.Char("Durée estimée",readonly=True)
    titre = fields.Char("Titre")

    complement_information = fields.Text("Description")

    consommation_ids = fields.One2many("intervention.consommations","intervention_id","Consommation")
    ressource_ids = fields.One2many("intervention.ressources","intervention_id","ressource")

    prestation_planif_h = fields.Integer("Heures")
    prestation_planif_m = fields.Integer("Minutes")

    prestation_effectuées_h = fields.Integer("Heures")
    prestation_effectuées_m = fields.Integer("Minutes")

    reste_faire_h = fields.Integer("Heures")
    reste_faire_m = fields.Integer("Minutes")

    reel_effectue_h = fields.Integer("Heures")
    reel_effectue_m = fields.Integer("Minutes")

    compte_rendu = fields.Text("Compte-rendu")
    temps_realise=fields.Integer("Somme temps realisé")

    fixe = fields.Boolean("Fixe")
    duplic_inter = fields.Boolean("Duplicate")

    T_int = fields.Char("Type de l'intervention",readonly=True)


    N_int = fields.Char("Nature de l'intervention",readonly=True)


    type_intervention =fields.Many2one("intervention.type_intervention","Type de l'intervention")


    color_type = fields.Char(related="type_intervention.color", string="color type")

    nature_intervention =fields.Many2one("intervention.nature_intervention","Nature de l'intervention")

    parc_ids = fields.One2many("intervention.parc_ligne","intervention_id","Parc")

    rapport_ids = fields.One2many("intervention.rapport_intervention","intervention_id","Rapport")
    defaut_ids = fields.One2many("intervention.defaut","intervention_id","Defaut")





    planifier = fields.Boolean("planifier")
    encour = fields.Boolean("en cours")
    demande_devis =fields.Boolean("Demande devis")
    style = fields.Char("style")


    def _default_stage_id(self):
        ids = self.env['intervention.state_intervention'].search([]).ids
        if ids:
            return ids[0]
        return False



    state_id = fields.Many2one('intervention.state_intervention', 'Statut', ondelete='restrict',
                               copy=False, index=True,compute="get_state")

    code_state =fields.Char(related="state_id.code", string="code state")


    def staut_encour (self):

        state = self.env["intervention.state_intervention"].sudo().search([("code","=","EC")])

        self.sudo().write({"state_id" : state.id})
        # self.state_id = 3


    def staut_demande_devi (self):
        
        state = self.env["intervention.state_intervention"].sudo().search([("code","=","DV")])

        self.sudo().write({"state_id" : state.id})






    # @api.constrains('collaborateur','collaborateur2')
    # def set_sage_x3(self):

    #     webservice_url = "http://192.168.10.20:4000/api/interventions/updateinterventiondateodoo"
    #     headers = {'Content-type': 'application/json'}

    #     for record in self:
    #         if record.collaborateur :
    #             date_debut = (datetime.strftime(record.date_debut,"%Y%m%d"))
    #             date_fin = (datetime.strftime(record.date_fin,"%Y%m%d"))


    #             Heure_debut = int(datetime.strftime(record.date_debut,"%H%M")) + 100
    #             Heure_fin = int(datetime.strftime(record.date_fin,"%H%M")) + 100

    #             logging.info("heeeeeeeeeeeeeeeeeeeeurrrrrrrrrrrrrrre")
    #             logging.info(Heure_debut)
    #             logging.info(Heure_fin)

    #             val = {
    #                 "id":record.num_intervention,
    #                 "date":date_debut,
    #                 "hour":str(Heure_debut),
    #                 "dateF":date_fin,
    #                 "hourF":str(Heure_fin),
    #                 "rep": record.collaborateur.code,
    #                 "rep2":record.collaborateur2.code
    #             }

    #             data = dumps(val)

    #             logging.info("daaaaaaaaataaaaaaaaaaaaaaa")
    #             logging.info(data)

    #             reponse = requests.request("POST",webservice_url,headers=headers, data=data)

    #             logging.info(reponse.json())

    #             return reponse








    @api.depends("date_fin","date_debut")

    def get_data (self):

        for record in self :


            if record.date_debut :


                record.date_invisible = record.date_debut.strftime("%Y-%m-%d")

            if record.date_fin :

                date_invisible_fin = record.date_fin.strftime("%Y-%m-%d")

            logging.info("datttttttttttttttttttte")
            logging.info(record.date_invisible)

            if not record.effectue :

                record.date_fin_planifier = record.date_fin
                record.date_debut_planifier = record.date_debut

      
    def search_state(self,cle):
        
        state = self.env['intervention.state_intervention'].search([("code","=",cle)])

        return state



    @api.depends("collaborateur","date_fin","effectue","fixe")

    def get_state (self):
        
        date_now =datetime.now()

        logging.info("fixxxxxxxxxxxxxxxe")
        logging.info(date_now)

        for record in self :

            if not record.fixe :

                if not record.collaborateur :

                    state = self.search_state("AP")

                    logging.info(state)

                    logging.info(state.color)
                    record.state_id = state.id

                    record.color =state.color

                elif record.effectue :

                    state = self.search_state("TR")
                    record.state_id = state.id
                    record.color = state.color


                
                elif date_now>record.date_fin:

                        state = self.search_state("ER")
                        record.state_id = state.id
                        record.color = state.color

                elif record.planifier :

                    state = self.search_state("PL")
                    record.state_id = state.id
                    record.color = state.color

                elif record.encour :

                    state = self.search_state("EC")
                    record.state_id = state.id
                    record.color = state.color
                

                else :
                    state = self.search_state("AF")
                    record.state_id = state.id
                    record.color = state.color

                # if record.effectue :
                #     record.color = "#6E9534"

                # else :
                #     record.color = "#ECCD31"
            else :
            
                record.state_id = self._default_stage_id()
            



    def write(self,val):
        logging.info("writtttttttttttttttttttte")
        logging.info(val)

        if self.duplic_inter or self.effectue :

            # raise Warning(_("Impossible de modifier le fiche d'intervention"))

            return {
                    'type': 'ir.actions.client',
                    'tag': 'reload',
                }

        date_time_now =datetime.now()


        if "style" in val :

            logging.info("styllllllllllllllllllllllllllllllle")

            val["collaborateur"]= False

        if "date_debut" in val and "date_fin" in val :

            date_debut = datetime.strptime(str(val["date_debut"]),'%Y-%m-%d %H:%M:%S')

            if "collaborateur" in val and self.planifier == True :

                if self.collaborateur.id != val["collaborateur"] :

                    val["planifier"] = False

                elif self.date_debut != date_debut :

                    val["planifier"] = False


            if val["date_debut"] == 'Invalid date' and val["date_fin"] == 'Invalid date':

                logging.info("Invaliddddddddddddddddd dateeeeeeeeeeeeeeeeeeeeeeee ")

                val["date_debut"] = self.date_debut
                val["date_fin"] = self.date_fin

                return super().write(val)

        # if "effectue" not in val :

        #     if "date_debut" in val and "date_fin" not in val and "collaborateur" not in val :

        #         date_debut = datetime.strptime(str(val["date_debut"]),'%Y-%m-%d %H:%M:%S')

        #         #self.controle_date(self.collaborateur.id,date_debut,self.date_fin)

        #         if date_debut <= date_time_now :

        #             return {
        #                 'type': 'ir.actions.client',
        #                 'tag': 'reload',
        #            }

        #         intervention = self.env["intervention.intervention"].sudo().search(['&','&',('collaborateur',"=",self.collaborateur.id),('num_intervention',"!=",self.num_intervention),('effectue','=',False),('fixe',"=",False)])

        #         if intervention :

        #             for record in intervention :


        #                 if (date_debut >= record.date_debut and self.date_fin <= record.date_fin) or (self.date_fin >= record.date_debut and date_debut <= record.date_fin):

        #                     return {
        #                         'type': 'ir.actions.client',
        #                         'tag': 'reload',
        #                             }

        #     if "date_debut" in val and "date_fin" in val and "collaborateur" not in val :

        #         date_debut = datetime.strptime(str(val["date_debut"]),'%Y-%m-%d %H:%M:%S')
        #         date_fin = datetime.strptime(str(val["date_fin"]),'%Y-%m-%d %H:%M:%S')

        #         # self.controle_date(self.collaborateur.id,date_debut,date_fin)



        #         if date_debut <= date_time_now :


        #             return {
        #                 'type': 'ir.actions.client',
        #                 'tag': 'reload',
        #             }

        #         intervention = self.env["intervention.intervention"].sudo().search(['&','&',('collaborateur',"=",self.collaborateur.id),('num_intervention',"!=",self.num_intervention),('effectue','=',False),('fixe',"=",False)])

        #         if intervention :

        #             for record in intervention :


        #                 if (date_debut >= record.date_debut and date_fin <= record.date_fin) or (date_fin >= record.date_debut and date_debut <= record.date_fin):

        #                     return {
        #                         'type': 'ir.actions.client',
        #                         'tag': 'reload',
        #                             }

        #     if "date_debut" in val and "date_fin" in val and "collaborateur" in val :

        #         date_debut = datetime.strptime(str(val["date_debut"]),'%Y-%m-%d %H:%M:%S')
        #         date_fin = datetime.strptime(str(val["date_fin"]),'%Y-%m-%d %H:%M:%S')

        #         # self.controle_date(val['collaborateur'],date_debut,date_fin)

        #         if date_debut <= date_time_now :

        #             return {
        #                 'type': 'ir.actions.client',
        #                 'tag': 'reload',
        #             }

        #         intervention = self.env["intervention.intervention"].sudo().search(['&','&',('collaborateur',"=",val['collaborateur']),('num_intervention',"!=",self.num_intervention),('effectue','=',False),('fixe',"=",False)])

        #         if intervention :

        #             for record in intervention :


        #                 if (date_debut >= record.date_debut and date_fin <= record.date_fin) or (date_fin >= record.date_debut and date_debut <= record.date_fin):

        #                     return {
        #                         'type': 'ir.actions.client',
        #                         'tag': 'reload',
        #                             }

        #     if "date_debut" not in val and "date_fin" not in val and "collaborateur" in val :

        #         if self.date_debut <= date_time_now :

        #             return {
        #                 'type': 'ir.actions.client',
        #                 'tag': 'reload',
        #             }

        #         intervention = self.env["intervention.intervention"].sudo().search(['&','&',('collaborateur',"=",val['collaborateur']),('num_intervention',"!=",self.num_intervention),('effectue','=',False),('fixe',"=",False)])

        #         if intervention :

        #             for record in intervention :


        #                 if (self.date_debut >= record.date_debut and self.date_fin <= record.date_fin) or (self.date_fin >= record.date_debut and self.date_debut <= record.date_fin):

        #                     return {
        #                         'type': 'ir.actions.client',
        #                         'tag': 'reload',
        #                             }

        intervention_dupli=self.env["intervention.intervention"].sudo().search([('num_intervention',"=",self.num_intervention),('duplic_inter',"=",True)])

        if "collaborateur2" in val :
 
            if val["collaborateur2"] :

                if intervention_dupli :

                    intervention_dupli.sudo().unlink()
                    self.sudo().copy(default={'collaborateur':val["collaborateur2"],"collaborateur2":"","duplic_inter":True})

                else:

                    logging.info("dupppppppppppppppppppppppppppppliquer")
                    self.sudo().copy(default={'collaborateur':val["collaborateur2"],"collaborateur2":"","duplic_inter":True})
            else :

                if intervention_dupli :

                    intervention_dupli.sudo().unlink()

        result = super().write(val)

        if result :

            if "date_debut" in val or "date_fin" in val or "effectue" in val :

                if intervention_dupli:

                    intervention_dupli.sudo().unlink()
                    self.sudo().copy(default={'collaborateur':self.collaborateur2.id,"collaborateur2":"","duplic_inter":True})

        return result





    # def controle_date(self,collaborateur,date_debut,date_fin):

    #     date_time_now =datetime.now()

    #     logging.info("date_time_nowwwwwwwwwwwww")

    #     logging.info(self.num_intervention)
    #     logging.info(collaborateur)
    #     logging.info(date_debut)

        

    #     controle = False

    #     reload_int =False





    #     if date_debut <= date_time_now :

    #         return {
    #                 'type': 'ir.actions.client',
    #                 'tag': 'reload',
    #             }


    #     intervention = self.env["intervention.intervention"].sudo().search(['&','&',('collaborateur',"=",collaborateur),('num_intervention',"!=",self.num_intervention),('effectue','=',False),('fixe',"=",False)])





        









    @api.depends("collaborateur","collaborateur2")
    def get_collaborateur (self):

        for record in self:

            if record.collaborateur.nom :

                    record.nom_collaborateur = str(record.collaborateur.nom )

            if record.collaborateur2.nom :

                    record.nom_collaborateur2 = str(record.collaborateur2.nom)
            



    @api.depends("interlocuteur")
    def get_interlocuteur (self):

        for record in self:

            if record.interlocuteur.nom and record.interlocuteur.prenom :

                record.nom_interlocuteur = str(record.interlocuteur.nom + " " +record.interlocuteur.prenom)

                

    def name_get(self):
        rec = []
        for record in self:
            rec.append((record.id,record.demande_service))
        return rec




class State_intervention(models.Model):

    _name = 'intervention.state_intervention'
    _description = 'statut Intervention'

    code = fields.Char("Code")
    intitule = fields.Char("Intitulé")
    color = fields.Char("Code couleur ")

    def name_get(self):
        rec = []
        for record in self:
            rec.append((record.id,record.intitule))

        return rec



class TypeIntervention(models.Model):

    _name = 'intervention.type_intervention'
    _description = 'Type Intervention'

    code = fields.Char("Code")
    intitule = fields.Char("Intitulé")
    color = fields.Char("Color")

    def name_get(self):
        rec = []
        for record in self:
            rec.append((record.id,record.intitule))

        return rec

class NatureIntervention(models.Model):

    _name = 'intervention.nature_intervention'
    _description = 'Nature Intervention'

    code = fields.Char("Code")
    intitule = fields.Char("Intitulé")

    def name_get(self):
        rec = []
        for record in self:
            rec.append((record.id,record.code))

        return rec

class RapportIntervention(models.Model):

    _name = 'intervention.rapport_intervention'
    _description = 'Rapport Intervention'

    nom = fields.Char("Nom Document")
    url = fields.Char('URL', default='https://www.odoo.com',readonly=True)
    intervention_id = fields.Many2one("intervention.intervention")

    def name_get(self):
        rec = []
        for record in self:
            rec.append((record.id,record.nom))

        return rec


class Validation(models.TransientModel):

    _name = 'validation_planif'


    def _default_date_debut(self):

        import datetime 
        import calendar

        tody = datetime.datetime.today().weekday()

        semaine = str(calendar.day_name[tody])


        if semaine == "Monday":

            return datetime.datetime.today()


        elif semaine == "Tuesday":

            tody = datetime.datetime.today() - datetime.timedelta(days=1)

            return tody


        elif semaine == "Wednesday":

            tody = datetime.datetime.today() - datetime.timedelta(days=2)

            return tody


        elif semaine == "Thursday":

            tody = datetime.datetime.today() - datetime.timedelta(days=3)

            return tody


        elif semaine == "Friday":
            tody = datetime.datetime.today() - datetime.timedelta(days=4)

            return tody

        else :

            tody = datetime.datetime.today() - datetime.timedelta(days=5)

            return tody


    def _default_date_fin(self):

        import datetime 
        import calendar

        tody = datetime.datetime.today().weekday()

        semaine = str(calendar.day_name[tody])


        if semaine == "Monday":

            tody = datetime.datetime.today() + datetime.timedelta(days=5)

            return tody


        elif semaine == "Tuesday":

            tody = datetime.datetime.today() + datetime.timedelta(days=4)

            return tody


        elif semaine == "Wednesday":

            tody = datetime.datetime.today() + datetime.timedelta(days=3)

            return tody


        elif semaine == "Thursday":

            tody = datetime.datetime.today() + datetime.timedelta(days=2)

            return tody


        elif semaine == "Friday":
            tody = datetime.datetime.today() + datetime.timedelta(days=1)

            return tody
        else :

            return datetime.datetime.today()
        
        

    date_debut = fields.Date("Date Début",default=_default_date_debut)
    date_fin = fields.Date('Date Fin',default=_default_date_fin)


    def set_segex3(self):
        import datetime

        webservice_url = "http://192.168.10.20:4000/api/interventions/updateinterventiondateodoo"
        headers = {'Content-type': 'application/json'}

        intervention = self.env["intervention.intervention"].sudo().search([('fixe',"=",False)])

        logging.info("lisssssssssssst d'intervention")

        logging.info(intervention)

        dt_debut = datetime.datetime.combine(self.date_debut, datetime.time(0, 0))
        dt_fin = datetime.datetime.combine(self.date_fin, datetime.time(23, 59))

        logging.info(dt_debut)
        logging.info(dt_fin)

        for record in intervention :

            if (dt_debut <= record.date_debut) and (dt_fin >= record.date_debut):


                if record.collaborateur and record.code_state == "AF":

                    logging.info("set_sage_xxxxxxxxxxxxxxxxxx333")

                    logging.info(record.num_intervention)

                    date_debut = (datetime.datetime.strftime(record.date_debut,"%Y%m%d"))
                    date_fin = (datetime.datetime.strftime(record.date_fin,"%Y%m%d"))

                    Heure_debut = int(datetime.datetime.strftime(record.date_debut,"%H%M")) + 100
                    Heure_fin = int(datetime.datetime.strftime(record.date_fin,"%H%M")) + 100

                    val = {
                        "id":record.num_intervention,
                        "date":date_debut,
                        "hour":str(Heure_debut),
                        "dateF":date_fin,
                        "hourF":str(Heure_fin),
                        "rep": record.collaborateur.code,
                        "rep2":record.collaborateur2.code
                    }

                    data = dumps(val)

                    reponse = requests.request("POST",webservice_url,headers=headers, data=data)

                    record.sudo().write({"planifier":True})

        





