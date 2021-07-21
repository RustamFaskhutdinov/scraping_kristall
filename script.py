import requests
from bs4 import BeautifulSoup
import csv


def get_list_items(url, params):
    # category = category
    request = requests.get(url, params=params)
    soup = BeautifulSoup(request.text, features='html.parser')
    a_tegs = soup.find_all('a')
    links_list = []
    for a_teg in a_tegs:
        links_list.append(f"http://kristall.by{a_teg.get('href')}")
    return links_list


def generate_desc(list_item, i, list_out, category=''):
    r = requests.get(list_item, )
    # r = requests.get(list_items[i])
    soup = BeautifulSoup(r.text, features='html.parser')

    # img
    img_local = soup.find('a', {'class': 'fancybox', 'rel': 'groupe'}).get('href')
    img = f"https://pavelkopy.by/kristall{img_local}"
    # img = f"http://kristall.by{img_local}"

    # articul
    articul = f'{img_local}'.replace('/assets/images/catalog/big/', '').replace('.jpg', '')
    # generate title
    title_h1 = f"{soup.find('h1').get_text()}".replace("\n" and "\t", '')
    title_articul = f"{soup.find('div', {'class': 'text-articul'}).get_text()}" \
        .replace("\n", '').replace('Артикул: ', '').replace('\t', '')
    title = f"{title_h1} {title_articul}"

    desc = soup.find_all('div', 'text-description')
    text_desc1 = f"<b>{desc[0].get_text().split()[0]}</b><br>" + \
                 " ".join(desc[0].get_text().split()[1:]) + "<br>"

    desc_param = desc[1].find_all('div', 'line-text')
    metal = color = insert = weight = size = code = other = None
    for line in desc_param:
        p = line.text.split()
        f = p[0]
        if 'Металл' in f:
            metal = p[1:]
        elif 'Цвет' in f:
            color = ' '.join(p[2:]).replace(', ', ',').split(',')
            while len(color) < 3:
                color.append(None)
        elif 'Вставка' in f:
            insert = ' '.join(p[1:]).replace(', ', ',').split(',')
            while len(insert) < 5:
                insert.append(None)
        elif 'Вес' in f:
            weight = ' '.join(p[1:])
        elif 'Размер' in f:
            size = f"<b>{p[0]}</b> " + " ".join(p[1:]) + '\n<br>'
        elif 'Код' in f:
            code = f"<b>{p[0]} {p[1]}</b> " + " ".join(p[2:]) + '\n<br>'
        else:
            other = f"<b>{p[0]}</b> " + " ".join(p[1:]) + '\n<br>'

        if other is not None:
            text_desc = f"{text_desc1}{size}{code}{other}"
        else:
            text_desc = f"{text_desc1}{size}{code}"
        # text_desc = text_desc1 + weight + size + code + other
    list_out.append([i, title, articul, img, metal[0], weight,
                     color[0], color[1], color[2],
                     insert[0], insert[1], insert[2], insert[3], insert[4],
                     text_desc, category
                     ])
    print(i)


def prnt_to_csv(data, filename='temp2.csv', ):
    filename = filename
    with open(filename, 'w', encoding='utf-8') as output_file:
        csv_writer = csv.writer(output_file, delimiter=',', quotechar='"')

        csv_writer.writerow(['id', "title", "articul", "photo", "Characteristics:Металл", "Characteristics:Вес",
                             "Characteristics:Цвет Металла", "Characteristics:Цвет Металла",
                             "Characteristics:Цвет Металла",
                             "Characteristics:Вставка", "Characteristics:Вставка", "Characteristics:Вставка",
                             "Characteristics:Вставка", "Characteristics:Вставка",
                             "text", "category"])

        for row in data:
            csv_writer.writerow(row)
