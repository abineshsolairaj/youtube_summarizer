import argparse
import sys
from heapq import nlargest
from string import punctuation

import spacy
from pytube import extract
from spacy.lang.en.stop_words import STOP_WORDS
from youtube_transcript_api import YouTubeTranscriptApi


DEFAULT_URL = "https://www.youtube.com/watch?v=fLvJ8VdHLA0"
SUMMARY_RATIO = 0.3


def fetch_transcript(url):
    video_id = extract.video_id(url)
    transcript = YouTubeTranscriptApi().fetch(video_id)
    return " ".join(snippet.text for snippet in transcript)


def summarize(text, ratio=SUMMARY_RATIO):
    nlp = spacy.load("en_core_web_sm")
    document = nlp(text)

    word_frequencies = {}
    for token in document:
        word = token.text.lower()
        if word in STOP_WORDS or word in punctuation:
            continue
        word_frequencies[word] = word_frequencies.get(word, 0) + 1

    if not word_frequencies:
        return ""

    max_frequency = max(word_frequencies.values())
    for word in word_frequencies:
        word_frequencies[word] /= max_frequency

    sentences = list(document.sents)
    scores = {}
    for sentence in sentences:
        for token in sentence:
            weight = word_frequencies.get(token.text.lower())
            if weight is not None:
                scores[sentence] = scores.get(sentence, 0) + weight

    select_length = max(1, int(len(sentences) * ratio))
    top_sentences = set(nlargest(select_length, scores, key=scores.get))
    ordered = [sentence.text for sentence in sentences if sentence in top_sentences]
    return " ".join(ordered)


def main():
    parser = argparse.ArgumentParser(description="Summarize a YouTube video from its transcript.")
    parser.add_argument("url", nargs="?", default=DEFAULT_URL, help="YouTube video URL")
    parser.add_argument("--ratio", type=float, default=SUMMARY_RATIO,
                        help="Fraction of sentences to keep in the summary (0 < ratio <= 1)")
    args = parser.parse_args()

    if not 0 < args.ratio <= 1:
        parser.error("--ratio must be in the (0, 1] range")

    try:
        text = fetch_transcript(args.url)
    except Exception as exc:
        print(f"Failed to fetch transcript: {exc}", file=sys.stderr)
        sys.exit(1)

    print(summarize(text, args.ratio))


if __name__ == "__main__":
    main()
