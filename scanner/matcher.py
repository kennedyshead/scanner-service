from http.client import InvalidURL
import re

import phonenumbers
from phonenumbers import NumberParseException
from urllib.request import urlopen
import probablepeople as pp
from postal_address import Address

SWE = (
    "0981", "0980", "0978", "0977", "0976", "0975", "0973", "0971", "0970",
    "0961",
    "0960", "0954",
    "0953", "0952", "0951", "0950", "0943", "0942", "0941", "0940", "0935",
    "0934",
    "0933", "0932",
    "0930", "0929", "0928", "0927", "0926", "0925", "0924", "0923", "0922",
    "0921",
    "0920", "0918",
    "0916", "0915", "0914", "0913", "0912", "0911", "0910", "070", "072",
    "073",
    "075", "076", "077", "078", "079", "0696", "0695", "0693", "0692", "0691",
    "0690", "0687", "0684", "0682", "0680", "0672", "0671", "0670", "0663",
    "0662",
    "0661", "0660",
    "0657", "0653", "0652", "0651", "0650", "0647", "0645", "0644", "0643",
    "0642",
    "0640", "0624",
    "0623", "0622", "0621", "0620", "0613", "0612", "0611", "0591", "0590",
    "0589",
    "0587", "0586",
    "0585", "0584", "0583", "0582", "0581", "0580", "0573", "0571", "0570",
    "0565",
    "0564", "0563",
    "0560", "0555", "0554", "0553", "0552", "0551", "0550", "0534", "0533",
    "0532",
    "0531", "0530",
    "0528", "0526", "0525", "0524", "0523", "0522", "0521", "0520", "0515",
    "0514",
    "0513", "0512",
    "0511", "0510", "0506", "0505", "0504", "0503", "0502", "0501", "0500",
    "0499",
    "0498", "0496",
    "0495", "0494", "0493", "0492", "0491", "0490", "0486", "0485", "0481",
    "0480",
    "0479", "0478",
    "0477", "0476", "0474", "0472", "0471", "0470", "0459", "0457", "0456",
    "0455",
    "0454", "0451",
    "0435", "0433", "0431", "0430", "0418", "0417", "0416", "0415", "0414",
    "0413",
    "0411", "0410",
    "0393", "0392", "0390", "0383", "0382", "0381", "0380", "0372", "0371",
    "0370",
    "0346", "0345",
    "0340", "0325", "0322", "0321", "0320", "0304", "0303", "0302", "0301",
    "0300",
    "0297", "0295",
    "0294", "0293", "0292", "0291", "0290", "0281", "0280", "0278", "0271",
    "0270",
    "0258", "0253",
    "0251", "0250", "0248", "0247", "0246", "0243", "0241", "0240", "0227",
    "0226",
    "0225", "0224",
    "0223", "0222", "0221", "0220", "0176", "0175", "0174", "0173", "0171",
    "0159",
    "0158", "0157",
    "0156", "0155", "0152", "0151", "0150", "0144", "0143", "0142", "0141",
    "0140",
    "0125", "0123",
    "0122", "0121", "0120", "090", "063", "060", "054", "046", "044", "042",
    "040",
    "036", "035", "033",
    "031", "026", "023", "021", "020", "0200", "019", "018", "016", "013",
    "011",
    "010", "08"
)

phone_number = re.compile(r"[\d\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]")


def is_phone_number(text, retest=True):
    try:
        pn = phone_number.findall(text)
    except TypeError:
        return False
    for line in pn:
        try:
            phonenumbers.parse(line, phonenumbers.UNKNOWN_REGION)
            return True
        except NumberParseException:
            pass

        if line.startswith(SWE):
            return True


def is_webbadress(url):
    if url.startswith("www."):
        return True
    try:
        if not url.startswith("http"):
            url = f"http://{url}"
        urlopen(url)
        return True
    except (IOError, ValueError, InvalidURL):
        return False


def is_postal_adress(text):
    if Address(text).validate():
        return True
    return False


def is_person(text):
    try:
        if pp.parse(text)[0][1] in ["GivenName", "surname"]:
            return True
    except IndexError:
        return False
