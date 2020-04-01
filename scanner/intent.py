import logging

import coloredlogs
import pycountry
from pyisemail import is_email
from transcribe.image import OCR, Path

from matcher import is_phone_number, phone_number, is_webbadress, parse

_LOGGER = logging.getLogger(__name__)

coloredlogs.install(level='DEBUG', logger=_LOGGER)


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
            mail.append(line)
        elif is_phone_number(line):
            res = phone_number.findall(line)
            if len(res) > 0:
                phone.append(res[0])
        elif is_webbadress(line):
            web.append(line)
        else:
            test = parse(line)
            if test is not False:
                for row in test:
                    if not isinstance(row, tuple) and row.label() == 'PERSON':
                        person.append(row[0][0])
                    elif not isinstance(
                            row, tuple) and row.label() == 'ORGANIZATION':
                        organization.append(row[0][0])
                    elif not isinstance(row, tuple) and row.label() == 'GPE':
                        try:
                            pycountry.countries.lookup(row[0][0])
                            country.append(row[0][0])
                        except LookupError:
                            extra.append(row[0][0])
                    elif not isinstance(row, tuple):
                        extra.append(row[0][0])
            else:
                extra.append(line)

    ret = {}
    if len(person) > 0:
        _LOGGER.info(f"person: {set(person)}")
        ret['person'] = person
    if len(organization) > 0:
        _LOGGER.info(f"Organization: {organization}")
        ret['organization'] = organization
    if len(mail) > 0:
        _LOGGER.info(f"Mail: {mail}")
        ret['mail'] = mail
    if len(phone) > 0:
        _LOGGER.info(f"Phone: {phone}")
        ret['phone'] = phone
    if len(mail) > 0:
        _LOGGER.info(f"Web: {web}")
        ret['web'] = web
    if len(mail) > 0:
        _LOGGER.info(f"Country: {country}")
        ret['country'] = country
    if len(extra) > 0:
        _LOGGER.warning("##### Extra")
        _LOGGER.warning(extra)
        _LOGGER.warning("#####")
        ret['extra'] = extra
    return ret
