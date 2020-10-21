"""Tasks related to the MASTER survey."""
import json
import os
import re
import numpy as np
from decimal import Decimal

from astrocats.catalog.photometry import PHOTOMETRY
from astrocats.catalog.utils import jd_to_mjd, pbar
from astropy.io.ascii import read
from bs4 import BeautifulSoup

from astrocats.cataclysmic.cataclysmic import CATACLYSMIC

def do_masterot(catalog):
    """Import list of MASTER events."""
    task_str = catalog.get_current_task_str()
    mast_url = 'http://observ.pereplet.ru/MASTER_OT.html'
    html = catalog.load_url(mast_url, os.path.join(
        catalog.get_current_task_repo(), 'MASTEROT/transients.html'))
    if not html:
        return
    bs = BeautifulSoup(html, 'html5lib')
#Issue, Only first ~1100 entries being read in. 
    table = bs.findAll("a", attrs={'href': re.compile(
           "^http://(master.sai.msu.ru|www.astronomerstelegram.org|gcn.gsfc.nasa.gov|observ.pereplet.ru|)")}) ####
    reduced_table = [(a.string, a.next_sibling) for a in table]
    unreduced_names = []
    values = []
    reduced_names = []
    ra = []
    dec = []
    reduced_date = []
    reduced_type = []
    reduced_mag = []
    for multiline in reduced_table[2:]:
