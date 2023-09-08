import os
from sklearn.ensemble import StackingClassifier, RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier

def list_files_in_folder(folder_path):
    file_list = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".csv"):
                file_path = os.path.join(root, file)
                file_list.append(file_path)
    return file_list

def stack_classifier():
    base_model = []
    base_model.append(('RF', RandomForestClassifier(n_estimators=100, random_state=42, max_depth=15, n_jobs=-1)))
    base_model.append(('DT', DecisionTreeClassifier(random_state=42, max_depth=15)))

    meta_learner = MLPClassifier(hidden_layer_sizes=(100), activation='relu', max_iter=500, learning_rate='invscaling')

    model = StackingClassifier(estimators=base_model, final_estimator=meta_learner, cv=5)
    return model
