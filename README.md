# text-augmentation
Backtranslated imdb movie reviews.
Each directory is named `imdb_{language_code}` and mimics the original structure of the `imdb` dataset.

### Backtranslating movie reviews to more languages

For backtranslating training data through Italian, the command would be

```
python cache_backtranslations.py     --imdb_dir imdb/train/ --target_language it
```

### Backtranslating other text
Modify cache_backtranslations.py to read from and write to new paths
