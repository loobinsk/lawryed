import importlib
import os
from abc import ABC, abstractmethod
from argparse import Namespace
from tempfile import NamedTemporaryFile
from typing import List

import validators
from django.core.files import File
from django.db.models.functions import Now
from googleapiclient.discovery import build  # noqa
from tldextract import extract

import complaint.models as data_module
import config.settings.base as settings_module
from webscreenshot.webscreenshot import take_screenshot


class DataModels:
    """
    Models avaliable from backends
    """
    Company = data_module.Company
    Product = data_module.Product

    Complaint = data_module.Complaint
    ComplaintDetail = data_module.ComplaintDetail

    STATUS = data_module.STATUS


class ApiKey:
    """
    Api Keys avaliable from backends
    """
    API_GOOGLE_SEARCH_KEY = settings_module.API_GOOGLE_SEARCH_KEY
    API_GOOGLE_SEARCH_CX = settings_module.API_GOOGLE_SEARCH_CX
    API_KEY_2IP = settings_module.API_KEY_2IP

    API_YOUTUBE_LOGIN = settings_module.API_YOUTUBE_LOGIN
    API_YOUTUBE_PASSWORD = settings_module.API_YOUTUBE_PASSWORD
    API_ANTICAPCTHA_KEY = settings_module.API_ANTICAPCTHA_KEY

    API_NO_REPLY_EMAIL = settings_module.API_NO_REPLY_EMAIL


class Poster(ABC):
    """
    Backend interface, you must subclass and implement all methods of this class!
    """

    domains: List[str] = []
    # process_email_send: bool = False
    default: bool = False
    help: str = 'Backend help string'

    complaint_detail: DataModels.ComplaintDetail
    company: DataModels.Company
    product: DataModels.Product

    data_screenshot: bytes = None
    data_hosting = None
    data_site_abuse_email = None
    data_status: DataModels.STATUS = DataModels.STATUS.error

    save_data: bool = True

    template_name = ''
    toemail = ''

    params_dict: dict

    def __init__(self, complaint_detail: DataModels.ComplaintDetail):
        print(f'Execute Poster: {complaint_detail.id}')
        self.template_name = ''
        self.toemail = ''

        self.complaint_detail = complaint_detail
        self.company: DataModels.Company = DataModels.Company.objects.filter(
            user_id=self.complaint_detail.complaint.user_id).first()
        self.product: DataModels.Product = DataModels.Product.objects.filter(
            complaint=self.complaint_detail.complaint).first()

        self.params_dict: dict = {
            'complaint_detail': self.complaint_detail,
            'company': self.company,
            'product': self.product,
        }

    def execute(self):
        print('Execute !!!!')
        self.get_site_screenshot()  # !!!!!!!!!!!!!
        # self.data_screenshot = b'\x7f\x45\x4c\x46\x01\x01\x01\x00'
        if not self.data_screenshot:
            self.finnalize()
            return None

        self.collect_data()

        # self.validate_data()
        self.finnalize()
        pass

    # @abstractmethod
    def collect_data(self):
        """
        Colect hosting, abuse email etc..
        """

        self.get_site_hosting()
        self.get_site_hosting_abuse_email()
        self.send_complaint_email()

    def finnalize(self):
        """
        Save data to database ?
        """
        if self.save_data:
            self.complaint_detail.status = self.data_status  # if site_status else DataModels.STATUS.error
            self.complaint_detail.email = self.toemail
            self.complaint_detail.hosting = self.data_hosting

            self.complaint_detail.template_name = self.template_name

            self.complaint_detail.finished = Now()

            if self.data_screenshot and len(self.data_screenshot) > 0:
                with NamedTemporaryFile(suffix='.png') as img_temp:
                    img_temp.write(self.data_screenshot)
                    img_temp.flush()
                    self.complaint_detail.screenshot.save('site_screenshot.png', File(img_temp))
            else:
                self.complaint_detail.status = DataModels.STATUS.error

            self.complaint_detail.save()

        print(
            f'Complaint detail executed, id: {self.complaint_detail.id}, status: {DataModels.STATUS[self.data_status]}, '
            f'data saved: {self.save_data}')
        pass

    @abstractmethod
    def get_site_screenshot(self):
        # self.data_screenshot = self.get_site_screenshot()
        pass

    @abstractmethod
    def get_site_hosting(self):
        pass

    @abstractmethod
    def get_site_hosting_abuse_email(self):
        pass

    @abstractmethod
    def send_complaint_email(self):
        pass


