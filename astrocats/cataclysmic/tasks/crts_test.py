"""Tasks related to the crts survey test for debugging."""
import json
import os
import re
from decimal import Decimal

from astrocats.catalog.photometry import PHOTOMETRY
from astrocats.catalog.utils import jd_to_mjd, pbar
from astropy.io.ascii import read
from bs4 import BeautifulSoup

from astrocats.cataclysmic.cataclysmic import CATACLYSMIC


def do_crts_test(catalog):
    """Import list of crts events."""
    task_str = catalog.get_current_task_str()
    crts_url = 'http://nesssi.cacr.caltech.edu/catalina/AllCV.arch.html'
    html = catalog.load_url(asn_url, os.path.join(
        catalog.get_current_task_repo(), 'CRTS/catalina-ALLCV.arch.html'))
    if not html:
        return
    bs = BeautifulSoup(html, 'html5lib')
    trs = bs.find('table').findAll('tr')
    for tri, tr in enumerate(pbar(trs, task_str)):
        name = ''
        ra = ''
        dec = ''
        discdate = ''
        mag = ''
        atellink = ''
        comment = '' #store to check if entry is a CV later
        if tri == 1:
            continue
        tds = tr.findAll('td')
        for tdi, td in enumerate(tds):
            if tdi == 0:
                object_name = td.text.strip().replace(':', '_')
#                    atellink = td.find('a')
#                    if atellink:
#                        atellink = atellink['href']
#                    else:
#                        atellink = ''
            if tdi == 1:
                ra = td.text
            if tdi == 2:
                dec = td.text
            if tdi == 5:
                date = td.text
                discdate = '/'.join([date[:4], date[4:6], date[6:]])
            if tdi == 3:
                mag = td.text
            if tdi == 12:
                comment = td.text
        if 'CV' in comment:
            name = catalog.add_entry(object_name)
            sources = [catalog.entries[name].add_source(
                url=crts_url, name='crts CV')]
            typesources = sources[:]
            if atellink:
                sources.append(
                    (catalog.entries[name]
                     .add_source(name='ATel ' +
                                 atellink.split('=')[-1], url=atellink)))
#            if typelink:
#                typesources.append(
#                    (catalog.entries[name]
#                     .add_source(name='ATel ' +
#                                 typelink.split('=')[-1], url=typelink)))
            sources = ','.join(sources)
            typesources = ','.join(typesources)
#            catalog.entries[name].add_quantity(CATACLYSMIC.ALIAS, name, sources)
            catalog.entries[name].add_quantity(
                CATACLYSMIC.DISCOVER_DATE, discdate, sources)
            catalog.entries[name].add_quantity(CATACLYSMIC.RA, ra, sources,
                                               u_value='floatdegrees')
            catalog.entries[name].add_quantity(CATACLYSMIC.DEC, dec, sources,
                                               u_value='floatdegrees')
            catalog.entries[name].add_quantity(
                CATACLYSMIC.VISUAL_MAG, mag, sources)
#            for ct in claimedtype.split('/'):
#                if ct != 'Unk':
#                    catalog.entries[name].add_quantity(CATACLYSMIC.CLAIMED_TYPE, ct,
#                                                       typesources)

        else:
            pass

    catalog.journal_entries()
    return