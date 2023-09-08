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
benign_folder_path = "Datasets/Stateless/Benign"
benign_files_list = utils.list_files_in_folder(benign_folder_path)

for file in benign_files_list:
    file_df = pd.read_csv(file)
    file_df['label'] = 0
    dataset_df = pd.concat([dataset_df, file_df], ignore_index=True)

# Load attack datasets
labels.append('malicious')
malicious_folder_path = "Datasets/Stateless/Attacks"
malicious_files_list = utils.list_files_in_folder(malicious_folder_path)

for file in malicious_files_list:
    file_df = pd.read_csv(file)
    file_df['label'] = 1
    dataset_df = pd.concat([dataset_df, file_df], ignore_index=True)

print("[*] Done!\n\n[*]Processing datasets...")
dataset_df = shuffle(dataset_df)
dataset_df = dataset_df.drop(labels=['timestamp'], axis=1)
dataset_df = dataset_df.fillna(0)

label_encoder = LabelEncoder()
dataset_df['longest_word'] = label_encoder.fit_transform(dataset_df['longest_word'].astype(str))
dataset_df['sld'] = label_encoder.fit_transform(dataset_df['sld'].astype(str))

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
