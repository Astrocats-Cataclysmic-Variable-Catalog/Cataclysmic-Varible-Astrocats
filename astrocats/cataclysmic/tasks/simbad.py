"""Import tasks for the SIMBAD astrophysical database.
"""
import re

from astroquery.simbad import Simbad

from astrocats.catalog.utils import is_number, pbar, single_spaces, uniq_cdl
from astrocats.cataclysmic.cataclysmic import CATACLYSMIC
from ..utils import name_clean


def do_simbad(catalog):
    # Simbad.list_votable_fields()
    # Some coordinates that SIMBAD claims belong to the SNe actually belong to
    # the host.
    task_str = catalog.get_current_task_str()
    simbadmirrors = ['http://simbad.harvard.edu/simbad/sim-script',
                     'http://simbad.u-strasbg.fr/simbad/sim-script']
    simbadbadcoordbib = ['2013ApJ...770..107C','Lasair']
    simbadbadtypebib = ['2014ApJ...796...87I', '2015MNRAS.448.1206M',
                        '2015ApJ...807L..18N']
    simbadbadnamebib = ['2004AJ....127.2809W', '2005MNRAS.364.1419Z',
                        '2015A&A...574A.112D', '2011MNRAS.417..916G',
                        '2002ApJ...566..880G','url:CBAT',
                        'url:GPSA']
    badurlbibname = ['url:TNS','url:ASASSN']
    simbadbannedcats = ['[TBV2008]', 'OGLE-MBR']
    simbadbannednames = ['SN']
    customSimbad = Simbad()
    customSimbad.ROW_LIMIT = -1
    customSimbad.TIMEOUT = 120
    customSimbad.add_votable_fields('otype', 'sptype', 'sp_bibcode', 'id')
    table = []
    print(customSimbad.SIMBAD_URL)
    for mirror in simbadmirrors:
        customSimbad.SIMBAD_URL = mirror
        try:
            table = customSimbad.query_criteria('maintypes=CV* | maintypes="CV?" | maintypes=No* | maintypes="No?"')
        except Exception:
            continue
        else:
            if not table:
                continue
            break

    if not table:
        catalog.log.warning('SIMBAD unable to load, probably offline.')

    # 2000A&AS..143....9W
    for brow in pbar(table, task_str):
        row = {x: re.sub(r'b\'(.*)\'', r'\1',
                         str(brow[x])) for x in brow.colnames}
        # Skip items with no bibliographic info aside from SIMBAD, too
        # error-prone
