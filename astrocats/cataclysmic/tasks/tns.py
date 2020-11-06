"""Import tasks for the Transient Name Server."""
import csv
import json
import os
import time
import urllib
import warnings
from datetime import datetime, timedelta
from math import ceil
from astropy.io.ascii import read

import requests

from astrocats.catalog.photometry import PHOTOMETRY
from astrocats.catalog.spectrum import SPECTRUM
from astrocats.catalog.utils import (is_integer, is_number, jd_to_mjd, pbar,
                                     pretty_num, sortOD)
from decimal import Decimal

from ..cataclysmic import CATACLYSMIC

def do_tns(catalog):
    """Load TNS metadata."""
    session = requests.Session()
    task_str = catalog.get_current_task_str()
    tns_url = 'https://wis-tns.weizmann.ac.il/'
    search_url = ('https://wis-tns.weizmann.ac.il/'+
                  'search?&discovered_period_value=30&discovered_period_units=years'+
                  '&unclassified_at=0&classified_sne=0&include_frb=0&name=&name_like=0'+
                  '&isTNS_AT=all&public=all&ra=&decl=&radius=&coords_unit=arcsec&reporting_groupid%5B%5D=null'+
                  '&groupid%5B%5D=null&classifier_groupid%5B%5D=null&objtype%5B%5D=27'+
                  '&at_type%5B%5D=null&date_start%5Bdate%5D=&date_end%5Bdate%5D=&discovery_mag_min=&discovery_mag_max='+
                  '&internal_name=&discoverer=&classifier=&spectra_count=&redshift_min=&redshift_max=&hostname='+
                  '&ext_catid=&ra_range_min=&ra_range_max=&decl_range_min=&decl_range_max='+
                  '&discovery_instrument%5B%5D=null&classification_instrument%5B%5D=null&associated_groups%5B%5D=null'+
                  '&at_rep_remarks=&class_rep_remarks=&frb_repeat=all&frb_repeater_of_objid=&frb_measured_redshift=0'+
                  '&frb_dm_range_min=&frb_dm_range_max=&frb_rm_range_min=&frb_rm_range_max=&frb_snr_range_min='+
                  '&frb_snr_range_max=&frb_flux_range_min=&frb_flux_range_max=&num_page=500&display%5Bredshift%5D=1'+
                  '&display%5Bhostname%5D=1&display%5Bhost_redshift%5D=1&display%5Bsource_group_name%5D=1'+
                  '&display%5Bclassifying_source_group_name%5D=1&display%5Bdiscovering_instrument_name%5D=0'+
                  '&display%5Bclassifing_instrument_name%5D=0&display%5Bprograms_name%5D=0&display%5Binternal_name%5D=1'+
                  '&display%5BisTNS_AT%5D=0&display%5Bpublic%5D=1&display%5Bend_pop_period%5D=0'+
                  '&display%5Bspectra_count%5D=1&display%5Bdiscoverymag%5D=1&display%5Bdiscmagfilter%5D=1&display'+
                  '%5Bdiscoverydate%5D=1&display%5Bdiscoverer%5D=1&display%5Bremarks%5D=0&display%5Bsources%5D=0'+
                  '&display%5Bbibcode%5D=0&display%5Bext_catalogs%5D=0&format=csv')
    csvtxt = catalog.load_url(search_url,
                              os.path.join(catalog.get_current_task_repo(),
                                           'TNS', 'index.csv'))
    data = read(csvtxt, format='csv')
    for rrow in pbar(data, task_str):
        row = dict((x, str(rrow[x])) for x in rrow.columns)
        name = catalog.add_entry(row['Name'])
        source = catalog.entries[name].add_source(name='TNS', url=tns_url)
        if int(float(row['Discovery Mag/Flux'])) >= 8:
            catalog.entries[name].add_quantity(CATACLYSMIC.MAX_VISUAL_APP_MAG, row['Discovery Mag/Flux'],
                                               source)
        catalog.entries[name].add_quantity(CATACLYSMIC.RA, row['RA'], source)
        catalog.entries[name].add_quantity(CATACLYSMIC.DEC, row['DEC'], source)
        catalog.entries[name].add_quantity(CATACLYSMIC.DISCOVER_DATE, row['Discovery Date (UT)'].replace('-', '/'), source)
        catalog.entries[name].add_quantity(CATACLYSMIC.CLAIMED_TYPE, 'Cataclysmic_Variable', source)
    catalog.journal_entries()