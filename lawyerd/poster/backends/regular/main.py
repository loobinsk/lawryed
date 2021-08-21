import json
import logging
from typing import List

import requests
import tldextract
from bs4 import BeautifulSoup
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from templated_email import send_templated_mail  # noqa

from products.models import PRODUCT_TYPE
from ...main import Poster, ApiKey, DataModels, get_site_screenshot


class ProcessBackend(Poster):
    domains: List[str] = []
    default: bool = True
    help: str = 'Regular site, default'

    def get_site_screenshot(self):
        self.data_screenshot = get_site_screenshot(self.complaint_detail.site)

    def get_site_hosting(self):
        # self.data_hosting = 'ukr.net'
        # return None  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!

        res: str = ''
        content = ''

        try:
            domain_address = tldextract.extract(self.complaint_detail.site).registered_domain
            url = f'https://api.2ip.ua/hosting.json?site={domain_address}&key={ApiKey.API_KEY_2IP}'
            r = requests.get(url)

            if r.status_code != 200:
                raise Exception('api.2ip.ua status code != 200')

            content = json.loads(r.content)
            res = content['site']
        except Exception as e:  # noqa
            logging.error(f'Exception get_site_hosting: {e}, content: {content}')
            pass

        logging.info(f'get_site_hosting, result: {res}')
        self.data_hosting = res

    def get_site_hosting_abuse_email(self):
        if not self.data_hosting:
            logging.error('get_site_hosting_abuse_email empty')
            return None

        res: str = ''
        # domain = tldextract.extract(self.complaint_detail.site).registered_domain
        domain = tldextract.extract(self.data_hosting).registered_domain
        logging.info('registered domain: %s' % domain)

        # domain = tldextract.extract(self.complaint_detail.site).registered_domain
        # r = requests.get(f'https://www.abuse.net/lookup.phtml?domain={self.data_hosting}')
        r = requests.get(f'https://www.abuse.net/lookup.phtml?domain={domain}')

        try:
            if r.status_code == 200:
                soup = BeautifulSoup(r.content, features="html.parser")
                e = soup.findAll("tt")[0].text
                res = e
        except Exception as e:
            logging.error(f'get_domain_abuse_email, abuse.net: {e}')

        logging.info(f'get_site_hosting_abuse_email, result: {res}')
        self.data_site_abuse_email = res

    def send_complaint_email(self):
        # screenshot: bytes = self.complaint_detail.screenshot.read()

        if self.company.user.redirected_email:
            self.toemail = self.company.user.redirected_email

        self.toemail: str = self.data_site_abuse_email

        logging.info('send_complaint_email: %s' % self.toemail)

        res: DataModels.STATUS = DataModels.STATUS.error
        # to_email = 'i.makushinsky@gmail.com'  # TODO: CHECK !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # to_email = 'ahiy72k@chomagor.com'
        # to_email = 'koyeve3011@macosnine.com'  # TODO: CHECK !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        try:
            validate_email(self.toemail)
        except ValidationError as e:
            # logging.info("bad email, details:", e)
            logging.info('Email not set, skipped')
            return res
        else:
            logging.info("good email")

        if not self.data_site_abuse_email or not self.toemail:
            logging.info('Email not set, skipped')
            return res

        _APPLICATON_PDF_STR = 'application/pdf'

        mail_attachments = [
            ('screenshot.png', self.data_screenshot, 'image/png'),
            ('product.pdf', self.product.document.read(), _APPLICATON_PDF_STR),
        ]

        if self.company.document:
            mail_attachments.append(('confirmation.pdf', self.company.document.read(), _APPLICATON_PDF_STR))

        logging.info('Send email: %s' % self.toemail)

        self.template_name = f'poster_regular_{PRODUCT_TYPE[self.product.itype].lower()}'
        #self.toemail = 'sibesi2003@heroulo.com'

        try:
            send_templated_mail(
                template_name=self.template_name,
                from_email=ApiKey.API_NO_REPLY_EMAIL,
                recipient_list=[self.toemail],
                context=self.params_dict,
                attachments=mail_attachments,
            )
        except Exception as e:  # noqa
            logging.error(f"Ebay send email error: {e}")

        res = DataModels.STATUS.ok
        logging.info(f'Complaint detail : {self.complaint_detail.id} sended!!!!!!!!!!!!!!!!!!!!!!!!')
        # except Exception as e:
        #     print(f'Email send fail! {e}')

        self.data_status = res
        # return res
