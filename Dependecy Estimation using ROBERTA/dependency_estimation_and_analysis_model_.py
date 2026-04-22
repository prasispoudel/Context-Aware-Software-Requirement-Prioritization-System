# -*- coding: utf-8 -*-
"""Dependency Estimation using RoBerTa (Training Script)
"""

# prompt: import the excel file and put it within a pandas dataframe.

!pip install openpyxl
import pandas as pd

df = pd.read_excel('Combined_Training_Data_Final.xlsx')

df.info()

from transformers import RobertaForSequenceClassification, RobertaTokenizer, TrainingArguments, Trainer

import pandas as pd

df = pd.read_excel('Combined_Training_Data_Final.xlsx')

requirement_pairs = []
requirements = df['Requirement_Text'].tolist()

for i in range(len(requirements)):
    for j in range(i + 1, len(requirements)):
        requirement_pairs.append((requirements[i], requirements[j]))

print(f"Generated {len(requirement_pairs)} unique pairs.")

# Preparing data for classification 

formatted_pairs = []
for req1, req2 in requirement_pairs:
    formatted_pairs.append({'text': f'{req1} [SEP] {req2}'})

print(f"Formatted {len(formatted_pairs)} pairs for RoBERTa input.")

#Preparing training data

training_data = []
requirements = df[['Requirement_Text', 'Is_Leaf_Requirement', 'Is_Root_Requirement']].to_dict('records')

for i in range(len(requirements)):
    for j in range(i + 1, len(requirements)):
        req1 = requirements[i]
        req2 = requirements[j]

        # Infering dependency based on the simplified heuristic
        is_req1_leaf = req1['Is_Leaf_Requirement'] == 1
        is_req1_root = req1['Is_Root_Requirement'] == 1
        is_req2_leaf = req2['Is_Leaf_Requirement'] == 1
        is_req2_root = req2['Is_Root_Requirement'] == 1

        # Heuristic: Label 1 if neither is root and neither is leaf, OR one is root and the other is not a leaf, OR one is a leaf and the other is not a root.
        if (not is_req1_root and not is_req1_leaf and not is_req2_root and not is_req2_leaf) or \
           (is_req1_root and not is_req2_leaf) or \
           (is_req1_leaf and not is_req2_root) or \
           (is_req2_root and not is_req1_leaf) or \
           (is_req2_leaf and not is_req1_root):
            label = 1
        else:
            label = 0


        formatted_pair = {
            'text': f"{req1['Requirement_Text']} [SEP] {req2['Requirement_Text']}",
            'label': label
        }
        training_data.append(formatted_pair)

print(f"Generated {len(training_data)} training pairs.")

# Spliting the training data


from sklearn.model_selection import train_test_split

texts = [pair['text'] for pair in training_data]
labels = [pair['label'] for pair in training_data]

train_texts, val_texts, train_labels, val_labels = train_test_split(
    texts,
    labels,
    test_size=0.2,  # 20% for validation
    random_state=42,
    stratify=labels  # Stratify to maintain class distribution
)

print(f"Training set size: {len(train_texts)}")
print(f"Validation set size: {len(val_texts)}")

# Loading and preparing the roberta model

from transformers import RobertaForSequenceClassification, RobertaTokenizer
import torch

# Loading a pre-trained RoBERTa model and tokenizer
model_name = 'roberta-base'  # Or your fine-tuned model path
tokenizer = RobertaTokenizer.from_pretrained(model_name)

# In binary classification, num_labels should be 2
num_labels = 2 # Binary classification (dependent or not dependent)
model = RobertaForSequenceClassification.from_pretrained(model_name, num_labels=num_labels)

# Creating a custom dataset class
class RequirementDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        # Ensure labels are long
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx]).long()
        return item

    def __len__(self):
        return len(self.labels)

train_encodings = tokenizer(train_texts, truncation=True, padding=True)
val_encodings = tokenizer(val_texts, truncation=True, padding=True)

train_dataset = RequirementDataset(train_encodings, train_labels)
val_dataset = RequirementDataset(val_encodings, val_labels)

print("Data prepared for RoBERTa model.")

# Training the roberta model

# Training arguments
training_args = TrainingArguments(
    output_dir='./results',          # output directory
    num_train_epochs=1,              # number of training epochs
    per_device_train_batch_size=16,  # batch size per device during training
    per_device_eval_batch_size=64,   # batch size for evaluation
    warmup_steps=500,                # number of warmup steps for learning rate scheduler
    weight_decay=0.01,               # strength of weight decay
    logging_dir='./logs',            # directory for storing logs
    logging_steps=10,
    eval_strategy="epoch",     # evaluate each epoch - Corrected parameter name
    save_strategy="epoch",           # Save checkpoint every epoch
    load_best_model_at_end=True,     # Load the best model at the end of training
)

# Initializing the Trainer
trainer = Trainer(
    model=model,                         # the instantiated Transformers model to be trained
    args=training_args,                  # training arguments, defined above
    train_dataset=train_dataset,         # training dataset
    eval_dataset=val_dataset             # evaluation dataset
)

print("Model, Training Arguments, and Trainer initialized.")

# Training the roberta model
trainer.train()

# Evaluatation of the model
eval_results = trainer.evaluate()
print(eval_results)


from google.colab import files

# After training is complete,  we need to save the model and tokenizer locally
model_save_path = "./roberta_dependency_model"
tokenizer_save_path = "./roberta_dependency_tokenizer"

# Finally saving the trained model and tokenizer
trainer.save_model(model_save_path)
tokenizer.save_pretrained(tokenizer_save_path)

print(f"Trained model saved to: {model_save_path}")
print(f"Tokenizer saved to: {tokenizer_save_path}")

print("Downloading model and tokenizer directories...")

# Zip the directories
!zip -r roberta_dependency_model.zip roberta_dependency_model/
!zip -r roberta_dependency_tokenizer.zip roberta_dependency_tokenizer/

# Downloading the zipped files
files.download('roberta_dependency_model.zip')
files.download('roberta_dependency_tokenizer.zip')