#    print(multiline[0])
        if multiline[0] == None:
            continue
        if multiline[0].startswith(' MASTER') or multiline[0].startswith('MASTER'):
            if multiline[1] != ',':
                unreduced_names.append(multiline[0])
                values.append(multiline[1])
    values = [w.replace('     ', ' ') for w in values]
    for name in unreduced_names:
        if name[0] == ' ':
            name = name[1:]
        reduced_names.append(name)
        ra.append(name[10:12]+':'+name[12:14]+':'+name[14:19])
        dec.append(name[19:22]+':'+name[22:24]+':'+name[24:])

    for item in values:
        if item[0] == ' ':
            item = item[1:]
        if item[0:2] == '  ':
            item = item[2:]
        if item[0] == ' ':
            item = item[1:]
        reduced_date.append(item[0:12].replace('  ', ' ').replace(' ', '/').replace('.', ''))
        reduced_type.append(item[17:20].replace(' ', ''))
        reduced_mag.append(item[21:26].replace(' ', ''))
    for i in np.arange(len(reduced_names)):
        if reduced_type[i] == 'CV':
            name = catalog.add_entry(reduced_names[i])
            sources = [catalog.entries[name].add_source(
                url=mast_url, name='MAST-CV Transients')]
            typesources = sources[:]
            sources = ','.join(sources)
            typesources = ','.join(typesources)
            catalog.entries[name].add_quantity(CATACLYSMIC.ALIAS, name, sources)
            catalog.entries[name].add_quantity(
                CATACLYSMIC.DISCOVER_DATE, reduced_date[i], sources)
            catalog.entries[name].add_quantity(
                CATACLYSMIC.RA, ra[i], sources, u_value='floatdegrees')
            catalog.entries[name].add_quantity(
                CATACLYSMIC.DEC, dec[i], sources, u_value='floatdegrees')
            catalog.entries[name].add_quantity(CATACLYSMIC.CLAIMED_TYPE,
                                               'Known CV', sources)
            catalog.entries[name].add_quantity(
                        CATACLYSMIC.MAX_VISUAL_APP_MAG, reduced_mag[i], sources)
        if reduced_type[i] == 'CV?':
            name = catalog.add_entry(reduced_names[i])
            sources = [catalog.entries[name].add_source(
                url=mast_url, name='MAST-CV Transients')]
            typesources = sources[:]
            sources = ','.join(sources)
            typesources = ','.join(typesources)
            catalog.entries[name].add_quantity(CATACLYSMIC.ALIAS, name, sources)
            catalog.entries[name].add_quantity(
                CATACLYSMIC.DISCOVER_DATE, reduced_date[i], sources)
            catalog.entries[name].add_quantity(
                CATACLYSMIC.RA, ra[i], sources, u_value='floatdegrees')
            catalog.entries[name].add_quantity(
                CATACLYSMIC.DEC, dec[i], sources, u_value='floatdegrees')
            catalog.entries[name].add_quantity(CATACLYSMIC.CLAIMED_TYPE,
                                               'Candidate', sources)
            catalog.entries[name].add_quantity(
                        CATACLYSMIC.MAX_VISUAL_APP_MAG, reduced_mag[i], sources)
        if reduced_type[i] == 'DN':
            name = catalog.add_entry(reduced_names[i])
            sources = [catalog.entries[name].add_source(
                url=mast_url, name='MAST-CV Transients')]
            typesources = sources[:]
            sources = ','.join(sources)
            typesources = ','.join(typesources)
            catalog.entries[name].add_quantity(CATACLYSMIC.ALIAS, name, sources)
            catalog.entries[name].add_quantity(
                CATACLYSMIC.DISCOVER_DATE, reduced_date[i], sources)
            catalog.entries[name].add_quantity(
                CATACLYSMIC.RA, ra[i], sources, u_value='floatdegrees')
            catalog.entries[name].add_quantity(
                CATACLYSMIC.DEC, dec[i], sources, u_value='floatdegrees')
            catalog.entries[name].add_quantity(CATACLYSMIC.CLAIMED_TYPE,
                                               'Dwarf Nova', sources)
            catalog.entries[name].add_quantity(
                        CATACLYSMIC.MAX_VISUAL_APP_MAG, reduced_mag[i], sources)
        if reduced_type[i] == 'N':
            name = catalog.add_entry(reduced_names[i])
            sources = [catalog.entries[name].add_source(
                url=mast_url, name='MAST-CV Transients')]
            typesources = sources[:]
            sources = ','.join(sources)
            typesources = ','.join(typesources)
            catalog.entries[name].add_quantity(CATACLYSMIC.ALIAS, name, sources)
            catalog.entries[name].add_quantity(
                CATACLYSMIC.DISCOVER_DATE, reduced_date[i], sources)
            catalog.entries[name].add_quantity(
                CATACLYSMIC.RA, ra[i], sources, u_value='floatdegrees')
            catalog.entries[name].add_quantity(
                CATACLYSMIC.DEC, dec[i], sources, u_value='floatdegrees')
            catalog.entries[name].add_quantity(CATACLYSMIC.CLAIMED_TYPE,
                                               'Nova', sources)
            catalog.entries[name].add_quantity(
                        CATACLYSMIC.MAX_VISUAL_APP_MAG, reduced_mag[i], sources)
        if reduced_type[i] == 'AN':
            name = catalog.add_entry(reduced_names[i])
            sources = [catalog.entries[name].add_source(
                url=mast_url, name='MAST-CV Transients')]
            typesources = sources[:]
            sources = ','.join(sources)
            typesources = ','.join(typesources)
            catalog.entries[name].add_quantity(CATACLYSMIC.ALIAS, name, sources)
            catalog.entries[name].add_quantity(
                CATACLYSMIC.DISCOVER_DATE, reduced_date[i], sources)
            catalog.entries[name].add_quantity(
                CATACLYSMIC.RA, ra[i], sources, u_value='floatdegrees')
            catalog.entries[name].add_quantity(
                CATACLYSMIC.DEC, dec[i], sources, u_value='floatdegrees')
            catalog.entries[name].add_quantity(CATACLYSMIC.CLAIMED_TYPE,
                                               'AntiNova', sources)
            catalog.entries[name].add_quantity(
                        CATACLYSMIC.MAX_VISUAL_APP_MAG, reduced_mag[i], sources)
        if reduced_type[i] == 'NL':
            name = catalog.add_entry(reduced_names[i])
            sources = [catalog.entries[name].add_source(
                url=mast_url, name='MAST-CV Transients')]
            typesources = sources[:]
            sources = ','.join(sources)
            typesources = ','.join(typesources)
            catalog.entries[name].add_quantity(CATACLYSMIC.ALIAS, name, sources)
            catalog.entries[name].add_quantity(
                CATACLYSMIC.DISCOVER_DATE, reduced_date[i], sources)
            catalog.entries[name].add_quantity(
                CATACLYSMIC.RA, ra[i], sources, u_value='floatdegrees')
            catalog.entries[name].add_quantity(
                CATACLYSMIC.DEC, dec[i], sources, u_value='floatdegrees')
            catalog.entries[name].add_quantity(CATACLYSMIC.CLAIMED_TYPE,
                                               'Novalike CV', sources)
            catalog.entries[name].add_quantity(
                        CATACLYSMIC.MAX_VISUAL_APP_MAG, reduced_mag[i], sources)

        i += 1

    catalog.journal_entries()
    return