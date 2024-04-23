import sys
import shutil
from pathlib import Path

def validate_arguments():
    program_usage = 'Usage: python merge_datasets.py <dataset_directory>'
    if len(sys.argv) != 2:
        print(program_usage)
        sys.exit(1)         

def modify_label_file(label_file, class_code):
    if class_code == None:
        return

    with open(label_file, 'r') as f:
        label_lines = f.readlines()

    modified_label_lines = []
    for line in label_lines:
        content = line.split()
        content[0] = str(class_code)
        modified_label_lines.append(' '.join(content) + '\n')

    with open(label_file, 'w') as f:
        f.writelines(modified_label_lines)

def main():
    validate_arguments()

    dataset_dir = Path(sys.argv[1]).resolve()

    dataset_labels = {
        'Wheelchair' : 3,
        'Blind' : 4,
        'Suitcase' : 5,
        'Stroller' : 6
    }


    whole_datasets = [
        'Blind',
        'Suitcase',
        'Wheelchair',
        'Child_Elderly_Adult',
        'Stroller'
    ]
    subsets = ['test', 'train', 'valid']
    subdirectories = ['images', 'labels']
    
    # Create the final directory structure
    for dataset_directory in subsets:
        for subdirectory in subdirectories:
            (dataset_dir / dataset_directory / subdirectory).mkdir(parents=True, exist_ok=True)
    
    # Reassign classes
    for dataset in whole_datasets:

        # Set the desired class id
        class_id = None
        if dataset != 'Child_Elderly_Adult':
            class_id = dataset_labels[dataset]
        else:
            class_id = None

        for subset in subsets:
            
            subdirectory = 'labels'
            path = dataset_dir / dataset / subset / subdirectory
            for image_file in path.iterdir():
                modify_label_file(image_file, class_id)


    # Copy or move files
    for dataset in whole_datasets:
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