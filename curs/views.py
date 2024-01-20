#   Необходимо создать страницу, которая будет получать курс евро к рублю из различных источников.
#
#     1. Источники для получения курса:
#     https://www.cbr-xml-daily.ru/daily_utf8.xml
#     https://www.cbr-xml-daily.ru/daily_json.js
#     предполагается, что список может быть расширен.
#     2. Должен быть задан порядок опроса источников.
#     3. В случае, если источник недоступен, необходимо переключиться на
#        прием данных с другого источника.
#     4. Список источников может быть расширен в будущем.
#
#    Что по вашему мнению плохо в текущей реализации и
#    как можно было бы это улучшить/отрефакторить.
#    Новый код писать не нужно, достаточно коротко описать проблемы
#    текущего кода и способы их решения.
#
#    Важно продемонстрировать понимание и возможность применения принципов ООП.

import json
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError

from django.http import HttpResponse

istocniki = [
    "https://www.cbr-xml-daily.ru/daily_json.js",
    "https://www.cbr-xml-daily.ru/daily_utf8.xml",
]


def cursValut(request):
    curs = ""
    for i in istocniki:
        try:
            r = urllib.request.urlopen(i)
        except urllib.error.HTTPError:
            continue
        except urllib.error.URLError:
            continue
        else:
            c = r.read()
            try:
                c = json.loads(c)
                curs = c["Valute"]["EUR"]["Value"]
                break
            except json.decoder.JSONDecodeError:
                try:
                    root = ET.fromstring(c.decode("utf-8"))
                    for r in root.iter("Valute"):
                        if r.find("CharCode").text == "EUR":
                            curs = r.find("Value").text
                            break
                except ParseError:
                    continue
    return HttpResponse("RATE: " + str(curs))
