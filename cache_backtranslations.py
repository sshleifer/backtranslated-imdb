import textblob

import itertools
import glob
import time
from tqdm import tqdm_notebook, tqdm
# from fastai.text import *
# from fastai.core import save_texts
import pickle
from pathlib import Path
import pathlib
import fire
import shutil

def pickle_save(obj, path):
    with open(path, 'wb') as f:
        pickle.dump(obj, f)

def pickle_load(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

def make_dir_structure_under(path) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)


def open_text(fn, enc='utf-8'):
    "Read the text in `fn`."
    with open(fn,'r', encoding = enc) as f: return ''.join(f.readlines())


def save_texts(fname, texts):
    "Save in `fname` the content of `texts`."
    with open(fname, 'w') as f:
        for t in texts: f.write(f'{t}\n')

VERBOSE = False
def back_translate(text, target_language, verbose=VERBOSE):
    es =  textblob.TextBlob(text).translate(to=target_language, from_lang='en')
    en =  textblob.TextBlob(str(es)).translate(to="en")
    if verbose:
        print(text)
        print(es)
        print(en)
    return str(en)

def saver(pth, target_language, google=False, do_sleep=True):
    assert isinstance(pth, str)
    text = open_text(pth)
    save_path = pth.replace('imdb', f'imdb_{target_language}')
    make_dir_structure_under(save_path)
    if Path(save_path).exists():
        return
    if google:
        back = back_gtranslate([text], target_language=target_language)
    else:
        back = back_translate(text, target_language=target_language)
    save_texts(save_path, [back])
    if do_sleep:
        time.sleep(.1)  # to avoid getting blocked

def map_backtranslate():
    """"""
    raise NotImplementedError()
    from multiprocessing import Pool

    import funcy
    path = untar_data(URLs.IMDB)
    txt_files = glob.glob(f'{path}/train/*/*.txt')
    pool = Pool(8)
    chunks = funcy.chunks(1000, txt_files)
    pool.map(save_backtranslations, list(chunks))


def gtranslate(text,  source_language='es', target_language='es'):
    from google.cloud import translate
    # Instantiates a client
    translate_client = translate.Client()
    translation = translate_client.translate(text, target_language=target_language, source_language=source_language)
    return [x['translatedText'] for x in translation]


def back_gtranslate(text, source_language='es', target_language='es'):
    spanish = gtranslate(text, source_language=source_language, target_language=target_language)
    english = gtranslate(spanish, source_language=target_language, target_language=source_language)
    return english

import numpy as np

def copy_subset_of_files(src_path: pathlib.Path, dest_path, n=500):
    """More making small IMDB"""
    if isinstance(src_path, str):
        src_path = Path(src_path)
    if isinstance(dest_path, str):
        dest_path = Path(dest_path)
    for sd in ['test', 'train']:
        sdir = src_path / sd
        paths = list(sdir.glob('*/*.txt'))
        small_paths = np.random.choice(paths, size=n, replace=False)
        for sp in small_paths:
            dest_path = dest_path / sp.relative_to(src_path)
            make_dir_structure_under(dest_path)
            shutil.copy(sp, dest_path)
    sdir = src_path / 'unsup'
    paths = list(sdir.glob('*.txt'))
    small_paths = np.random.choice(paths, size=n, replace=False)
    for sp in small_paths:
        dest_path = dest_path / sp.relative_to(src_path)
        make_dir_structure_under(dest_path)
        shutil.copy(sp, dest_path)


def stupid_shuffle(txt_files):
    combo = itertools.combinations(txt_files, len(txt_files))
    for shuff_files in combo:
        break
    return shuff_files

PAT = '*/*.txt'

def run(imdb_dir, target_language):
    #/ Users / shleifer /.fastai / data / imdb / train /
    neg_files = glob.glob(imdb_dir + 'neg/*.txt')
    pos_files = glob.glob(imdb_dir + 'pos/*.txt')
    txt_files = stupid_shuffle(neg_files + pos_files)
    for pth in tqdm(txt_files):
        try:
            saver(pth, target_language)
        except Exception as e:
            print(e, pth)


if __name__ == '__main__': fire.Fire(run)
