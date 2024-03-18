import logging
import os
import subprocess
import httpx
import more_itertools
from time import sleep, time

from requests_html import HTML
from urllib.parse import urldefrag

from functools import partial
from tqdm import tqdm as std_tqdm

from logger import TqdmLogger
from std import TqdmMultiProcessPool

from requests.exceptions import ConnectionError
from requests.exceptions import RequestException

# make directories
os.makedirs(save_dir := 'dc', exist_ok=True)
os.makedirs(seed_dir := 'seed', exist_ok=True)

# scraper config
process_count = 2
session = httpx.Client(http2=True)  # https://stackoverflow.com/a/70706028
cookies = {
}
headers = {
}

# scraping range
recursive = False
domain = ''
base = ('', )
seed = {f'https://fr.wiktionary.org/?curid={i}' for i in range(11111)}
fetched_url_path = f'{seed_dir}/merged-file'
entry_css = {'.ns-0', '.ns-14', '.ns-100', '.ns-102', '.ns-104', '.ns-106', '.ns-110', '.ns-114', '.ns-118'}

# logging set-up
vlog = TqdmLogger()  # console and file (vocal)
clog = TqdmLogger(mode='c')  # console-only
save = TqdmLogger(mode='f')  # file-only without format

# progress bar style
tqdm = partial(std_tqdm, dynamic_ncols=True, colour='#008080')


def get_rhtml(url):
    while True:
        try:
            r = session.get(url, cookies=cookies, headers=headers, follow_redirects=False, timeout=20)
            html = HTML(html=r.text)
        except ConnectionError as err:
            vlog.e(f'{err} | {url}')
        except RequestException as err:
            vlog.e(f'{err} | {url}')
        except BaseException as err:
            vlog.c(f'{err} | {url}')  # traceback.print_exc()
        else:
            msg = f'{r.status_code} | {url.split("/", 3)[-1]}'
            hds = dict(r.headers)
            if 'Connection' in hds and hds['Connection'] == 'close':
                vlog.e(f'Connection refused | {url}')  # https://stackoverflow.com/a/24899222
            elif r.status_code == 429:
                clog.w(msg)
            elif r.status_code != 200:  # {302, 400, 404, 500}
                vlog.w(msg)
                save.w(url, filename='RETRY_URL', filepath=seed_dir)
                return None
            else:
                vlog.i(msg)
                return html
        sleep(5)


def get_urls(rh):
    set_hr = set()
    for link in rh.absolute_links:
        link = link.replace('https://example.org', domain)
        if link.startswith(base):
            hr = urldefrag(link).url
            # hr = hr.split('?q=')[0]
            # hr = hr.replace('?t=1', '')
            set_hr.add(hr)
    return set_hr


def get_dc(rh):
    for css in entry_css:
        if (des := rh.find(css)):
            dc = ''.join(de.html for de in des).replace('\n', '')
            return dc


def iter_m(url, tqdm_func, global_tqdm):
    set_hr = set()
    if (rh := get_rhtml(url)):
        if recursive:
            set_hr = get_urls(rh)
        if (dc := get_dc(rh)):
            save.i(url, filename='FETCHED_URL', filepath=seed_dir)
            save.i(f'<dc_url>{url}</dc_url>{dc}', filename='dc', filepath=save_dir)  # f'{os.getpid()}'
    global_tqdm.update()
    return set_hr


def wget_m(set_u, set_d, max_cs=2500):
    i = 0
    while True:
        with tqdm(total=len(set_u)) as g_pb:
            if recursive:
                g_pb.set_description(f'Batch {i + 1}')

            sets_hr = []
            fn_x = ([iter_m, (url,)] for url in set_u)
            for fn_x_i in more_itertools.chunked(fn_x, max_cs):
                with TqdmMultiProcessPool(process_count) as pool:
                    sets_hr += pool.map(g_pb, fn_x_i)

        yield (set_hr := set().union(*sets_hr))

        with open(f'{seed_dir}/set_u', 'w') as f_u, open(f'{seed_dir}/set_d', 'w') as f_d:
            f_u.write('\n'.join(set_u := set_hr - set_d))
            f_d.write('\n'.join(set_d := set_hr | set_d))

        if not set_u:
            break
        i += 1


def main():
    try:
        with open(f'{seed_dir}/set_u', 'r') as fu, open(f'{seed_dir}/set_d', 'r') as fd:
            set_u = set(fu.read().split('\n')) - {''}
            set_d = set(fd.read().split('\n')) - {''}
    except FileNotFoundError:
        seed_c = set(seed)
        if os.path.exists(fetched_url_path):
            with open(fetched_url_path, 'r') as f:
                seed_c = seed - set(f.read().split('\n'))
        set_u = set_d = seed_c

    for _ in wget_m(set_u, set_d):
        pass


if __name__ == '__main__':
    main()

