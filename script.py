
import re
from pathlib import Path

NEED_REPLACED_NAMES = {
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
    '「P.U.N.K.': '「朋克',
    '「Evil★Twin’s': '「邪恶★双子克星',
    '「Evil★Twins': '「邪恶★双子星',
    '「Live☆Twin': '「直播☆双子',
    '「Evil★Twin': '「邪恶★双子',
}

NOT_CARD_NAMES = (
    '攻击力',
    '守备力',
    '原本攻击力',
    '原本守备力',
    '攻击力·守备力',
    '原本攻击力·守备力',
    '○○',
    '...',
    'トリックスター・キャンディナ',
    'トリックスター・ライトステージ',
    '悪夢の拷問部屋',
    '永续效果',
    '诱发即时效果',
    '増殖するG',
)


def replace_en_name(texts: str) -> str:
    texts = texts.replace('\n\n\n', '\n\n')
    for key, value in NEED_REPLACED_NAMES.items():
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


def add_cdb_url(texts: str) -> str:

    def need_skip(line: str) -> bool:
        if ':strike:' in line or '\ *' in line or line.startswith('.. _`'):
            return True
        return False

    stack = []
    card_names, card_name = [], []
    for line in texts.split('\n'):
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
                    for not_card_name in NOT_CARD_NAMES:
                        if not_card_name in name:
                            is_card = False
                            break
                    if is_card:
                        card_names.append(name)
                    card_name = []

    card_names_dict = {}
    for card_name in card_names:
        card_name = card_name[1:-1].strip('`_')
        card_names_dict[f'「{card_name}」'] = f'「`{card_name}`_」'

    have_url_card_names = set(re.findall('.. _`(.*?)`: ', texts))
    tail_texts = set()

    new_texts = []
    for line in texts.strip().split('\n'):
        if need_skip(line):
            new_texts.append(line)
            continue
        for old, new in card_names_dict.items():
            line = line.replace(old, new)
        new_texts.append(line)

    for card_name in card_names_dict:
        card_name = card_name[1:-1].strip('`_')
        if card_name not in have_url_card_names:
            tail_texts.add(f'.. _`{card_name}`: https://ygocdb.com/?search={card_name.replace(" ", "+")}')

    if not have_url_card_names and tail_texts:
        new_texts.append('\n')
    if tail_texts:
        new_texts.extend(tail_texts)
    return '\n'.join(new_texts).strip() + '\n'


def do_one(file: Path) -> None:
    old_texts = file.read_text(encoding='utf8')
    texts = replace_en_name(old_texts)
    texts = add_cdb_url(texts)
    texts = add_jp_locale_in_db_url(texts)
    if texts != old_texts:
        file.write_text(texts, encoding='utf8')


def do_all() -> None:
    docs_path = Path(__file__).parent / 'docs'
    for sub_path in docs_path.iterdir():
        if sub_path.is_file() and sub_path.name.endswith('.rst'):
            do_one(sub_path)
        elif sub_path.is_dir():
            for file in sub_path.iterdir():
                if file.name.endswith('.rst'):
                    do_one(file)


if __name__ == '__main__':
    do_all()
