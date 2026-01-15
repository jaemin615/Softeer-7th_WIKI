import sys
import csv

def load_words(filename):
    word_set = set()
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                word = line.strip().lower()
                if word:
                    word_set.add(word)
    except FileNotFoundError:
        pass
    return word_set

POSITIVE_WORDS = load_words('positive-words.txt')
NEGATIVE_WORDS = load_words('negative-words.txt')

def classify_sentiment(text):
    text = text.lower()
    words_in_text = text.split()
    
    pos_count = sum(1 for word in words_in_text if word in POSITIVE_WORDS)
    neg_count = sum(1 for word in words_in_text if word in NEGATIVE_WORDS)

    if pos_count > neg_count:
        return "positive"
    elif neg_count > pos_count:
        return "negative"
    else:
        return "neutral"

def main():
    reader = csv.reader(sys.stdin)

    for row in reader:
        if len(row) >= 6:
            tweet_text = row[5]
            sentiment = classify_sentiment(tweet_text)
            print(f"{sentiment}\t1")

if __name__ == "__main__":
    main()
