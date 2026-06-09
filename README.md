# youtube_summarizer

A Python command-line tool that summarizes a YouTube video by downloading its
transcript and extracting the most important sentences using extractive,
frequency-based scoring with spaCy.

## How it works

1. **Extract the video ID** from the YouTube URL using `pytube`.
2. **Download the transcript** for that video with `youtube-transcript-api`.
3. **Tokenize and segment** the transcript into sentences and words using the
   spaCy `en_core_web_sm` English model.
4. **Compute word frequencies**, ignoring stop words (e.g. "the", "a", "an")
   and punctuation. Frequencies are normalized by the maximum frequency so
   each word has a weight in `(0, 1]`.
5. **Score each sentence** as the sum of its constituent word weights.
6. **Select the top N sentences** (default 30%, configurable) with `heapq.nlargest`,
   then emit them in original document order so the summary reads naturally.

## Requirements

- Python 3.8+
- Internet access to fetch the transcript and download the spaCy model
- A video that has captions/transcripts available on YouTube

## Installation

Clone the repository and install the dependencies:

```bash
git clone https://github.com/abineshsolairaj/youtube_summarizer.git
cd youtube_summarizer
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

It is recommended to install inside a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## Usage

Run the script with a YouTube URL as the positional argument:

```bash
python youtube_summarizer.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

If you omit the URL, a built-in sample URL is used:

```bash
python youtube_summarizer.py
```

### Options

| Flag | Default | Description |
|---|---|---|
| `url` (positional) | sample video | Full YouTube video URL to summarize |
| `--ratio` | `0.3` | Fraction of sentences to keep in the summary, in `(0, 1]` |
| `-h`, `--help` | — | Show the help message and exit |

### Examples

Keep the top 20% of sentences:

```bash
python youtube_summarizer.py "https://www.youtube.com/watch?v=VIDEO_ID" --ratio 0.2
```

Save the summary to a file:

```bash
python youtube_summarizer.py "https://www.youtube.com/watch?v=VIDEO_ID" > summary.txt
```

### Exit codes

| Code | Meaning |
|---|---|
| `0` | Summary printed successfully |
| `1` | Transcript could not be fetched (network error, no captions, etc.) |
| `2` | Invalid command-line arguments (e.g. `--ratio` outside `(0, 1]`) |

## Troubleshooting

- **`Failed to fetch transcript: ...`** — The video has no transcript
  available, captions are disabled, the URL is invalid, or YouTube blocked
  the request. Try a different video or check your network.
- **`Can't find model 'en_core_web_sm'`** — Run
  `python -m spacy download en_core_web_sm`.
- **`ModuleNotFoundError`** — Re-run `pip install -r requirements.txt`,
  preferably inside a virtual environment.

## Project layout

```
youtube_summarizer/
├── README.md
├── requirements.txt
└── youtube_summarizer.py
```

## License

See repository for license information.
