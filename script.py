import re
import shutil
from pathlib import Path
from typing import Set

import requests
from git import Repo

# 配置与路径
CURRENT_DIR = Path(__file__).parent.resolve()
DOCS_DIR = CURRENT_DIR / 'docs'
VALID_CARD_URLS_FILE = CURRENT_DIR / 'valid_card_urls.txt'
HTTPS_PROXY = {'https': 'http://127.0.0.1:7890'}

# 全局状态
ALL_CARD_URLS: Set[str] = set()
VALID_CARD_URLS: Set[str] = set()

if VALID_CARD_URLS_FILE.exists():
    VALID_CARD_URLS = set(VALID_CARD_URLS_FILE.read_text(encoding='utf8').split())

# 映射配置
NEED_REPLACED_NAMES = {
    '「E·HERO': '「元素英雄', '「D-HERO': '「命运英雄', '「C·HERO': '「对极英雄',
    '「M·HERO': '「假面英雄', '「HERO': '「英雄', '「EM': '「娱乐伙伴',
    '「Em': '「娱乐法师', '「HSR': '「高速疾行机人', '「SR': '「疾行机人',
    '「CNo.': '「混沌No.', '「SNo.': '「闪光No.', '「ZS': '「异热同心从者',
    '「ZW': '「异热同心武器', '「DZW': '「暗黑异热同心武器', '「CX': '「混沌超量',
    '「RUM': '「升阶魔法', '「A·O·J': '「正义盟军', '「ABF': '「强袭黑羽',
    '「BF': '「黑羽', '「WW': '「风魔女', '「U.A.': '「超级运动员',
    '「V·HERO': '「幻影英雄', '「Kozmo': '「星际仙踪', '「C·': '「茧状体·',
    '「Sin': '「罪', '「SPYRAL GEAR': '「秘旋谍装备', '「SPYRAL MISSION': '「秘旋谍任务',
    '「SPYRAL': '「秘旋谍', '「S-Force': '「治安战警队', '「D·D·R」': '「异次元复活」',
    '「N·': '「新空间侠·', '「RR': '「急袭猛禽', '「LL': '「抒情歌鸲',
    '「H·C': '「英豪挑战者', '「P.U.N.K.': '「朋克', '「Evil★Twin’s': '「邪恶★双子克星',
    '「Evil★Twins': '「邪恶★双子星', '「Live☆Twin': '「直播☆双子', '「Evil★Twin': '「邪恶★双子',
}

FIX_NAMES = {'「`魔法卡「`灵魂交错`_」`_」': '「`魔法卡「灵魂交错」`_」'}

NOT_CARD_NAMES = {
    '攻击力', '守备力', '等级', '原本攻击力', '原本守备力', '攻击力·守备力',
    '原本攻击力·守备力', '○○', '...', 'トリックスター・キャンディナ',
    'トリックスター・ライトステージ', '悪夢の拷問部屋', '永续效果', '诱发即时效果',
    '増殖するG', 'メタバース', '罪 サイバー・エンド・ドラゴン', 'E', 'T', 'A', 'H',
    '作为对象的1只怪兽破坏', 'カウンター罠を発動した時', '卡名',
    'カードの発動を無効にした時', '二重怪兽',
}

SERIES_NAMES = {'隆隆隆', '刷拉拉', '我我我', '怒怒怒', 'ゴゴゴ'}
SERIES_SUFFIXES = (
    '怪兽', '魔法', '陷阱', '卡', '通常怪兽', '调整', '效果怪兽', '连接怪兽',
    'S怪兽', 'X怪兽', 'P怪兽', '融合怪兽', '仪式怪兽', '速攻魔法', '装备魔法',
    '永续魔法', '永续陷阱', '通常魔法', '通常陷阱', '反击陷阱'
)

def replace_en_name(texts: str) -> str:
    texts = texts.replace('\n\n\n', '\n\n')
    for old, new in NEED_REPLACED_NAMES.items():
        texts = texts.replace(old, new)
    return texts

def add_jp_locale_in_db_url(texts: str) -> str:
    def replacer(match):
        url = match.group(1)
        if url.startswith('https://www.db.yugioh-card.com/yugiohdb') and '&request_locale=ja' not in url:
            return f'<{url}&request_locale=ja>'
        return f'<{url}>'
    return re.sub(r'<(.*?)>', replacer, texts)

