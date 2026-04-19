import re
import shutil
from pathlib import Path
from typing import Set, Dict

import requests
from git import Repo

# 配置与路径
CURRENT_DIR = Path(__file__).parent.resolve()
DOCS_DIR = CURRENT_DIR / 'docs'
LINKS_FILE = DOCS_DIR / 'links.rst'
HTTPS_PROXY = {'https': 'http://127.0.0.1:7890'}

# 全局状态
GLOBAL_LINKS: Dict[str, str] = {}  # 汇总所有文件的链接定义 {name: url}

# 初始化时从现有文件加载已有链接，防止丢失
if LINKS_FILE.exists():
    link_pattern = re.compile(r'^\.\. _`(.+?)`: (.+)$')
    for line in LINKS_FILE.read_text(encoding='utf8').splitlines():
        match = link_pattern.match(line)
        if match:
            GLOBAL_LINKS[match.group(1)] = match.group(2)

# 映射配置与原始代码一致
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
    '永续魔法', '场地魔法', '永续陷阱', '通常魔法', '通常陷阱', '反击陷阱'
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
        if any(x in line for x in (':strike:',)) or line.startswith('.. _`'):
            return True
        return False

    cards_name, series_name = [], []

    for line in texts.split('\n'):
        if need_skip(line):
            continue

        stack = []
        name_chars = []
        bracket_depth = 0  # 处理 『』 嵌套

        for i, char in enumerate(line):
            if char == '『':
                bracket_depth += 1
            elif char == '』':
                bracket_depth -= 1

            if char == '「':
                stack.append(i)

            if stack:
                name_chars.append(char)

            if char == '」':
                if stack:
                    stack.pop()
                    if not stack:  # 最外层括号闭合
                        if bracket_depth > 0:
                            name_chars = []
                            continue

                        full_content = ''.join(name_chars)
                        name_chars = []

                        # 仅移除最外层的一对 「 」
                        if full_content.startswith('「') and full_content.endswith('」'):
                            inner_content = full_content[1:-1]
                        else:
                            inner_content = full_content

                        clean_name = inner_content.strip('`_')
                        if not clean_name or clean_name in NOT_CARD_NAMES or '○○' in clean_name:
                            continue

                        is_series = False
                        after_text = line[i+1:]
                        if any(after_text.startswith(s) for s in SERIES_SUFFIXES) and not after_text.startswith('卡的发动'):
                            is_series = True
                        elif clean_name in SERIES_NAMES:
                            is_series = True
                        elif '衍生物' in clean_name and '○○' not in clean_name:
                            is_series = True

                        if is_series:
                            series_name.append(clean_name)
                        else:
                            cards_name.append(clean_name)

    # 汇总已有链接并清理正文末尾（旧脚本留下的定义行）
    existing_defs = re.findall(r'.. _`(.*?)`: (http.*)', texts)
    for name, url in existing_defs:
        GLOBAL_LINKS[name] = url

    replace_map = {}
    for name in cards_name:
        replace_map[f'「{name}」'] = f'「`{name}`_」'
        replace_map[f'「`{name}`」'] = f'「`{name}`_」'

    for name in series_name:
        replace_map[f'「{name}」'] = f'「`{name}`_」'
        replace_map[f'「`{name}`」'] = f'「`{name}`_」'

    lines = []
    for line in texts.strip().split('\n'):
        if line.startswith('.. _`'):
            continue
        if not need_skip(line):
            for old, new in replace_map.items():
                line = line.replace(old, new)
            for err, cor in FIX_NAMES.items():
                line = line.replace(err, cor)
        lines.append(line)
    new_texts = '\n'.join(lines).strip() + '\n'

    for name in cards_name:
        if name not in GLOBAL_LINKS:
            url = f'https://ygocdb.com/card/name/{name.replace(" ", "%20").replace("/", "%2F")}'
            GLOBAL_LINKS[name] = url

    for name in series_name:
        if name not in GLOBAL_LINKS or '/card/name/' in GLOBAL_LINKS[name]:
            url = f'https://ygocdb.com/?search={name}'
            GLOBAL_LINKS[name] = url

    return new_texts


def write_global_links() -> None:
    """将所有收集到的链接写入唯一的汇总文件"""
    content = []
    for name in sorted(GLOBAL_LINKS.keys()):
        url = GLOBAL_LINKS[name]
        content.append(f'.. _`{name}`: {url}')
    LINKS_FILE.write_text('\n'.join(content) + '\n', encoding='utf8')
    print(f"已更新汇总链接文件: {LINKS_FILE}")


def strike_completion(texts: str) -> str:
    lines = []
    for line in texts.split('\n'):
        if '| :strike:' in line:
            if '「`' in line:
                line = line.split(r'\ `')[0].replace(
                    '「`', '「').replace('`_」', '」').strip('`')
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
        content = '\n'.join(l for l in content.split(
            '\n') if '| :strike:' not in l).strip() + '\n'

    for name in NOT_CARD_NAMES:
        content = content.replace(f'「`{name}`_」', f'「{name}」')

    if content != old_content:
        file.write_text(content, encoding='utf8', newline='\n')


def process_all(branch: str = 'dev') -> None:
    for file in DOCS_DIR.rglob('*.rst'):
        if file.name == 'links.rst':
            continue
        process_one_file(file, branch)


def git_operations(commit_message: str) -> None:
    repo = Repo(CURRENT_DIR)
    repo.git.checkout('dev')
    if repo.is_dirty():
        repo.git.add('.')
        repo.index.commit(commit_message)
        repo.git.push()

    for target, msg, is_main in [('valid', 'rm invalid faq', False), ('main', 'rm faq', True)]:
        if target in repo.branches:
            repo.delete_head(target, force=True)
        repo.git.checkout('-b', target)
        if is_main:
            for p in ['docs/c06', 'docs/c07']:
                shutil.rmtree(DOCS_DIR / p.split('/')[-1], ignore_errors=True)
            for f in ['docs/chapters/p06_ocg_rule_faq.rst', 'docs/chapters/p07_ocg_deck_course.rst']:
                (CURRENT_DIR / f).unlink(missing_ok=True)
        else:
            process_all(target)
            write_global_links()

        if repo.is_dirty():
            repo.git.add('.')
            repo.index.commit(msg)
            repo.git.push('--set-upstream', 'origin', target, '-f')
    repo.git.checkout('dev')


def main(commit_message: str) -> None:
    process_all('dev')
    write_global_links()
    git_operations(commit_message)


if __name__ == '__main__':
    import sys
    msg = sys.argv[1] if len(sys.argv) > 1 else 'add faq'
    main(msg)
