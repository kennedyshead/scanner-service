import json
import logging
import re

import coloredlogs
import pycountry
from pyisemail import is_email
from transcribe.image import OCR, Path

from matcher import is_phone_number, phone_number, is_webbadress, parse

_LOGGER = logging.getLogger(__name__)

coloredlogs.install(level='DEBUG', logger=_LOGGER)

regex = re.compile(r"[a-zA-ZåäöÅÄÖ]+")

# TODO Make all this save to database https://oss.redislabs.com/redisearch/

with open('languages/swedish/firstnames.json') as file:
    firstnames = json.load(file)

with open('languages/swedish/surnames.json') as file:
    surnames = json.load(file)


def scan(imagename):
    path = Path(imagename)
    data = OCR(path)
    try:
        data.scan()
    except IndexError:
        return

    person = []
    organization = []
    mail = []
    phone = []
    web = []
    country = []
    extra = []

    for line in data.unformatted.split("\n"):
        if is_email(line):
            mail.append(line.strip('.'))
            continue
        elif is_phone_number(line):
            res = phone_number.findall(line)
            if len(res) > 0:
                phone.append(res[0])
                continue
        elif is_webbadress(line):
            web.append(line)
            continue
        else:
            test = parse(line)
            if test is not False:
                for row in test:
                    if not isinstance(
                            row, tuple) and regex.search(row[0][0]) is None:
                        if row[0][0].capitalize() in firstnames or \
                                row[0][0].capitalize() in surnames:
                            person.append(row[0][0].capitalize())
                            continue
                        elif row.label() == 'PERSON':
                            person.append(row[0][0].capitalize())
                            continue
                        elif row.label() == 'ORGANIZATION':
                            organization.append(row[0][0].capitalize())
                            continue
                        elif row.label() == 'GPE':
                            try:
                                pycountry.countries.lookup(row[0][0])
                                country.append(row[0][0].capitalize())
                                continue
                            except LookupError:
                                pass

            extra.append(line)

    ret = {}
    if len(person) > 0:
        _LOGGER.info(f"person: {set(person)}")
        ret['person'] = person
    if len(organization) > 0:
        _LOGGER.info(f"Organization: {set(organization)}")
        ret['organization'] = organization
    if len(mail) > 0:
        _LOGGER.info(f"Mail: {set(mail)}")
        ret['mail'] = mail
    if len(phone) > 0:
        _LOGGER.info(f"Phone: {set(phone)}")
        ret['phone'] = phone
    if len(mail) > 0:
        _LOGGER.info(f"Web: {set(web)}")
        ret['web'] = web
    if len(mail) > 0:
        _LOGGER.info(f"Country: {set(country)}")
        ret['country'] = country
    if len(extra) > 0:
        _LOGGER.warning("##### Extra")
        _LOGGER.warning(extra)
        _LOGGER.warning("#####")
        ret['extra'] = extra
    return ret
