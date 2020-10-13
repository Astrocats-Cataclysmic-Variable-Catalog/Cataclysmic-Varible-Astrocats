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


def do_ztf(catalog):
    """Process ztf files extracted from datatables of published ztf works."""
    task_str = catalog.get_current_task_str()
    files = ['ajab7ccet1_mrt_csv.csv','ajab7ccet2_mrt_csv.csv']
    for f in files:


        datafile = os.path.join(catalog.get_current_task_repo(), 'ZTF',
                                f)
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
                'ZTF'+row['name'],
                srcname='ZTF',
                bibcode='2020AJ....159..198S')
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
    #        catalog.entries[name].add_quantity(CATACLYSMIC.VISUAL_MAG, row['Vmax'],
    #                                           source)
            catalog.entries[name].add_quantity(CATACLYSMIC.RA, row['ra'], source)
            catalog.entries[name].add_quantity(CATACLYSMIC.DEC, row['dec'], source)
            catalog.entries[name].add_quantity(
                CATACLYSMIC.MAX_VISUAL_APP_MAG, row['mag'], source)
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