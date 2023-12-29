from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
import nltk
import string
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from tqdm import tqdm
import pandas as pd


nltk.download("stopwords")
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")
nltk.download("omw-1.4")

# Assuming you have tqdm imported in your environment
tqdm.pandas()
indo_slang_word = pd.read_csv("data/indo_slang_word.csv")


def cleaning(text):
    # Case folding
    text = text.lower()
    # Trim text
    text = text.strip()
    # Remove punctuations, special characters, and double whitespace
    text = re.compile("<.*?>").sub("", text)
    text = re.compile("[%s]" % re.escape(string.punctuation)).sub(" ", text)
    text = re.sub("\\s+", " ", text)
    # Number removal
    text = re.sub(r"\[[0-9]*\]", " ", text)
    text = re.sub(r"[^\w\s]", "", str(text).lower().strip())
    # Remove number and whitespaces
    text = re.sub(r"\d", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text


def handle_negation(review):
    # Membuat pola regular expression untuk menemukan kata "tidak" dan kata-kata setelahnya
    negation_pattern = re.compile(r"\btidak\b\s+(\w+)")

    # Menggabungkan kata-kata setelah kata "tidak" dengan tanda garis bawah
    modified_review = negation_pattern.sub(
        lambda match: "tidak" + match.group(1), review
    )

    return modified_review


def replace_slang_word(doc, slang_word):
    for index in range(0, len(doc) - 1):
        index_slang = slang_word.slang == doc[index]
        formal = list(set(slang_word[index_slang].formal))
        if len(formal) == 1:
            doc[index] = formal[0]
    return doc


filtering = stopwords.words("indonesian")


def stopword_removal(review):
    return [x for x in review if x not in filtering]


factory = StemmerFactory()
stemmer = factory.create_stemmer()


def process_review(review):
    review = cleaning(review)
    review = handle_negation(review)
    review = word_tokenize(review)
    review = replace_slang_word(review, indo_slang_word)
    review = stopword_removal(review)
    review = [stemmer.stem(word) for word in review]
    return " ".join(review)


def data_preprocessor(data):
    df = pd.DataFrame(data)
    df["review"] = df["review"].progress_apply(process_review)

    return df
