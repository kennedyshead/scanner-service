import logging

import coloredlogs
from pyisemail import is_email
from transcribe.image import OCR, Path

from matcher import is_phone_number, phone_number, is_webbadress, \
    is_postal_adress, is_person

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
    mail = []
    phone = []
    web = []
    address = []
    no_match = []

    for line in data.unformatted.split("\n"):
        if is_email(line):
            mail.append(line)
        elif is_phone_number(line):
            res = phone_number.findall(line)
            if len(res) > 0:
                phone.append(res[0])
        elif is_webbadress(line):
            web.append(line)
        elif is_postal_adress(line):
            address.append(line)
        elif is_person(line):
            person.append(line)
        else:
            no_match.append(line)
    if len(person) > 0:
        _LOGGER.info(f"person: {person}")
    if len(mail) > 0:
        _LOGGER.info(f"Mail: {mail}")
    if len(phone) > 0:
        _LOGGER.info(f"Phone: {phone}")
    if len(mail) > 0:
        _LOGGER.info(f"Web: {web}")
    if len(address) > 0:
        _LOGGER.info(f"Adress: {address}")
    if len(no_match) > 0:
        _LOGGER.warning("##### NO MATCH")
        _LOGGER.warning(no_match)
        _LOGGER.warning("#####")
