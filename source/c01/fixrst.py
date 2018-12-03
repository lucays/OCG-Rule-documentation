import subprocess
import os


def addblankline(filename):
    # addblankline(filename)
    with open(filename, 'r', encoding='utf8') as f:
        contents = list(f)
        length = len(contents)
        results = []
        for index, text in enumerate(contents):
            if text == '\n' and index + 1 < length:
                if (contents[index+1].startswith('| ') or contents[index+1].startswith('- ') or contents[index+1].strip().startswith('1.')) and contents[index-1].startswith('| '):
                    results.append('|\n')
                elif not contents[index+1].strip('- ').startswith('| ') and not contents[index-1].strip('- ').startswith('| '):
                    results.append(text)
                elif not (contents[index+1].startswith('| ') or contents[index+1].startswith('- ')) and (contents[index+1].strip().startswith('- ') or contents[index+1].strip().startswith('1.')) and not contents[index+1].strip('- ').startswith('| '):
                    # results[-1] = '| ' + results[-1]
                    results.append('|\n')
                elif contents[index-1].strip('- ').startswith('| ') and contents[index+1].strip('- ').startswith('| '):
                    if contents[index+1].startswith('| ') and not contents[index-1].startswith('| '):
                        results.append(text)
                    else:
                        blank_counts = contents[index-1].index('| ')
                        results.append(f'{" "*blank_counts}|\n')
                else:
                    results.append(text)
            else:
                results.append(text)
    with open(filename, 'w', encoding='utf8') as f:
        f.write(''.join(results))


'''
p = subprocess.run(['ls'], stdout=subprocess.PIPE, encoding='utf8')
for filename in p.stdout.split():
    if '.rst' in filename:
        addblankline(filename)
'''
p = os.popen('dir')
files = [i.split()[-1].strip() for i in p if i.startswith('2018') and '.rst' in i]
for file in files:
    addblankline(file)
