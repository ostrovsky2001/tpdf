import aiohttp_jinja2

from urllib.parse import quote
from libs.tpdf import TPdf
from aiohttp import web
import pandas as pd

class ResponseFile(web.Response):
    def __new__(cls, file_name, file_body):
        headers = {
            'Content-Type': 'application/pdf; charset="utf-8"',
            'Content-Disposition': "inline; filename*=UTF-8''{}".format(
                quote(file_name, encoding='utf-8'))
        }
        return web.Response(body=file_body, headers=headers)


@aiohttp_jinja2.template('positioning.html')
async def positioning(request):
    tpdf = TPdf()
    # дефолтные параметры
    in_data = {
        'pdf_name': 'ClearPage',
        'page_num': '1',
    }
    in_data.update(dict(request.query))
    fields = tpdf.load_fields_from_file(name=in_data['pdf_name'], to_front=True)
    in_data.update({'fields': fields})
    return in_data

df = pd.read_excel('table.xlsx')
TPdf.dump_to_json(df)

async def save_form_fields(request):
    rq = await request.json()
    return TPdf.save_fields_to_file(rq['pos'])


mime = {
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'png': 'image/png',
    'bmp': 'image/bmp',
    'gif': 'image/gif',
    'pdf': 'application/pdf',
    'xls': 'application/vnd.ms-excel',
    'xlsx': 'application/vnd.ms-excel',
    'xlsm': 'application/vnd.ms-excel',
    'doc': 'application/msword',
    'docx': 'application/msword',
    'rtf': 'application/rtf',
    'ppt': 'application/powerpoint',
    'pptx': 'application/powerpoint',
}


async def get_file(request):
    pdf_name = request.query['pdf_name']
    tpdf = TPdf()
    file = tpdf.get_pdf(pdf_name, b64='False', fill_x=True)
    return ResponseFile(pdf_name, file)


# async def example(request):
#     df = pd.read_excel('table.xlsx')

#     # набор данных для генерации комплекта документов
#     data = {
#         df.values[1][0]:df.values[1][1],
#         'last_name': 'Иванова',
#         'first_name': 'Мария',
#         'middle_name': 'Иванова',
#         'gender': 'Ж',
#         'birth_date': '01.01.2000',
#         'birth_place': 'г.Москва',
#         'registration': 'г.Москва, ул. Полковника Исаева, дом 17, кв 43',
#         '1_work': 'Радистка 3 категории, в/ч 89031',
#         '2_work': 'Радистка 1 категории, в/ч 17043',
#         '3_work': 'Командир отделения радистов, в/ч 17043 главного управления разведки комитета государственной безопасности республики Беларусь.',
#         'kafedra': 'Кафедра ИИСТ, ЛЭТИ',
#     }

#     # перечень документов в комплекте
#     complete = [
#         ('ZayavlenieNaZagranpasport', 1),
#         ('ClearPage', 1),
#         ('ZayavlenieNaZagranpasport', 1),
#     ]

#     # загружаем данные в основной класс и получаем комплект документов в pdf
#     tpdf = TPdf(**data)
#     # можно сгенерировать один файл или комплект документов
#     # file = tpdf.get_pdf('ZayavlenieNaZagranpasport ', b64='False')
#     file = tpdf.get_complete(complete, b64='False')

#     return ResponseFile('ZayavlenieNaZagranpasport.pdf', file)

async def new_name(request):
    # набор данных для генерации комплекта документов
    data = df[df.columns[:2]].set_index(df.columns[0]).T.to_dict('records')[0]

    # перечень документов в комплекте
    complete = [
        ('NewName', 1)
    ]

    # загружаем данные в основной класс и получаем комплект документов в pdf
    tpdf = TPdf(**data)
    # можно сгенерировать один файл или комплект документов
    # file = tpdf.get_pdf('ZayavlenieNaZagranpasport ', b64='False')
    file = tpdf.get_complete(complete, b64='False')

    return ResponseFile('NewName.pdf', file)