def add_cdb_url(texts: str) -> str:
    def need_skip(line: str) -> bool:
        if any(x in line for x in (':strike:', r'\ *', '**')) or line.startswith('.. _`'):
            if '*' in line and '「`' in line:
                names = re.findall(r'(?<=「)[^」]*[^「]*(?=」)', line)
                return all(f'.. _`{n.strip("_`")}' in texts for n in names)
            return True
        return False

    cards_name, series_name = [], []
    for line in texts.split('\n'):
        if need_skip(line): continue
        stack, name_chars = [], []
        bracket_depth = 0
        for i, char in enumerate(line):
            if char == '『': bracket_depth += 1
            elif char == '』': bracket_depth -= 1
            
            if char == '「': stack.append(char)
            if stack: name_chars.append(char)
            if char == '」':
                if stack: stack.pop()
                if not stack:
                    if bracket_depth > 0:
                        name_chars = []
                        continue
                    
                    full_name = ''.join(name_chars)
                    clean_name = full_name.strip('「`_」')
                    
                    is_card = True
                    if clean_name in NOT_CARD_NAMES or '○○' in full_name:
                        is_card = False
                    
                    is_series = False
                    if any(line[i+1:].startswith(s) for s in SERIES_SUFFIXES) and not line[i+1:].startswith('卡的发动'):
                        is_series = True
                    elif clean_name in SERIES_NAMES:
                        is_series = True
                    elif '衍生物' in full_name and '○○' not in full_name:
                        is_series = True
                    
                    if is_series:
                        series_name.append(full_name)
                        is_card = False
                    
                    if is_card:
                        cards_name.append(full_name)
                    
                    name_chars = []

    def to_dict(names):
        return {n: f"「`{n[1:-1].strip('`_')}`_」" for n in names}

    cards_dict, series_dict = to_dict(cards_name), to_dict(series_name)
    existing_urls = set(re.findall(r'.. _`(.*?)`: ', texts))
    tail_links = set()

    lines = []
    for line in texts.strip().split('\n'):
        if not need_skip(line):
            for old, new in cards_dict.items(): line = line.replace(old, new)
            for err, cor in FIX_NAMES.items(): line = line.replace(err, cor)
        lines.append(line)
    new_texts = '\n'.join(lines) + '\n'

    for name_raw in cards_dict:
        name = name_raw[1:-1].strip('`_')
        if name not in existing_urls:
            url = f'https://ygocdb.com/card/name/{name.replace(" ", "%20").replace("/", "%2F")}'
            tail_links.add(f'.. _`{name}`: {url}')

    for name_raw in series_dict:
        name = name_raw[1:-1].strip('`_')
        url = f'https://ygocdb.com/?search={name}'
        if name not in existing_urls:
            tail_links.add(f'.. _`{name}`: {url}')
        else:
            new_texts = new_texts.replace(f'「{name}」', f'「`{name}`_」')
            old_pattern = f'.. _`{name}`: https://ygocdb.com/card/name/{name}'
            new_texts = new_texts.replace(old_pattern, f'.. _`{name}`: {url}')

    if tail_links:
        new_texts += '\n'.join(sorted(tail_links)) + '\n'
    return new_texts

def check_card_urls(card_urls: Set[str]) -> None:
    updated = False
    for i, url in enumerate(sorted(card_urls), 1):
        if url in VALID_CARD_URLS: continue
        try:
            r = requests.get(url, proxies=HTTPS_PROXY, timeout=10)
            if '没有找到对应卡片' not in r.text:
                VALID_CARD_URLS.add(url)
                updated = True
            if i % 10 == 0 and updated:
                VALID_CARD_URLS_FILE.write_text('\n'.join(sorted(VALID_CARD_URLS)), encoding='utf8')
        except Exception as e:
            print(f"Error checking {url}: {e}")
    if updated:
        VALID_CARD_URLS_FILE.write_text('\n'.join(sorted(VALID_CARD_URLS)), encoding='utf8')

def strike_completion(texts: str) -> str:
    lines = []
    for line in texts.split('\n'):
        if '| :strike:' in line:
            if '「`' in line:
                line = line.split(r'\ `')[0].replace('「`', '「').replace('`_」', '」').strip('`')
            else:
                line = line.strip('`')
            if r'。\ `' in line:
                line = r'。\ `'.join(line.split(r'。\ `')[:-1]) + '。'
            line = line.replace(r'\ :ref:`', '').replace(r'`\ 。', '。')
            if r'`\ ' not in line and '[#]' not in line:
                line = f'{line}`'
        lines.append(line)
    return '\n'.join(lines).strip() + '\n'

def process_one_file(file: Path, branch: str) -> None:
    old_content = file.read_text(encoding='utf8')
    content = replace_en_name(old_content)
    content = add_cdb_url(content)
    content = add_jp_locale_in_db_url(content)
    
    if branch == 'dev':
        content = strike_completion(content)
    else:
        content = '\n'.join(l for l in content.split('\n') if '| :strike:' not in l).strip() + '\n'
    
    for name in NOT_CARD_NAMES:
        content = content.replace(f'「`{name}`_」', f'「{name}」')
    
    for url in re.findall(r': (https://ygocdb.com/card/name/.*)', content):
        ALL_CARD_URLS.add(url)
        
    if content != old_content:
        file.write_text(content, encoding='utf8', newline='\n')

def process_all(branch: str = 'dev') -> None:
    for file in DOCS_DIR.rglob('*.rst'):
        process_one_file(file, branch)

def git_operations(commit_message: str) -> None:
    repo = Repo(CURRENT_DIR)
    repo.git.checkout('dev')
    if repo.is_dirty():
        repo.git.add('.')
        repo.index.commit(commit_message)
        repo.git.push()

    for target, msg, is_main in [('valid', 'rm invalid faq', False), ('main', 'rm faq', True)]:
        if target in repo.branches: repo.delete_head(target, force=True)
        repo.git.checkout('-b', target)
        if is_main:
            for p in ['docs/c06', 'docs/c07']: shutil.rmtree(DOCS_DIR / p.split('/')[-1], ignore_errors=True)
            for f in ['docs/chapters/p06_ocg_rule_faq.rst', 'docs/chapters/p07_ocg_deck_course.rst']:
                (CURRENT_DIR / f).unlink(missing_ok=True)
        else:
            process_all(target)
        
        if repo.is_dirty():
            repo.git.add('.')
            repo.index.commit(msg)
            repo.git.push('--set-upstream', 'origin', target, '-f')
    repo.git.checkout('dev')

def main(commit_message: str = 'add faq') -> None:
    process_all('dev')
    check_card_urls(ALL_CARD_URLS)
    git_operations(commit_message)

if __name__ == '__main__':
    main()
