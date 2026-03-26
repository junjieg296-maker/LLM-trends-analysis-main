import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import os
import nltk
from nltk.corpus import stopwords


def generate_word_cloud():
    # 1. 路径设置
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_path, 'data', 'processed', 'cleaned_data.csv')
    output_dir = os.path.join(base_path, 'outputs', 'figures')

    # 下载停用词表（如果没下过的话）
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords')

    # 2. 读取数据
    df = pd.read_csv(data_path)
    # 将所有标题拼成一个大长文本
    # 注意：这里我们用 Title，如果你想更深入可以用 Abstract，但 Title 最精准
    text = " ".join(title for title in df.Title.astype(str))

    # 3. 设置停用词 (过滤掉无意义的词)
    # 除了系统默认的，我们还可以手动添加一些干扰词
    custom_stopwords = set(STOPWORDS)
    custom_stopwords.update(["based", "using", "study", "analysis", "approach", "framework", "system"])
    # 加上 nltk 的英文停用词
    custom_stopwords.update(stopwords.words('english'))

    # 4. 生成词云
    print("🚀 正在分析关键词并生成词云...")
    wc = WordCloud(
        background_color='white',  # 背景选白色，打印出来省墨且专业
        max_words=100,  # 只看最火的 100 个关键词
        width=1600,
        height=800,
        stopwords=custom_stopwords,
        colormap='coolwarm',  # 颜色方案：冷暖色调
        contour_width=1,
        contour_color='steelblue'
    ).generate(text)

    # 5. 展示与保存
    plt.figure(figsize=(20, 10), dpi=300)
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")  # 不显示坐标轴

    output_file = os.path.join(output_dir, 'wordcloud_titles.png')
    plt.savefig(output_file, bbox_inches='tight')
    print(f"✅ 关键词词云已生成至: {output_file}")
    plt.show()


if __name__ == "__main__":
    generate_word_cloud()