
import re
from pathlib import Path

import requests
from git import Repo

current_dir = Path(__file__).parent.resolve()

HTTPS_PROXY = 'http://127.0.0.1:7890'

VALID_CARD_URLS_LST = []
ALL_CARD_URLS, NEW_CARD_URLS, VALID_CARD_URLS = set(), set(), set()
VALID_CARD_URLS_FILE = current_dir / 'valid_card_urls.txt'
if VALID_CARD_URLS_FILE.exists():
    VALID_CARD_URLS_LST = VALID_CARD_URLS_FILE.read_text(encoding='utf8').split()
    VALID_CARD_URLS = set(VALID_CARD_URLS_LST)

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

FIX_NAMES = {
    '「`魔法卡「`灵魂交错`_」`_」': '「`魔法卡「灵魂交错」`_」'
}

NOT_CARD_NAMES = {
    '攻击力',
    '守备力',
    '等级',
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
    'メタバース',
    '罪 サイバー・エンド・ドラゴン',
    'E', 'T', 'A', 'H',
    '作为对象的1只怪兽破坏',
    'カウンター罠を発動した時',
    '卡名',
    'カウンター罠を発動した時',
    'カードの発動を無効にした時',
    '二重怪兽',
}

SERIES_NAMES = (
    '隆隆隆',
    '刷拉拉',
    '我我我',
    '怒怒怒',
    'ゴゴゴ',
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
        if ':strike:' in line or r'\ *' in line or '**' in line or line.startswith('.. _`'):

            if '*' in line and '「`' in line:
                for i in re.findall('(?<=「)[^」]*[^「]*(?=」)', line):
                    i = i.strip('_`')
                    if f'.. _`{i}' not in texts:
                        return False
            return True
        return False

    def get_names_dict(names: list) -> dict:
        names_dict = {}
        for name in names:
            name = name[1:-1].strip('`_')
            names_dict[f'「{name}」'] = f'「`{name}`_」'
        return names_dict

    stack = []
    cards_name, series_name, name_chars = [], [], []
    for line in texts.split('\n'):
        if need_skip(line):
            continue
        # regex (?<=「)[^」]*[^「]*(?=」)
        for index, char in enumerate(line):
            if char == '「':
                stack.append(char)
            if stack:
                name_chars.append(char)
            if char == '」':
                stack.pop()
                if not stack:
                    name = ''.join(name_chars)
                    is_card = True
                    if name.strip('「`_」') in NOT_CARD_NAMES:
                        is_card = False
                    if '○○' in name:
                        is_card = False
                    for serie in (
                        '怪兽', '魔法', '陷阱', '卡',
                        '通常怪兽', '调整', '效果怪兽', '连接怪兽', 'S怪兽', 'X怪兽', 'P怪兽', '融合怪兽', '仪式怪兽',
                        '速攻魔法', '装备魔法', '永续魔法', '永续陷阱', '通常魔法', '通常陷阱', '反击陷阱'
                    ):
                        if line[index+1:].startswith(serie) and not line[index+1:].startswith('卡的发动'):
                            series_name.append(name)
                            is_card = False
                            break
                    for serie in SERIES_NAMES:
                        if name.strip('「`_」') == serie:
                            series_name.append(name)
                            is_card = False
                            break
                    if '衍生物' in name and '○○' not in name:
                        series_name.append(name)
                        is_card = False
                    if is_card:
                        cards_name.append(name)
                    name_chars = []

    cards_name_dict = get_names_dict(cards_name)
    series_name_dict = get_names_dict(series_name)

    have_url_card_names = set(re.findall('.. _`(.*?)`: ', texts))
    tail_texts = set()

    new_texts = []
    for line in texts.strip().split('\n'):
        if need_skip(line):
            new_texts.append(line)
            continue
        for old, new in cards_name_dict.items():
            line = line.replace(old, new)
        for error, correct in FIX_NAMES.items():
            line = line.replace(error, correct)
        new_texts.append(line)
    new_texts = '\n'.join(new_texts)

    for card_name in cards_name_dict:
        card_name = card_name[1:-1].strip('`_')
        if card_name not in have_url_card_names:
            new_card_url = f'https://ygocdb.com/card/name/{card_name.replace(" ", "%20").replace("/", "%2F")}'
            tail_texts.add(f'.. _`{card_name}`: {new_card_url}')
            NEW_CARD_URLS.add(new_card_url)
    for serie_name in series_name_dict:
        serie_name = serie_name[1:-1].strip('`_')
        new_serie_url = f'https://ygocdb.com/?search={serie_name}'
        if serie_name not in have_url_card_names:
            tail_texts.add(f'.. _`{serie_name}`: {new_serie_url}')
        else:
            new_texts = new_texts.replace(f'「{serie_name}」', f'「`{serie_name}`_」')
            new_texts = new_texts.replace(f'.. _`{serie_name}`: https://ygocdb.com/card/name/{serie_name}', f'.. _`{serie_name}`: {new_serie_url}')

    new_texts += '\n'
    if tail_texts:
        new_texts += '\n'.join(tail_texts)
        new_texts += '\n'
    return new_texts


def exract_card_urls(texts: str):
    card_urls = re.findall(': (https://ygocdb.com/card/name/.*)', texts)
    for card_url in card_urls:
        ALL_CARD_URLS.add(card_url)


def check_card_urls(card_urls: list[str]) -> None:
    c = 0
    for card_url in card_urls:
        if card_url in VALID_CARD_URLS:
            continue
        try:
            r = requests.get(card_url, proxies={'https': HTTPS_PROXY})
            if '没有找到对应卡片' in r.text:
                print(card_url, 'ERROR: no card!')
            else:
                VALID_CARD_URLS.add(card_url)
            c += 1
            if c % 10 == 0:
                VALID_CARD_URLS_FILE.write_text('\n'.join(VALID_CARD_URLS), encoding='utf8')
        except Exception as e:
            print(card_url, e)
    old_valid_card_urls = set(VALID_CARD_URLS_LST)
    for valid_card_url in VALID_CARD_URLS:
        if valid_card_url not in old_valid_card_urls:
            VALID_CARD_URLS_LST.append(valid_card_url)
    VALID_CARD_URLS_FILE.write_text('\n'.join(VALID_CARD_URLS_LST), encoding='utf8')


def strike_completion(texts: str) -> str:
    new_texts = []
    for line in texts.split('\n'):
        if '| :strike:' in line:
            if '「`' in line:
                line = line.split(r'\ `')[0]
                line = line.replace('「`', '「').replace('`_」', '」').strip('`')
            else:
                line = line.strip('`')
            if r'。\ `' in line:
                datas = line.split(r'。\ `')
                line = r'。\ `'.join(datas[:-1]) + '。'
            line = line.replace(r'\ :ref:`', '').replace(r'`\ 。', '。')
            if r'`\ ' not in line and '[#]' not in line:
                line = f'{line}`'
        new_texts.append(line)
    return '\n'.join(new_texts).strip() + '\n'


def remove_strike_completion(texts: str) -> str:
    new_texts = []
    for line in texts.split('\n'):
        if '| :strike:' in line:
            continue
        new_texts.append(line)
    return '\n'.join(new_texts).strip() + '\n'


def replace_not_card(texts: str) -> str:
    for not_card_name in NOT_CARD_NAMES:
        texts = texts.replace(f'「`{not_card_name}`_」', f'「{not_card_name}」')
    return texts


def process_one_file(file: Path, branch: str) -> None:
    old_texts = file.read_text(encoding='utf8')
    texts = replace_en_name(old_texts)
    texts = add_cdb_url(texts)
    texts = add_jp_locale_in_db_url(texts)
    if branch == 'dev':
        texts = strike_completion(texts)
    else:
        texts = remove_strike_completion(texts)
    texts = replace_not_card(texts)
    exract_card_urls(texts)
    if texts != old_texts:
        file.write_text(texts, encoding='utf8', newline='\n')


def process_all(branch: str = 'dev') -> None:
    docs_path = Path(__file__).parent / 'docs'
    for sub_path in docs_path.iterdir():
        if sub_path.is_file() and sub_path.name.endswith('.rst'):
            process_one_file(sub_path, branch)
        elif sub_path.is_dir():
            for file in sub_path.iterdir():
                if file.name.endswith('.rst'):
                    process_one_file(file, branch)


def delete_folder(folder_path: Path) -> None:
    if folder_path.exists() and folder_path.is_dir():
        # 递归删除文件夹中的所有文件和子文件夹
        for item in folder_path.iterdir():
            if item.is_dir():
                delete_folder(item)  # 递归删除子文件夹
            else:
                item.unlink()  # 删除文件
        folder_path.rmdir()  # 删除空文件夹
        print(f"已删除文件夹: {folder_path}")
    else:
        print(f"文件夹不存在或不是目录: {folder_path}")


def git_operations(commit_message: str) -> None:
    repo = Repo(current_dir)
    repo.git.checkout('dev')
    if repo.is_dirty():
        repo.git.add('.')
        repo.index.commit(commit_message)
        repo.git.push()

    if 'valid' in repo.branches:
        repo.delete_head('valid', force=True)
    repo.git.checkout('-b', 'valid')
    process_all('valid')
    if repo.is_dirty():
        repo.git.add('.')
        repo.index.commit('rm invalid faq')
        repo.git.push('--set-upstream', 'origin', 'valid', '-f')

    if 'main' in repo.branches:
        repo.delete_head('main', force=True)
    repo.git.checkout('-b', 'main')
    delete_folder(current_dir / 'docs/c06')
    delete_folder(current_dir / 'docs/c07')
    (current_dir / 'docs/chapters/p06_ocg_rule_faq.rst').unlink()
    (current_dir / 'docs/chapters/p07_ocg_deck_course.rst').unlink()
    if repo.is_dirty():
        repo.git.add('.')
        repo.index.commit('rm faq')
        repo.git.push('--set-upstream', 'origin', 'main', '-f')
    repo.git.checkout('dev')


def main(commit_message: str = 'add faq') -> None:
    process_all()
    check_card_urls(ALL_CARD_URLS)
    git_operations(commit_message)


if __name__ == '__main__':
    main('fix faq')
