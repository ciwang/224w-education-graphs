from pathlib import Path
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
import csv
import re

TAG_RE = re.compile(r'<[^>]+>')
def clean(text):
    return TAG_RE.sub('', text)

if len(sys.argv) > 1:
    CSV_FILE = sys.argv[1]
else:
    CSV_FILE = '../data/academia.stackexchange.com/Posts.csv'

corpus = []
with open(CSV_FILE, "r") as f:
    reader = csv.reader(f)
    reader.__next__()
    for row in reader:
        new_row = row[:]
        new_row[3] = clean(new_row[3])
        new_row[3] = new_row[3].replace('\n', ' ')
        corpus.append(new_row[3])

tf = TfidfVectorizer(analyzer = 'word', stop_words = 'english')
tfidf_matrix = tf.fit_transform(corpus)
feature_names = tf.get_feature_names()

top_dict = defaultdict(int)
dense = tfidf_matrix.todense()
for num, row in enumerate(dense):
    post_body = row.tolist()[0]
    phrase_scores = [pair for pair in zip(range(0, len(post_body)), post_body) if pair[1] > 0]
    sorted_phrase_scores = sorted(phrase_scores, key = lambda t: t[1] * -1)
    # print('---ROW {}---'.format(num))
    for phrase, score in [(feature_names[word_id], score) for (word_id, score) in sorted_phrase_scores][:3]:
        # print('{0: <20} {1}'.format(phrase, score))
        top_dict[phrase] += 1

most_important = []
sorted_keys = sorted(top_dict, key = top_dict.get, reverse = True)
for key in sorted_keys:
    most_important.append((key, top_dict[key]))

OUTPUT_FILE = Path(CSV_FILE).with_suffix('.most_important.txt')
with open(OUTPUT_FILE, 'w') as f:
    for item in most_important:
        f.write('{}\n'.format(item))

print('Created file {}'.format(OUTPUT_FILE))