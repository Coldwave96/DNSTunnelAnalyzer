import ast
import pandas as pd
from sklearn.utils import shuffle
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

import utils

labels = []
dataset_df = pd.DataFrame()

print("[*] Loading datasets...")
# Load benign datasets
labels.append('benign')
benign_folder_path = "Datasets/Stateful/Benign"
benign_files_list = utils.list_files_in_folder(benign_folder_path)

for file in benign_files_list:
    file_df = pd.read_csv(file)
    file_df['label'] = 0
    dataset_df = pd.concat([dataset_df, file_df], ignore_index=True)

# Load attack datasets
labels.append('malicious')
malicious_folder_path = "Datasets/Stateful/Attacks"
malicious_files_list = utils.list_files_in_folder(malicious_folder_path)

for file in malicious_files_list:
    file_df = pd.read_csv(file)
    file_df['label'] = 1
    dataset_df = pd.concat([dataset_df, file_df], ignore_index=True)

print("[*] Done!\n\n[*] Processing datasets...")
dataset_df = shuffle(dataset_df)
dataset_df = dataset_df.fillna(0)

label_encoder = LabelEncoder()
dataset_df['rr_type'] = label_encoder.fit_transform(dataset_df['rr_type'])
dataset_df['distinct_ip'] = label_encoder.fit_transform(dataset_df['distinct_ip'])
dataset_df['unique_country'] = label_encoder.fit_transform(dataset_df['unique_country'])
dataset_df['unique_asn'] = label_encoder.fit_transform(dataset_df['unique_asn'])
dataset_df['distinct_domains'] = label_encoder.fit_transform(dataset_df['distinct_domains'])
dataset_df['reverse_dns'] = label_encoder.fit_transform(dataset_df['reverse_dns'])

dataset_df['unique_ttl'] = dataset_df['unique_ttl'].apply(lambda x: ast.literal_eval(x) if type(x) == str else x)
dataset_df['unique_ttl'] = dataset_df['unique_ttl'].apply(lambda x: sum(x) / len(x) if len(x) > 0 else 0)

x = dataset_df.drop(labels=['label'], axis=1)
y = dataset_df['label'].values

scaler = StandardScaler()
x = scaler.fit_transform(x)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

print("[*] Done!\n\n[*] Training...")
model = utils.stack_classifier()
model = model.fit(x_train, y_train)

print("[*] Done!\n\n[*] Evaluation")
y_pred = model.predict(x_test)
classification_report = classification_report(y_test, y_pred, target_names=labels)
print(classification_report)
