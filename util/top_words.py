# uses Python 3, may not work in Python 2

from pathlib import Path
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
from nltk.stem.snowball import SnowballStemmer
import csv
import re
from tqdm import tqdm

# columns in the <input>.csv file
ROW_INDEX = 0
BODY_INDEX = 3
ID_INDEX = 9
OWNERUSERID_INDEX = 15
DATE_INDEX = 7
POSTTYPEID_INDEX = 17
TAG_INDEX = 19

# number of top words (by tf-idf) to extract from each postbody
NUM_TOP_WORDS = 5

# remove html tags from postbodies
TAG_RE = re.compile(r'<[^>]+>')
def clean(text):
    return TAG_RE.sub('', text)

# filepaths
if len(sys.argv) > 1:
    CSV_FILE = sys.argv[1]
else:
    CSV_FILE = '../data/stats.stackexchange.com/Posts_2.csv'

# if using a split CSV, the index of the first data row, else 0
START_ROW = 200000

OUTPUT_FILE = Path(CSV_FILE).with_name(Path(CSV_FILE).with_suffix('').name + '-top_words_more').with_suffix('.tsv')

########## cleaning and loading into corpus ##########

reference = defaultdict(list)
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
        reference[int(new_row[ROW_INDEX])] = [new_row[BODY_INDEX], new_row[ID_INDEX], new_row[OWNERUSERID_INDEX], new_row[DATE_INDEX], new_row[POSTTYPEID_INDEX], new_row[TAG_INDEX]]
        corpus.append(new_row[BODY_INDEX])

# reference is a dict of (postbody, postid, userid) with row as key
# corpus is a list of postbodies, index is the row the postbody came from
assert corpus[0] == reference[START_ROW + 0][0]
assert corpus[100] == reference[START_ROW + 100][0]
assert corpus[8000] == reference[START_ROW + 8000][0]

print('Reference dict built.')

# stem the corpus
print('Applying Snowball stemmer...')

stemmer = SnowballStemmer('english')
stemmed_corpus = []
for postbody in tqdm(corpus):
    stemmed_words = " ".join([stemmer.stem(word) for word in postbody.split()])
    stemmed_corpus.append(stemmed_words)

########## finding top words for each postbody ##########

print('Building tf-idf matrix...')

tf = TfidfVectorizer(analyzer = 'word', stop_words = 'english', strip_accents = 'unicode')
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

########## output to file ##########

print('Writing to {}...'.format(OUTPUT_FILE))

with open(OUTPUT_FILE, 'w', newline='') as tsvfile:
    writer = csv.writer(tsvfile, delimiter='\t')
    header_row = ['Body', 'Id', 'OwnerUserId',  'Date', 'PostTypeId', 'Tags']
    for num in range(1, NUM_TOP_WORDS + 1):
        header_row.append('TopWord{}'.format(num))
    writer.writerow(header_row)
    for line in output:
        writer.writerow(line)

print('Finished writing to {}.'.format(OUTPUT_FILE))