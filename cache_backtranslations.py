import textblob
import funcy
import glob
import time
from tqdm import tqdm_notebook, tqdm
from fastai.text import *
from fastai.core import save_texts
import pickle
from pathlib import Path
from multiprocessing import Pool

def pickle_save(obj, path):
    with open(path, 'wb') as f:
        pickle.dump(obj, f)

def pickle_load(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

def make_dir_structure_under(path) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)


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
        time.sleep(1)  # to avoid getting bothced

def map_backtranslate():
    """"""
    raise NotImplementedError()
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


txt_files = glob('/Users/shleifer/.fastai/data/imdb/train/*/*.txt')
