import pandas as pd
import jieba
import os
from datetime import datetime
import random


def split_train_val_test(all_files):
    random.shuffle(all_files)
    length = len(all_files)
    train = all_files[: int(length * 0.7)]
    val = all_files[int(length * 0.7): int(length * 0.9)]
    test = all_files[int(length * 0.9): ]

    return train, val, test


def save_file_list(file_name, file_list):
    with open(file_name, 'w') as writer:
        [writer.write(f+'\n') for f in file_list]


def create_hightligh_tokens(summary):
    split_tokens = '。'
    lines = summary.split(split_tokens)

    lines = [" ".join(list(jieba.cut(line))) for line in lines]

    highlight_part = "\n\n@highlight\n\n".join([' '] + lines[:-1])

    return highlight_part


def get_content(content):
    return " ".join(jieba.cut(content))


file = 'bin_data/news-summary-20k.csv'

tokens = 'bin_data/chinese_20k_news_tokens/'

filenames = 'bin_data/filename_list/'

if not os.path.exists(tokens): os.makedirs(tokens)
if not os.path.exists(filenames): os.makedirs(filenames)

succeed = 0

all_file_names = []

for ii, c in enumerate(pd.read_csv(file).iterrows()):
    try:
        if len(c[1].summary) >= len(c[1].content): continue
        title = str(datetime.utcnow().strftime("%Y%m%d%H%M%S"))[-8:]
        title = title + str(ii) + '.story'
        file_name = os.path.join(tokens, title)
        token_file = open(file_name, 'w', encoding='utf-8')
        token_file.write(get_content(c[1].content.strip()) + '\n\n')
        token_file.write(create_hightligh_tokens(c[1].summary.strip()))
        token_file.close()
        succeed += 1
        all_file_names.append(title)
        if succeed % 100 == 0: print(succeed)
    except Exception as e:
        print(e)
        continue

print('splitting files')

train, val, test = split_train_val_test(all_file_names)

save_file_list(os.path.join(filenames, 'train.txt'), train)
save_file_list(os.path.join(filenames, 'val.txt'), val)
save_file_list(os.path.join(filenames, 'test.txt'), test)



