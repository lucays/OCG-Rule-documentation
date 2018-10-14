import sys

def main():
    filename = sys.argv[1]
    resname = sys.argv[2]
    with open(filename, 'r', encoding='utf8') as f:
        datas = []
        for line in f:
            if line[:2] not in {'# ', '> ', '--', 'ti'} and line !='\n':
                datas.append(f'{line[:-1]}  \n')
            else:
                datas.append(line)

    with open(resname, 'w', encoding='utf8') as f:
        for line in datas:
            f.write(line)


if __name__ == '__main__':
    main()
