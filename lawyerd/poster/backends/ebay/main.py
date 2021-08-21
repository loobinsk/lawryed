import logging
from typing import List

from templated_email import send_templated_mail  # noqa

from products.models import PRODUCT_TYPE
from ...main import Poster, ApiKey, DataModels, get_site_screenshot  # , SendAbuseExitCode


class ProcessBackend(Poster):
    domains: List[str] = ['ebay.com', ]
    process_email_send: bool = False
    default: bool = False
    help: str = 'Ebay backend'

    def get_site_screenshot(self):
        self.data_screenshot = get_site_screenshot(self.complaint_detail.site)

    def get_site_hosting(self):
        return ''

    def get_site_hosting_abuse_email(self):
        return ''

    def send_complaint_email(self):
        self.toemail = 'copyright@ebay.com'

        # to_email = 'i.makushinsky@gmail.com'  # TODO: CHECK !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # to_email = 'koyeve3011@macosnine.com'  # TODO: CHECK !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        if self.company.user.redirected_email:
            self.toemail = self.company.user.redirected_email

        res: DataModels.STATUS = DataModels.STATUS.error

        _APPLICATON_PDF_STR = 'application/pdf'

        mail_attachments = [
            ('screenshot.png', self.data_screenshot, 'image/png'),
            ('product.pdf', self.product.document.read(), _APPLICATON_PDF_STR),
        ]

        if self.company.document:
            mail_attachments.append(('confirmation.pdf', self.company.document.read(), _APPLICATON_PDF_STR))

        logging.info('Send email...')


        try:
            self.template_name = f'poster_ebay_{PRODUCT_TYPE[self.product.itype].lower()}'
            #self.toemail = 'sibesi2003@heroulo.com'

            send_templated_mail(
                template_name=self.template_name,
                # template_name=f'poster_regular_{PRODUCT_TYPE[self.product.itype].lower()}',
                from_email=ApiKey.API_NO_REPLY_EMAIL,
                recipient_list=[self.toemail],
                context=self.params_dict,
                attachments=mail_attachments,
            )
        except Exception as e:  # noqa
            logging.error(f"Ebay send email error: {e}")

        res = DataModels.STATUS.ok
        logging.info(f'Complaint detail : {self.complaint_detail.id} sended!!!!!!!!!!!!!!!!!!!!!!!!')

        self.data_status = res

        pass
