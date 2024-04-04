import os
import sys
import shutil
from pathlib import Path

class_for_wheelchair = 3
class_for_blind = 4
class_for_suitcase = 5

dataset_dir = os.path.abspath(sys.argv[1])
dataset_parent_directories = ['Blind', 'Suitcase', 'Wheelchair', 'Child_Elderly_Adult']
dataset_directories = ['test', 'train', 'valid']
subdirectories = ['images', 'labels']

if len(sys.argv) != 2:
    print('Usage: python create_dataset.py <dataset_directory>')
    exit(1)


# Consolidate path definitions
train_image_dir = os.path.join(dataset_dir, 'train', 'images')
test_image_dir = os.path.join(dataset_dir, 'test', 'images')
valid_image_dir = os.path.join(dataset_dir, 'valid', 'images')
train_label_dir = os.path.join(dataset_dir, 'train', 'labels')
test_label_dir = os.path.join(dataset_dir, 'test', 'labels')
valid_label_dir = os.path.join(dataset_dir, 'valid', 'labels')

# Create the directory structure
for dataset_directory in dataset_directories:
    for subdirectory in subdirectories:
        path = Path(os.path.join(os.path.join(dataset_dir, dataset_directory), subdirectory))
        path.mkdir(parents=True, exist_ok=True)

for dataset_parent_directory in dataset_parent_directories:
    path = os.path.join(dataset_dir, dataset_parent_directory)

    # enter subdirectory
    subdir = os.listdir(path)
    path = os.path.join(path, subdir[0]) 

    for dataset_directory in dataset_directories:
        new_path = os.path.join(path, dataset_directory)

        image_path = os.path.join(new_path, 'images')
        label_path = os.path.join(new_path, 'labels')        

        # move images to the corresponding directories
        for image in os.listdir(image_path):
            if dataset_directory == 'train':
                os.rename(os.path.join(image_path, image), os.path.join(train_image_dir, image))
            elif dataset_directory == 'test':
                os.rename(os.path.join(image_path, image), os.path.join(test_image_dir, image))
            elif dataset_directory == 'valid':
                os.rename(os.path.join(image_path, image), os.path.join(valid_image_dir, image))

        # reassign the classes and then move them to the corresponding directories
        for label in os.listdir(label_path):
            with open(os.path.join(label_path, label), 'r') as f:
                label_lines = f.readlines()

            modified_label_lines = []
            for line in label_lines:
                content = line.split()
                if dataset_parent_directory == 'Blind':
                    content[0] = str(class_for_blind)
                elif dataset_parent_directory == 'Suitcase':
                    content[0] = str(class_for_suitcase)
                elif dataset_parent_directory == 'Wheelchair':
                    content[0] = str(class_for_wheelchair)
                modified_label_lines.append(' '.join(content) + '\n')

            # reassign the classes
            with open(os.path.join(label_path, label), 'w') as f:
                f.writelines(modified_label_lines)

            # move the labels to the corresponding directories
            if dataset_directory == 'train':
                os.rename(os.path.join(label_path, label), os.path.join(train_label_dir, label))
            elif dataset_directory == 'test':
                os.rename(os.path.join(label_path, label), os.path.join(test_label_dir, label))
            elif dataset_directory == 'valid':
                os.rename(os.path.join(label_path, label), os.path.join(valid_label_dir, label))
    
    # remove the old directories containing the emptited subdirectories
    shutil.rmtree( Path(path).parent )

print('Successfully merged the datasets!')