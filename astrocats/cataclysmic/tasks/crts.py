"""Import tasks for the Catalina Real-Time Transient Survey. Currently not functioning as intended."""
import os
import re

from astrocats.catalog.utils import is_number, pbar
from astrocats.catalog.photometry import PHOTOMETRY
from bs4 import BeautifulSoup

from decimal import Decimal

from astrocats.cataclysmic.cataclysmic import CATACLYSMIC


def do_crts(catalog):
    """Import data from the Catalina Real-Time Transient Survey."""
    crtsnameerrors = ['2011ax']
    task_str = catalog.get_current_task_str()
    folders = ['catalina', 'catalina','catalina','catalina','MLS', 'MLS','MLS','MLS','catalina']#, 'SSS']
    files = ['CRTSII_BrightCV.html', 'AllSNCV.arch.html', 'CRTSII_CV.html', 'CRTSII_SNCV.html',
	     'CRTSII_BrightCV.html', 'AllSNCV.arch.html', 'CRTSII_CV.html', 'CRTSII_SNCV.html','AllCV.arch.html']
    for fi, fold in enumerate(pbar(folders, task_str)):
        html = catalog.load_url(
            'http://nesssi.cacr.caltech.edu/' + fold + '/' + files[fi],
            os.path.join(catalog.get_current_task_repo(), 'CRTS', fold + '-' +
                         files[fi]), archived_mode=('arch' in files[fi]))
        html = html.replace('<ahref=', '<a href=')
        if not html:
            continue
        bs = BeautifulSoup(html, 'html5lib')
        trs = bs.findAll('tr')
        for tr in pbar(trs, task_str):
            tds = tr.findAll('td')
            if not tds:
                continue
            # refs = []
            aliases = []
            name = ''
            ra = ''
            dec = ''
            mag = ''
            discdate = ''
            comment = ''
            atellink = ''
            # ttype = ''
            # ctype = ''
            for tdi, td in enumerate(tds):
                if tdi == 0:
                    object_name = td.text.strip().replace(':', '_')
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
                     url='http://nesssi.cacr.caltech.edu/' + fold + '/' + files[fi], name='crts Transients')]
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
#                catalog.entries[name].add_quantity(CATACLYSMIC.ALIAS, name, sources)
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