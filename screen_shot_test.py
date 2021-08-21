import os
from argparse import Namespace
from multiprocessing.spawn import freeze_support
from shutil import rmtree
from tempfile import mkdtemp

from webscreenshot import take_screenshot, filter_bad_filename_chars


def main():
    url = 'https://www.ebay.com/b/LGA-1155-Socket-H2-Computer-Processors/164/bn_649756?rt=nc&_sop=16'
    url = 'https://ukr.net'

    tmp_dir = mkdtemp()
    output_format = 'png'
    # output_filename = os.path.join(tmp_dir, f'site_screenshot.{output_format}')
    output_filename = os.path.join(tmp_dir, f'{filter_bad_filename_chars(url)}.{output_format}')
    # output_filename = 'c:\\2222.png'
    # output_filename = os.path.join(tmp_dir, ('%s.%s' % (filter_bad_filename_chars(url), output_format)))

    options = Namespace(URL=url, cookie=None, format=output_format, header=None, http_password=None,
                        http_username=None, input_file=None, log_level='ERROR', multiprotocol=False, no_xserver=False,
                        output_directory=tmp_dir, port=None, proxy=None, proxy_auth=None, proxy_type=None,
                        quality=75,

                        renderer='phantomjs',
                        # renderer='chromium',

                        renderer_binary=None,
                        ssl=False,
                        timeout=30, ajax_max_timeouts=30,
                        verbosity=0, window_size='1200,800', workers=1)
    take_screenshot([url], options)

    with open(output_filename, 'rb') as f:
        res = f.read()
        pass
    rmtree(tmp_dir, ignore_errors=True)

    print(f'len: {len(res)}')

if __name__ == '__main__':
    # freeze_support()
    main()
