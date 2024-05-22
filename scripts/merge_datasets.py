import sys
import shutil
from pathlib import Path
from pandas import read_csv
from DatasetLabel import DatasetLabel

def validate_arguments():
    program_usage = 'Usage: python merge_datasets.py <dataset_directory> <path_to_dataset_version>'
    if len(sys.argv) != 3:
        print(program_usage)
        sys.exit(1)         

def modify_label_file(label_file, dataset, dataset_labels: DatasetLabel):
    with open(label_file, 'r') as f:
        label_lines = f.readlines()

    modified_label_lines = []
    for line in label_lines:
        content = line.split()
        new_label = str(dataset_labels.get_valid_id_class(dataset, content[0]))
        if (new_label != '-1'):
            content[0] = new_label
            modified_label_lines.append(' '.join(content) + '\n')
        else:
            continue

    with open(label_file, 'w') as f:
        f.writelines(modified_label_lines)

def main():
    validate_arguments()

    dataset_dir = Path(sys.argv[1]).resolve()
    dataset_version = read_csv(Path(sys.argv[2]).resolve(), sep=';')
    dataset_labels = DatasetLabel(str(Path(sys.argv[2]).resolve()))
    
    whole_datasets = dataset_version['dataset_dir']
    subsets = ['test', 'train', 'valid']
    subdirectories = ['images', 'labels']
    
    # Create the final directory structure
    for dataset_directory in subsets:
        for subdirectory in subdirectories:
            (dataset_dir / dataset_directory / subdirectory).mkdir(parents=True, exist_ok=True)
    
    # Reassign classes
    for dataset in whole_datasets:
        print("Reasigning labels in dataset '" + str(dataset) + "' ...", end=" ")
        for subset in subsets:
            
            subdirectory = 'labels'
            path = dataset_dir / dataset / subset / subdirectory
            for image_file in path.iterdir():
                modify_label_file(image_file, dataset, dataset_labels)


    # Copy or move files
    for dataset in whole_datasets:
        print("Merging dataset '" + str(dataset) + "' ...", end=" ")
        for subset in subsets:
            
            for subdirectory in subdirectories:
                src_dir = dataset_dir / dataset / subset / subdirectory
                dest_dir = dataset_dir / subset / subdirectory

                for image_file in src_dir.iterdir():
                    shutil.copy(image_file, dest_dir)

    # Delete the temporary directories
    for dataset in whole_datasets:
        shutil.rmtree(dataset_dir / dataset)

    print('Successfully merged the datasets!')

if __name__ == "__main__":
    main()
