import os
import re

docs_path = os.path.join(os.getcwd(), 'docs')

names = {
    '「E·HERO': '「元素英雄',
    '「D-HERO': '「命运英雄',
    '「C·HERO': '「对极英雄',
    '「M·HERO': '「假面英雄',
    '「HERO': '「英雄',
    '「EM': '「娱乐伙伴',
    '「Em': '「娱乐法师',
    '「HSR': '「高速疾行机人',
    '「SR': '「疾行机人',
    '「CNo.': '「混沌No.',
    '「SNo.': '「闪光No.',
    '「ZS': '「异热同心从者',
    '「ZW': '「异热同心武器',
    '「DZW': '「暗黑异热同心武器',
    '「CX': '「混沌超量',
    '「RUM': '「升阶魔法',
    '「SR': '「疾行机人',
    '「A·O·J': '「正义盟军',
    '「ABF': '「强袭黑羽',
    '「BF': '「黑羽',
    '「WW': '「风魔女',
    '「U.A.': '「超级运动员',
    '「V·HERO': '「幻影英雄',
    '「Kozmo': '「星际仙踪',
    '「C·': '「茧状体·',
    '「Sin': '「罪',
    '「SPYRAL GEAR': '「秘旋谍装备',
    '「SPYRAL MISSION': '「秘旋谍任务',
    '「SPYRAL': '「秘旋谍',
    '「S-Force': '「治安战警队',
    '「D·D·R」': '「异次元复活」',
    '「TG': '「科技属',
    '「N·': '「新空间侠·',
    '「RR': '「急袭猛禽',
    '「LL': '「抒情歌鸲',
    '「H·C': '「英豪挑战者',
    '「P.U.N.K.': '「朋克'
}

not_card_names = (
    '攻击力·守备力',
    '原本攻击力·守备力'
    '...',
    'トリックスター・キャンディナ',
    'トリックスター・ライトステージ',
    '悪夢の拷問部屋',
    '永续效果',
    '诱发即时效果',
    '増殖するG'
)


def replace_en_name(texts: str) -> str:
    texts = texts.replace('\n\n\n', '\n\n')
    for key, value in names.items():
        texts = texts.replace(key, value)
    return texts


def add_jp_locale_in_db_url(texts: str) -> str:
    jp_locale = '&request_locale=ja'
    urls = re.findall('<(.*?)>', texts)
    new_urls = {}
    for url in urls:
        if url.startswith('https://www.db.yugioh-card.com/yugiohdb') and jp_locale not in url:
            new_urls[url] = f'{url}{jp_locale}'
    for url, new_url in new_urls.items():
        texts = texts.replace(url, new_url)
    return texts


def add_cdb_link(texts: str) -> str:

    def need_skip(line: str) -> bool:
        if ':strike:' in line or '\ *' in line or line.startswith('.. _`'):
            return True
        return False

    stack = []
    card_names, card_name = [], []
    for line in texts.split('\n'):
        line = f'{line}\n'
        if need_skip(line):
            continue
        for char in line:
            if char == '「':
                stack.append(char)
            if stack:
                card_name.append(char)
            if char == '」':
                stack.pop()
                if not stack:
                    name = ''.join(card_name)
                    is_card = True
                    for not_card_name in not_card_names:
                        if not_card_name in name:
                            is_card = False
                            break
                    if is_card and not name.endswith('_」'):
                        card_names.append(name)
                    card_name = []
    tail_texts = set()
    names = {}
    for card_name in set(card_names):
        name = ' '.join(card_name[1:-1].strip().split())
        new_name = f'「`{name}`_」'
        names[card_name] = new_name
        tail_texts.add(f'.. _`{name}`: https://ygocdb.com/?search={name.replace(" ", "+")}\n')
    if not names:
        return texts
    new_texts = []
    part_texts = []
    for line in texts.split('\n'):
        line = f'{line}\n'
        if need_skip(line):
            part_texts = ''.join(part_texts)
            for old, new in names.items():
                part_texts = part_texts.replace(old, new)
            new_texts.append(part_texts)
            new_texts.append(line)
            part_texts = []
            continue
        else:
            part_texts.append(line)
    if part_texts:
        part_texts = ''.join(part_texts)
        for old, new in names.items():
            part_texts = part_texts.replace(old, new)
        new_texts.append(part_texts)

    results = ''.join(new_texts)
    if tail_texts:
        results += ''.join(list(tail_texts))
    return results


def do_one(filepath: str) -> None:
    with open(filepath, 'r', encoding='utf8') as f:
        try:
            texts = ''.join(f.readlines())
        except:
            print(filepath, 'read exception')
            return None
        texts = replace_en_name(texts)
        texts = add_cdb_link(texts)
        texts = add_jp_locale_in_db_url(texts)
    with open(filepath, 'w', encoding='utf8') as f:
        f.write(texts)


def do_all() -> None:
    for filename in os.listdir(docs_path):
        filepath = os.path.join(docs_path, filename)
        if os.path.isdir(filepath):
            for rst_file in os.listdir(filepath):
                rst_path = os.path.join(filepath, rst_file)
                if not rst_path.endswith('.rst'):
                    continue
                do_one(rst_path)
        if os.path.isfile(filepath) and filepath.endswith('.rst'):
            do_one(filepath)


if __name__ == '__main__':
    do_all()
