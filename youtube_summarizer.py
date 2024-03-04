from pytube import extract
from heapq import nlargest
from youtube_transcript_api import YouTubeTranscriptApi
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation

#Replace with your favorite video url
url = 'https://www.youtube.com/watch?v=fLvJ8VdHLA0'
video_id = extract.video_id(url)

video_transcript = YouTubeTranscriptApi.get_transcript(video_id)
text = ""
for elem in video_transcript:
    text = text + " " + elem["text"]

nlp = spacy.load('en_core_web_sm')
document = nlp(text)
for sentence in document.sents:
    print(sentence.text)

tokens = [token.text for token in document]

word_frequencies = {}
for word in document:
    text = word.text.lower()
    if text not in list(STOP_WORDS) and text not in punctuation:
        if word.text not in word_frequencies.keys():
            word_frequencies[word.text] = 1
        else:
            word_frequencies[word.text] += 1

max_frequency = max(word_frequencies.values())
for word in word_frequencies.keys():
    word_frequencies[word] = word_frequencies[word]/max_frequency

tokens = [sentence for sentence in document.sents]
score = {}
for sentence in tokens:
    for word in sentence:
        if word.text.lower() in word_frequencies.keys():
            if sentence not in score.keys():
                score[sentence] = word_frequencies[word.text.lower()]
            else:
                score[sentence] += word_frequencies[word.text.lower()]

select_length = int(len(tokens) * 0.3)
summary = nlargest(select_length, score, key = score.get)
final_summary = [word.text for word in summary]
summary = ' '.join(final_summary)
print(summary)