#        print(row)
        if (not row['COO_BIBCODE'] and not row['SP_BIBCODE'] and
                not row['SP_BIBCODE_2'] and not row['OTYPE'] == 'Nova' and 
                not row['OTYPE'] == 'DwarfNova'):
            continue
        if any([x in row['MAIN_ID'] for x in simbadbannedcats]):
            continue
        if row['COO_BIBCODE'] and row['COO_BIBCODE'] in simbadbadnamebib:
            continue
        name = single_spaces(re.sub(r'\[[^)]*\]', '', row['MAIN_ID']).strip()).replace('*','_')
        if name in simbadbannednames:
            continue
        if is_number(name.replace(' ', '')):
            continue
        name = catalog.add_entry(name)
        source = (catalog.entries[name]
                  .add_source(name='SIMBAD astronomical database',
                              bibcode="2000A&AS..143....9W",
                              url="http://simbad.u-strasbg.fr/",
                              secondary=True)).replace('*','_')
        if row['COO_BIBCODE'] == 'url:TNS':
            source = ','.join(
                [source, catalog.entries[name]
                  .add_source(name='Transient Name Server',
                              url='https://wis-tns.weizmann.ac.il/')])
        if row['COO_BIBCODE'] == 'url:ASASSN':
            source = ','.join(
                [source, catalog.entries[name]
                  .add_source(name='ASAS-CV Transients',
                              bibcode="2014ApJ...788...48S",
                              url='http://www.astronomy.ohio-state.edu/~assassin/transients.html')])
        aliases = row['ID'].split(',')
        for alias in aliases:
            if any([x in alias for x in simbadbannedcats]):
                continue
            ali = single_spaces(re.sub(r'\[[^)]*\]', '', alias).strip()).replace('*','_')
            if is_number(ali.replace(' ', '')):
                continue
            if ali in simbadbannednames:
                continue
            ali = name_clean(ali)
            catalog.entries[name].add_quantity(CATACLYSMIC.ALIAS,
                                               ali, source)
            catalog.entries[name].add_quantity(
                CATACLYSMIC.CLAIMED_TYPE,
                (row['OTYPE']
                 .replace('CV.', 'CV')
                 .replace('CV', 'CV')
                 .replace('(~)', '')
				 .replace('CV?', 'Candidate')
                 .replace('*', '')
                 .replace('No?', 'Candidate Nova')
                 .strip(': ')), source)
        if row['COO_BIBCODE'] and row['COO_BIBCODE'] not in simbadbadcoordbib:
            csources = source
            if row['COO_BIBCODE'] not in badurlbibname:
                csources = ','.join(
                    [source, catalog.entries[name].add_source(
                       bibcode=row['COO_BIBCODE'])])
            catalog.entries[name].add_quantity(CATACLYSMIC.RA,
                                               row['RA'], csources)
            catalog.entries[name].add_quantity(CATACLYSMIC.DEC,
                                               row['DEC'], csources)
            catalog.entries[name].add_quantity(
                CATACLYSMIC.CLAIMED_TYPE,
                (row['OTYPE']
                 .replace('CV.', 'CV')
                 .replace('CV', 'CV')
                 .replace('(~)', '')
				 .replace('CV?', 'Candidate')
                 .replace('*', '')
                 .replace('No?', 'Candidate Nova')
                 .strip(': ')), csources)
        if row['SP_BIBCODE'] and row['SP_BIBCODE'] not in simbadbadtypebib:
            ssources = source
            if row['SP_BIBCODE'] and row['SP_BIBCODE_2'] not in badurlbibname:
                ssources = uniq_cdl([source,
                                 catalog.entries[name]
                                 .add_source(bibcode=row['SP_BIBCODE'])] +
                                ([catalog.entries[name]
                                  .add_source(bibcode=row['SP_BIBCODE_2'])] if
                                 row['SP_BIBCODE_2'] else []))
            catalog.entries[name].add_quantity(
                CATACLYSMIC.CLAIMED_TYPE,
                (row['OTYPE']
                 .replace('CV.', 'CV')
                 .replace('CV', 'CV')
                 .replace('(~)', '')
				 .replace('CV?', 'Candidate')
                 .replace('*', '')
                 .replace('No?', 'Candidate Nova')
                 .strip(': ')), ssources)
        if row['OTYPE'] == 'Nova' and row['SP_BIBCODE'] == '' and row['COO_BIBCODE'] =='':
            catalog.entries[name].add_quantity(CATACLYSMIC.RA,
                                               row['RA'], source)
            catalog.entries[name].add_quantity(CATACLYSMIC.DEC,
                                               row['DEC'], source)
            catalog.entries[name].add_quantity(
                CATACLYSMIC.CLAIMED_TYPE,
                (row['OTYPE']), source)
        if row['OTYPE'] == 'DwarfNova' and row['SP_BIBCODE'] == '' and row['COO_BIBCODE'] =='':
            catalog.entries[name].add_quantity(CATACLYSMIC.RA,
                                               row['RA'], source)
            catalog.entries[name].add_quantity(CATACLYSMIC.DEC,
                                               row['DEC'], source)
            catalog.entries[name].add_quantity(
                CATACLYSMIC.CLAIMED_TYPE,
                (row['OTYPE']), source)
    catalog.journal_entries()
    return
