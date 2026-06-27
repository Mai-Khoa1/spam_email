"""Gộp 3 dataset thành dataset song ngữ Anh-Việt."""
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent / 'spam_detector_ai' / 'data'

# 1. English dataset
en = pd.read_csv(DATA_DIR / 'spam.csv', encoding='latin-1', usecols=['label', 'text'])
en = en.dropna(subset=['label', 'text'])
en['label'] = en['label'].str.strip().str.lower()
en = en[en['label'].isin(['spam', 'ham'])][['label', 'text']]

# 2. Vietnamese dataset (tự tạo, có cả spam/ham)
vi1 = pd.read_csv(DATA_DIR / 'spam_vi.csv', encoding='utf-8', usecols=['label', 'text'])
vi1 = vi1.dropna(subset=['label', 'text'])
vi1['label'] = vi1['label'].str.strip().str.lower()
vi1 = vi1[vi1['label'].isin(['spam', 'ham'])][['label', 'text']]

# 3. Vietnamese spam dataset (toàn spam)
vi2 = pd.read_csv(DATA_DIR / 'vietnamese_spam_dataset.csv', encoding='utf-8', usecols=['label', 'text'])
vi2 = vi2.dropna(subset=['label', 'text'])
vi2['label'] = vi2['label'].str.strip().str.lower()
vi2 = vi2[vi2['label'].isin(['spam', 'ham'])][['label', 'text']]

# Gộp và xáo trộn
combined = pd.concat([en, vi1, vi2], ignore_index=True)
combined = combined.sample(frac=1, random_state=42).reset_index(drop=True)

output = DATA_DIR / 'spam_combined.csv'
combined.to_csv(output, index=False, encoding='utf-8')

print(f'Dataset song ngu da tao: {output}')
print(f'Tong so mau : {len(combined)}')
print(f'  Tieng Anh : {len(en)}')
print(f'  VI (spam_vi.csv)           : {len(vi1)}')
print(f'  VI (vietnamese_spam_dataset): {len(vi2)}')
print(f'\nPhan phoi nhan:')
print(combined['label'].value_counts().to_string())
