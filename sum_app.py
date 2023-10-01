import streamlit as st
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# Download only if not already downloaded
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

st.title('Webpage Summarization App')

# User input for URL
url = st.text_input('Enter the URL of the article you want to summarize:')

# Summary length slider
summary_length = st.slider('Choose the length of the summary:', min_value=1, max_value=10, value=3)

if url:
    st.write('Generating summary...')
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    paragraphs = soup.find_all('p')
    text = ' '.join([p.text for p in paragraphs])
    
    # Calculate read time
    words = text.split()
    read_time = len(words) // 200
    
    st.write(f'Estimated Read Time: {read_time} minutes')

    summary = ' '.join(text.split('.')[:summary_length]) + '.'
    st.write('Summary:', summary)

    # Tokenize and remove stopwords
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text.lower())
    filtered_words = [w for w in word_tokens if not w in stop_words and w.isalnum()]

    # Get frequency distribution
    freq_dist = nltk.FreqDist(filtered_words)
    keywords = [word for word, freq in freq_dist.items() if freq > 2]

    # Show keywords in Streamlit
    st.write('Keywords:', ', '.join(keywords))
