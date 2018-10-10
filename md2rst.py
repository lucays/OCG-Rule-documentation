import subprocess

p = subprocess.run(['ls'], stdout=subprocess.PIPE, encoding='utf8')
for filename in p.stdout.split():
    if '.md' in filename:
        subprocess.run(['pandoc', filename, '-s', '-o', filename[:-3]+'.rst'])
