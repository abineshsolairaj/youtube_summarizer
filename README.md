# youtube_summarizer

This Python code summarizes a YouTube video by analyzing its transcript and extracting the most important sentences.

# Functionality

# Import Libraries: The code utilizes libraries for:

- pytube: Extracting video IDs from URLs.
- youtube_transcript_api: Downloading video transcripts.
- spaCy: Performing Natural Language Processing tasks.
- heapq: Finding the most frequent elements.

# Get Video Transcript:

- The code takes a YouTube video URL (replace with your desired URL).
- It extracts the video ID from the URL.
- Then, it downloads the transcript of the video using the YouTubeTranscriptApi.
- Finally, it combines all transcript elements into a single text string.

# Sentence Segmentation and Tokenization:

- The code employs spaCy to load a pre-trained English language model (en_core_web_sm).
- It then processes the text string to identify individual sentences and splits them into words (tokens).

# Frequency Analysis and Normalization:

- It removes stop words (common words like "the", "a", "an") and punctuation marks from the tokens.
- It calculates the frequency of each unique word, excluding stop words and punctuation.
- To account for word length variations, word frequencies are normalized by dividing them by the maximum frequency in the text.

# Sentence Scoring:

- Each sentence is assigned a score based on the sum of the normalized frequencies of its constituent words.
- Sentences with words appearing more frequently in the transcript will receive higher scores.

# Summary Generation:

- The code selects the top 30% (configurable) of sentences with the highest scores using the heapq library.
- Finally, it combines the words from these high-scoring sentences to form a summary of the video.

Overall, this code demonstrates an automated approach to summarizing YouTube videos by leveraging Natural Language Processing techniques.