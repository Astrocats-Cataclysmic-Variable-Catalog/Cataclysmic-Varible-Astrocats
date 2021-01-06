"""Tasks related to the ASASSN survey."""
import json
import os
import re
from decimal import Decimal

from astrocats.catalog.photometry import PHOTOMETRY
from astrocats.catalog.utils import jd_to_mjd, pbar
from astropy.io.ascii import read
from bs4 import BeautifulSoup

from astrocats.cataclysmic.cataclysmic import CATACLYSMIC


def do_lasair(catalog):
    """Import list of LASAIR events."""
    task_str = catalog.get_current_task_str()
    lars_url = 'https://lasair.roe.ac.uk/watchlist/26/'
    html = catalog.load_url(lars_url, os.path.join(
        catalog.get_current_task_repo(), 'LASAIR/transients.html'))
    if not html:
        return
    bs = BeautifulSoup(html, 'html5lib')
    trs = bs.find_all('table')[1]#.findAll('tr')
    trs = trs.findAll('tr')
    for tri, tr in enumerate(pbar(trs, task_str)):
        aliasname = ''
        ra = ''
        dec = ''
        discdate = ''
        mag = ''
        atellink = ''
        ztfname = ''
        classification = '' #store to check if entry is a CV later
#        if tri == 1:
#            continue
        tds = tr.findAll('td')
#        atex = 0
        for tdi, td in enumerate(tds):
            if tdi == 0:
                ra = td.text
            if tdi == 1:
                dec = td.text
            if tdi == 2:
                aliasname = ''.join(td.text)
            if tdi == 4:
                ztfname = ''.join(td.text)
            if tdi == 7:
                classification = td.text
        if 'CV' in classification:
            name = catalog.add_entry(ztfname)
            sources = [catalog.entries[name].add_source(
                name='Lasair The Transient Alert Broker for LSST UK', bibcode="2019RNAAS...3...26S",url=lars_url)]
            sources = ','.join(sources)
            catalog.entries[name].add_quantity(CATACLYSMIC.ALIAS, aliasname, sources)
            catalog.entries[name].add_quantity(CATACLYSMIC.RA, ra, sources,
                                               u_value='floatdegrees')
            catalog.entries[name].add_quantity(CATACLYSMIC.DEC, dec, sources,
                                               u_value='floatdegrees')
        else:
            pass

    catalog.journal_entries()
    return

#talk to professor about light curves data
#def do_asas_atels(catalog):
#    """Import LCs exposed in ASASSN Atels."""
#    with open('/root/better-atel/atels.json') as f:
#        ateljson = json.load(f)
#    for entry in ateljson:
#        if ('asas-sn.osu.edu/light_curve' in entry['body'] and
#                'Cataclysmic' in entry['subjects']):
#            matches = re.findall(r'<a\s+[^>]*?href="([^"]*)".*?>(.*?)<\/a>',
#                                 entry['body'], re.DOTALL)
#            lcurl = ''
#            objname = ''
#            for match in matches:
#                if 'asas-sn.osu.edu/light_curve' in match[0]:
#                    lcurl = match[0]
#                    objname = re.findall(
#                        r'\bASASSN-[0-9][0-9].*?\b', match[1])
#                    if len(objname):
#                        objname = objname[0]
#            if objname and lcurl:
#                name, source = catalog.new_entry(
#                    objname, srcname='ASAS-SN Sky Patrol',
#                    bibcode='2017arXiv170607060K',
#                    url='https://asas-sn.osu.edu')
#                csv = catalog.load_url(lcurl + '.csv', os.path.join(
#                    catalog.get_current_task_repo(), os.path.join(
#                        'ASASSN', objname + '.csv')))
#                data = read(csv, format='csv')
#                for row in data:
#                    mag = str(row['mag'])
#                    if float(mag.strip('>')) > 50.0:
#                        continue
#                    photodict = {
#                        PHOTOMETRY.TIME: str(jd_to_mjd(
#                            Decimal(str(row['HJD'])))),
#                        PHOTOMETRY.MAGNITUDE: mag.strip('>'),
#                        PHOTOMETRY.SURVEY: 'ASASSN',
#                        PHOTOMETRY.SOURCE: source
#                    }
#                    if '>' in mag:
#                        photodict[PHOTOMETRY.UPPER_LIMIT] = True
#                    else:
#                        photodict[PHOTOMETRY.E_MAGNITUDE] = str(row['mag_err'])
#                    catalog.entries[name].add_photometry(**photodict)
#    catalog.journal_entries()
#    return