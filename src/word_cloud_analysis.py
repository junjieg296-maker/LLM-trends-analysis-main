import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import os
import nltk
from nltk.corpus import stopwords


def generate_word_cloud():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_path, 'data', 'processed', 'cleaned_data.csv')
    output_dir = os.path.join(base_path, 'outputs', 'figures')

    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords')

    df = pd.read_csv(data_path)
    text = " ".join(title for title in df.Title.astype(str))

    custom_stopwords = set(STOPWORDS)
    custom_stopwords.update(["based", "using", "study", "analysis", "approach", "framework", "system"])
    custom_stopwords.update(stopwords.words('english'))

    print("Analyzing keywords and generating word cloud...")
    wc = WordCloud(
        background_color='white',
        max_words=100,
        width=1600,
        height=800,
        stopwords=custom_stopwords,
        colormap='coolwarm',
        contour_width=1,
        contour_color='steelblue'
    ).generate(text)

    plt.figure(figsize=(20, 10), dpi=300)
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")

    output_file = os.path.join(output_dir, 'wordcloud_titles.png')
    plt.savefig(output_file, bbox_inches='tight')
    print("Word cloud saved to: {}".format(output_file))
    plt.close()


if __name__ == "__main__":
    generate_word_cloud()