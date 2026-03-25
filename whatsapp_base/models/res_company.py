from odoo import models, fields, api, _
import urllib.request
from urllib.parse import quote
import requests
import json


class ResCompany(models.Model):
    _inherit = 'res.company'

    use_whatsapp_server = fields.Boolean(string="Use Whatsapp Server?")
    instance_id = fields.Char("Instance ID")
    whatsapp_access_token = fields.Char("Access Token")
    whatsapp_number = fields.Char('Whatsapp Number')
    whatsapp_url = fields.Char('URL')


    def get_whatsapp_url(self):
        whatsapp_number = self.whatsapp_number.replace(" ", "").replace("+", "").strip()
        url = self.whatsapp_url
        url += "/api/send?number=" + str(whatsapp_number)
        # url += "&type=text&message=" + str(self.text_message)
        url += "&instance_id=" + str(self.instance_id)
        url += "&access_token=" + str(self.whatsapp_access_token)
        return url


    def send_to_whatsapp(self, whatsapp_number, text_message, filename=None, media_url=None):
        print("DATAS ::::::::::: ", media_url, whatsapp_number, text_message)
        url = self.whatsapp_url
        whatsapp_number = whatsapp_number.replace(" ", "").replace("+", "").strip()
        encode_media_url = ''
        if media_url:
            url_parts = media_url.split("/")
            encoded_url = quote(url_parts[0], safe='')  # Encode scheme (http)
            encoded_url += "/" + "/".join(quote(part, safe='') for part in url_parts[1:])
            encode_media_url = encoded_url
        
        url += "/api/send?number=" + str(whatsapp_number)
        # url += "&type=text&message=" + str(text_message)
        url += "&type=media&message=" + text_message
        if media_url:
            url += "&media_url=" + encode_media_url
            url += "&filename=" + filename
        url += "&instance_id=" + str(self.instance_id)
        url += "&access_token=" + str(self.whatsapp_access_token)
        print("URL :::::::::::: ", url)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
        headers = {
              'Content-Type': 'application/json'
            }
        res = requests.post(url, headers=headers)
        print("RESPONSE ::::::::::::: ", res)
        if res.status_code == 200:
            response_data = json.loads(res.text)
            if isinstance(response_data, dict) and response_data.get('status') == 'success':
                print("MESSAGE SEND")



    