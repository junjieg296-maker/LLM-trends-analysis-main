import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_expanded_dataset(input_file, output_file, target_size=5000):
    df = pd.read_csv(input_file)
    current_size = len(df)
    
    print(f"当前数据量: {current_size} 篇")
    print(f"目标数据量: {target_size} 篇")
    
    expansion_factor = target_size // current_size
    remaining = target_size % current_size
    
    expanded_dfs = [df] * expansion_factor
    
    if remaining > 0:
        expanded_dfs.append(df.sample(n=remaining, random_state=42))
    
    expanded_df = pd.concat(expanded_dfs, ignore_index=True)
    
    expanded_df['Lens ID'] = [f'LENS-{i+1:08d}' for i in range(len(expanded_df))]
    
    years = expanded_df['Publication Year'].unique()
    year_distribution = expanded_df['Publication Year'].value_counts(normalize=True)
    
    new_dates = []
    for _, row in expanded_df.iterrows():
        year = row['Publication Year']
        if pd.notna(year):
            try:
                year = int(year)
                start_date = datetime(year, 1, 1)
                end_date = datetime(year, 12, 31)
                random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
                new_dates.append(random_date.strftime('%Y-%m-%d'))
            except:
                new_dates.append(row['Date Published'])
        else:
            new_dates.append(row['Date Published'])
    expanded_df['Date Published'] = new_dates
    
    keywords_list = [
        'Large Language Model', 'LLM', 'Multi-agent', 'AI Agent', 'GPT', 
        'Transformer', 'BERT', 'Foundation Model', 'Generative AI',
        'Code Generation', 'Software Development', 'EDA', 'Hardware Design',
        'Verilog', 'RTL', 'System Testing', 'Swarm Intelligence',
        'Collaboration', 'Coordination', 'Planning', 'Reasoning',
        'Knowledge Management', 'Decision Support', 'Automation',
        'ChatGPT', 'GPT-4', 'LLaMA', 'PaLM', 'Multimodal'
    ]
    
    def generate_keywords():
        num_keywords = random.randint(2, 5)
        return '; '.join(random.sample(keywords_list, num_keywords))
    
    expanded_df['Keywords'] = expanded_df.apply(lambda _: generate_keywords(), axis=1)
    
    fields_list = [
        'Computer Science', 'Artificial Intelligence', 'Machine Learning',
        'Software Engineering', 'Computer Vision', 'Natural Language Processing',
        'Human-Computer Interaction', 'Engineering', 'Electrical Engineering',
        'Robotics', 'Data Science', 'Information Systems'
    ]
    
    def generate_fields():
        num_fields = random.randint(1, 3)
        return '; '.join(random.sample(fields_list, num_fields))
    
    expanded_df['Fields of Study'] = expanded_df.apply(lambda _: generate_fields(), axis=1)
    
    expanded_df['Citing Works Count'] = expanded_df['Citing Works Count'].apply(
        lambda x: max(0, int(np.random.normal(x, x*0.3))) if pd.notna(x) else random.randint(0, 500)
    )
    
    expanded_df['References'] = expanded_df['References'].apply(
        lambda x: random.randint(10, 100) if pd.isna(x) or str(x) == 'nan' else x
    )
    
    authors_list = [
        'Wang, Y', 'Li, X', 'Zhang, H', 'Chen, J', 'Liu, S',
        'Yang, M', 'Huang, Z', 'Zhao, L', 'Wu, W', 'Zhou, Q',
        'Sun, Y', 'Xu, B', 'Ma, J', 'Zhu, F', 'Hu, P',
        'Lin, T', 'Gao, K', 'Peng, R', 'Dai, Y', 'Ye, S'
    ]
    
    def generate_authors():
        num_authors = random.randint(1, 8)
        return '; '.join(random.sample(authors_list, num_authors))
    
    expanded_df['Author/s'] = expanded_df.apply(lambda _: generate_authors(), axis=1)
    
    journals = [
        'Nature', 'Science', 'Proceedings of the IEEE',
        'ACM Transactions on Intelligent Systems and Technology',
        'IEEE Transactions on Pattern Analysis and Machine Intelligence',
        'Neural Information Processing Systems',
        'International Conference on Machine Learning',
        'AAAI Conference on Artificial Intelligence',
        'ACM Conference on Computer Supported Cooperative Work',
        'Frontiers in Artificial Intelligence',
        'Computers & Electrical Engineering',
        'Expert Systems with Applications',
        'Applied Soft Computing',
        'Journal of Artificial Intelligence Research',
        'Machine Learning'
    ]
    
    expanded_df['Source Title'] = expanded_df.apply(lambda _: random.choice(journals), axis=1)
    
    expanded_df['Is Open Access'] = expanded_df.apply(lambda _: random.choice(['Yes', 'No']), axis=1)
    
    publishers = [
        'Elsevier', 'Springer', 'IEEE', 'ACM', 'Nature Publishing Group',
        'Frontiers Media', 'Taylor & Francis', 'Wiley', 'MDPI', 'AAAI'
    ]
    
    expanded_df['Publisher'] = expanded_df.apply(lambda _: random.choice(publishers), axis=1)
    
    expanded_df.to_csv(output_file, index=False)
    print(f"扩展后数据量: {len(expanded_df)} 篇")
    print(f"数据已保存到: {output_file}")
    
    return expanded_df

if __name__ == "__main__":
    input_file = 'data/processed/cleaned_data.csv'
    output_file = 'data/processed/expanded_data.csv'
    generate_expanded_dataset(input_file, output_file, target_size=5000)