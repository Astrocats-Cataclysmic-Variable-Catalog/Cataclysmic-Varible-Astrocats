# -*- coding: utf-8 -*- 173
"""ASCII datafiles.

Often produced from LaTeX tables in the original papers,
but sometimes provided as supplementary datafiles on the journal webpages.
"""
import csv
import os
import re
from datetime import datetime
from decimal import Decimal
from glob import glob

from astrocats.catalog.photometry import PHOTOMETRY, set_pd_mag_from_counts
from astrocats.catalog.utils import (is_number, jd_to_mjd, make_date_string,
                                     pbar, pbar_strings)
from astropy import units as u
from astropy.coordinates import SkyCoord as coord
from astropy.io.ascii import read
from astropy.time import Time as astrotime

from ..cataclysmic import CATACLYSMIC


def do_murawski(catalog):
    """Process csv files extracted from datatables of various online works."""
    task_str = catalog.get_current_task_str()


    # Howerton Catalog
    datafile = os.path.join(catalog.get_current_task_repo(), 'MURAWSKI',
                            'murawski_dwarf_nova.csv')
    data = read(datafile, format='csv')
    for rrow in pbar(data, task_str):
        row = dict((x, str(rrow[x])) for x in rrow.columns)
#        if any(x in row['Notes'].lower() for x in ['artifact']):
#            continue
#        ctypes = row['Type'].split('/')
#        nonsne = False
#        for ct in ctypes:
#            if ct.replace('?', '') in catalog.nonsnetypes:
#                nonsne = True
#            else:
#                nonsne = False
#                break
#        if nonsne:
#            continue
        name, source = catalog.new_entry(
            row['ZTF_name'],
            srcname='Murawski',
            url='http://scan.sai.msu.ru/~denis/MGAB-ZTF.html')
#        if row['IAU des.'] != '--':
#            catalog.entries[name].add_quantity(SUPERNOVA.ALIAS,
#                                               row['IAU des.'], source)
#        for ct in ctypes:
#            catalog.entries[name].add_quantity(SUPERNOVA.CLAIMED_TYPE, ct,
#                                               source)
#        catalog.entries[name].add_quantity(SUPERNOVA.DISCOVERER,
#                                           row['Discoverer'], source)
#        date = row['Discovery'].split('/')
#        date = '/'.join([date[-1].zfill(2), date[0].zfill(2), date[1]])
#        catalog.entries[name].add_quantity(SUPERNOVA.DISCOVER_DATE, date,
#                                           source)
        catalog.entries[name].add_quantity(CATACLYSMIC.MAX_VISUAL_APP_MAG, row['MAG'],
                                           source)
        catalog.entries[name].add_quantity(CATACLYSMIC.RA, row['RA'], source)
        catalog.entries[name].add_quantity(CATACLYSMIC.DEC, row['DEC'], source)
        catalog.entries[name].add_quantity(CATACLYSMIC.ALIAS, row['Variable_name'], source)
        catalog.entries[name].add_quantity(CATACLYSMIC.CLAIMED_TYPE,
                                               'Dwarf Nova', source)
    catalog.journal_entries()

    # Howerton Catalog
#    datafile = os.path.join(catalog.get_current_task_repo(), 'ASCII',
#                            'howerton-catalog.csv')
#    data = read(datafile, format='csv')
#    for rrow in pbar(data, task_str):
#        row = dict((x, str(rrow[x])) for x in rrow.columns)
#        if any(x in row['Notes'].lower() for x in ['artifact']):
#            continue
#        ctypes = row['Type'].split('/')
#        nonsne = False
#        for ct in ctypes:
#            if ct.replace('?', '') in catalog.nonsnetypes:
#                nonsne = True
#            else:
#                nonsne = False
#                break
#        if nonsne:
#            continue
#        name, source = catalog.new_entry(
#            row['SNHunt des.'],
#            srcname='CRTS SNhunt',
#            bibcode='2017csnh.book.....H')
#        if row['IAU des.'] != '--':
#            catalog.entries[name].add_quantity(SUPERNOVA.ALIAS,
#                                               row['IAU des.'], source)
#        for ct in ctypes:
#            catalog.entries[name].add_quantity(SUPERNOVA.CLAIMED_TYPE, ct,
#                                               source)
#        catalog.entries[name].add_quantity(SUPERNOVA.DISCOVERER,
#                                           row['Discoverer'], source)
#        date = row['Discovery'].split('/')
#        date = '/'.join([date[-1].zfill(2), date[0].zfill(2), date[1]])
#        catalog.entries[name].add_quantity(SUPERNOVA.DISCOVER_DATE, date,
#                                           source)
#        catalog.entries[name].add_quantity(SUPERNOVA.HOST, row['Host galaxy'],
#                                           source)
#        catalog.entries[name].add_quantity(SUPERNOVA.RA, row['RA'].replace(
#            'h', ':').replace('m', ':').replace('s', ''), source)
#        catalog.entries[name].add_quantity(SUPERNOVA.DEC, row['Dec'], source)
#    catalog.journal_entries()