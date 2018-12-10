# uses Python 3, may not work in Python 2

from pathlib import Path
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
from nltk.stem.snowball import SnowballStemmer
import csv
import re
from tqdm import tqdm
from bs4 import BeautifulSoup
import pickle

########## PARAMETERS TO ADJUST ##########

# number of top words (by tf-idf) to extract from each postbody
NUM_TOP_WORDS = 5

# filepaths
if len(sys.argv) > 1:
    CSV_FILE = sys.argv[1]
else:
    CSV_FILE = '../data/stats.stackexchange.com/Posts_0.csv'

OUTPUT_FILE = Path(CSV_FILE).with_name('STATS_20k-' + Path(CSV_FILE).with_suffix('').name + '-top_uni&bigrams_nostem').with_suffix('.tsv')

PICKLE_FILE = Path(OUTPUT_FILE).with_suffix('.pickle')

# if using a split CSV, the index of the first data row, else 0
START_ROW = 0

# set both to 1 for unigram, 2 for bigram, etc., or set a range
NGRAM_START = 1
NGRAM_END = 2

# use Snowball stemmer before building tf-idf matrix?
STEMMER = False

########################################

# columns in the <input>.csv file
ROW_INDEX = 0
BODY_INDEX = 3
ID_INDEX = 9
OWNERUSERID_INDEX = 15
DATE_INDEX = 7
POSTTYPEID_INDEX = 17
TAG_INDEX = 19
TITLE_INDEX = 20

# remove html tags, <code> blocks, latex math mode, etc. from postbodies
RE_LATEX = re.compile(r'\$.+?\$')
RE_LATEX2 = re.compile(r'\$\$.+?\$\$', flags=re.MULTILINE|re.DOTALL)
RE_LATEX3 = re.compile(r'\\begin{align}.+?\\end{align}', flags=re.MULTILINE|re.DOTALL)
RE_VARS = re.compile(r'\b.\_.\b')
RE_VARS2 = re.compile(r'\b\D\d\b')
RE_HTML = re.compile(r'<[^>]+>')
RE_NUMBERS = re.compile(r'\b\d+\b')

def clean(text):
    text = RE_LATEX2.sub('', text)
    text = RE_LATEX3.sub('', text)
    text = RE_LATEX.sub('', text)
    soup = BeautifulSoup(text, 'html.parser')
    for code_block in soup.find_all('code'):
        code_block.decompose()
    text = str(soup)
    text = RE_HTML.sub('', text)
    text = RE_NUMBERS.sub('', text)
    text = RE_VARS.sub('', text)
    text = RE_VARS2.sub('', text)
    return text

########## cleaning and loading into corpus ##########

reference = defaultdict(list)
postid_dict = defaultdict(list)
corpus = []
print('Building reference dict...')
with open(CSV_FILE, "r") as f:
    reader = csv.reader(f)
    reader.__next__()
    for row in reader:
        new_row = row[:]
        new_row[BODY_INDEX] = clean(new_row[BODY_INDEX])
        new_row[BODY_INDEX] = new_row[BODY_INDEX].replace('\n', ' ')
        new_row[TAG_INDEX] = new_row[TAG_INDEX].replace('<', '')
        new_row[TAG_INDEX] = new_row[TAG_INDEX].replace('>', ', ')
        reference[int(new_row[ROW_INDEX])] = [new_row[BODY_INDEX], new_row[ID_INDEX], new_row[OWNERUSERID_INDEX], new_row[DATE_INDEX], new_row[POSTTYPEID_INDEX], new_row[TITLE_INDEX], new_row[TAG_INDEX]]
        postid_dict[int(new_row[ID_INDEX])] = [new_row[BODY_INDEX], new_row[TITLE_INDEX], new_row[TAG_INDEX]]
        corpus.append(new_row[BODY_INDEX])

# reference is a dict of (postbody, postid, userid) with row as key
# corpus is a list of postbodies, index is the row the postbody came from
assert corpus[0] == reference[START_ROW + 0][0]
if corpus[100]:
    assert corpus[100] == reference[START_ROW + 100][0]
if corpus[1000]:
    assert corpus[1000] == reference[START_ROW + 1000][0]
if corpus[10000]:
    assert corpus[10000] == reference[START_ROW + 10000][0]

print('Reference dict built.')

if STEMMER:
    print('Applying Snowball stemmer...')

    stemmer = SnowballStemmer('english')
    stemmed_corpus = []
    for postbody in tqdm(corpus):
        stemmed_words = " ".join([stemmer.stem(word) for word in postbody.split()])
        stemmed_corpus.append(stemmed_words)
else:
    stemmed_corpus = corpus

########## finding top words for each postbody ##########

print('Building tf-idf matrix...')

tf = TfidfVectorizer(analyzer = 'word',
                     stop_words = 'english',
                     strip_accents = 'unicode',
                     ngram_range=(NGRAM_START, NGRAM_END))
tfidf_matrix = tf.fit_transform(stemmed_corpus)
feature_names = tf.get_feature_names()

output = []

print('Finding top phrases...')

dense = tfidf_matrix.todense()
for num, row in enumerate(tqdm(dense)):
    post_body = row.tolist()[0]
    phrase_scores = [pair for pair in zip(range(0, len(post_body)), post_body) if pair[1] > 0]
    sorted_phrase_scores = sorted(phrase_scores, key = lambda t: t[1] * -1)
    top_phrases = []
    for phrase, score in [(feature_names[word_id], score) for (word_id, score) in sorted_phrase_scores][:NUM_TOP_WORDS]:
        top_phrases.append(phrase)
    output.append(reference[START_ROW + num] + top_phrases)
    postid = reference[START_ROW + num][1]
    postid_dict[postid].append(top_phrases)

########## output to file ##########

with open(PICKLE_FILE, 'wb') as f:
    pickle.dump(postid_dict, f, protocol = 2)

print('Postid dict saved to {}.'.format(PICKLE_FILE))

print('Writing to {}...'.format(OUTPUT_FILE))

with open(OUTPUT_FILE, 'w', newline='') as tsvfile:
    writer = csv.writer(tsvfile, delimiter='\t')
    header_row = ['Body', 'Id', 'OwnerUserId',  'Date', 'PostTypeId', 'Title', 'Tags']
    for num in range(1, NUM_TOP_WORDS + 1):
        header_row.append('TopWord{}'.format(num))
    writer.writerow(header_row)
    for line in output:
        writer.writerow(line)

print('Finished writing to {}.'.format(OUTPUT_FILE))