def get_sites_list(search_text: str, product_name: str, results_count: int = 10) -> List:
    res: List = []

    # link is direct URL ?
    if validators.url(search_text):
        return [search_text]

    # Use google search
    service = build("customsearch", "v1", developerKey=ApiKey.API_GOOGLE_SEARCH_KEY, credentials=None)
    page_index = 1

    while True:
        google_res = service.cse().list(q=f'{product_name} {search_text}', cx=ApiKey.API_GOOGLE_SEARCH_CX,
            start=page_index).execute()
        if 'items' not in google_res:
            break

        # analize google result
        for item in google_res['items']:
            link = item['link']
            res.append(link)

        if len(res) >= results_count:
            break

        page_index += 10  # dont change!

    res = res[:results_count]
    return res


def get_site_screenshot(url):
    res = None

    try:
        output_filename_obj = NamedTemporaryFile(suffix='.png')
        output_filename = output_filename_obj.name
        output_filename_obj.close()
        options = Namespace(
            single_output_file=output_filename, label=False, URL=None, cookie=None, header=None,
            http_password=None, http_username=None,
            input_file=None, log_level='DEBUG', multiprotocol=False, no_xserver=False,

            port=None, proxy=None, proxy_auth=None, proxy_type=None,
            renderer='chromium', renderer_binary=None, ssl=False, timeout=30, verbosity=2, window_size='1200,800',
            workers=1)

        take_screenshot([url], options)

        if os.path.exists(output_filename):
            with open(output_filename, 'rb') as f:
                res = f.read()
            os.remove(output_filename)

    except Exception as e:  # noqa
        print(f'get_site_screenshot exception: {str(e)}')

    return res


# get_site_screenshot('https://www.ebay.com/itm/Campark-4-3-LCD-Babyphone-Video-Monitor-Digitaler-2-4G-Nachtsichtkamera-Babyfone/402454452385?_trkparms=aid%3D111001%26algo%3DREC.SEED%26ao%3D1%26asc%3D20180816085401%26meid%3D21c70fadc8a540a0967aefbe7bcfec14%26pid%3D100970%26rk%3D1%26rkt%3D2%26mehot%3Dnone%26sd%3D402454452385%26itm%3D402454452385%26pmt%3D1%26noa%3D1%26pg%3D2380057&_trksid=p2380057.c100970.m5481&_trkparms=pageci%3A10c07987-84ad-11eb-b3e0-8aa737602ed7%7Cparentrq%3A30345b8b1780a69f890912aeffd196f6%7Ciid%3A1')
# get_site_screenshot('https://google.com')


# region 'BACKEND'
class BackendStorageClass:
    BACKENDS: List[Poster] = []
    BACKEND_DEFAULT: Poster  # = Poster()

    def __init__(self):
        _backend_path = 'backends'
        _backends_list_names = os.listdir(os.path.join(os.path.dirname(__file__), _backend_path))
        self.BACKENDS = [BackendStorageClass.get_backend_process_class(_backend_path, x) for x in _backends_list_names]

        if not self.BACKENDS:
            raise Exception('Backends not found!')

        _backend_default = [x for x in self.BACKENDS if x.default]

        if len(_backend_default)!=1:
            raise Exception('Must be only one default backend!')
        self.BACKEND_DEFAULT = _backend_default[0]

    @staticmethod
    def get_backend_process_class(backend_path: str, backend_name: str):
        """
        Get backend Process class
        :param backend_name: backend name
        :param backend_path: backend path name
        :return:
        """
        module_name = f'.{backend_path}.{backend_name.lower()}.main'
        backend_module = importlib.import_module(module_name, package='poster')
        res = backend_module.ProcessBackend  # noqa
        return res

    def get_url_backend(self, url: str) -> Poster:
        """
        Get Poster object depend on backend of URL
        :param url: URL
        :return: Poster
        """
        backend = self.BACKEND_DEFAULT

        domain = extract(url).registered_domain
        for x in self.BACKENDS:
            if not x.default and domain in x.domains:
                backend = x
                break

        res: Poster = backend
        return res


BackendStorage = BackendStorageClass()
# endregion
