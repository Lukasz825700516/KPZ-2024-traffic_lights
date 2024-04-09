import sys
import shutil
from pathlib import Path
import itertools
import os

class_for_wheelchair = 3
class_for_blind = 4
class_for_suitcase = 5

def authenticate_kaggle():
    authentication_data = '{"username":"helmutedgarson","key":"3fb6889f0a2de29194b0f271716c8d56"}'

    kaggle_json_path = os.path.expanduser('~/.kaggle/kaggle.json')

    os.makedirs(os.path.dirname(kaggle_json_path), exist_ok=True)

    with open(kaggle_json_path, 'w') as file:
        file.write(authentication_data)


def download_kaggle_datasets():

    import auth_kaggle

    auth_kaggle.authenticate_kaggle()

    import kaggle
    from kaggle.api.kaggle_api_extended import KaggleApi


    dataset_directory = Path('./Datasets')

    api = KaggleApi()
    api.authenticate()
    
    datasets = {
        "Blind" : "jangbyeonghui/visually-impairedwhitecane",
        "Suitcase" : "dataclusterlabs/suitcaseluggage-dataset",
    }


    for dataset_name, dataset_url in datasets.items():
        api.dataset_download_files(dataset_url, path=dataset_directory/dataset_name, unzip=True)


def download_roboflow_datasets():
    key = '96bccdb6-5fd7-4947-9335-2feaef52dbcd'
    download_location = './Datasets'
    format = 'yolov8'
    datasets = {
        'Stroller' : 'thales-a5kye/stroller_final/dataset/3',
        'Child_Elderly_Adult' : 'gist-awllb/dl-bhh3b/dataset/4',
        'Wheelchair' : 'obj-detection-gmggm/objectdetect-iga7u'
    }

    commands = [
        f'Use this secret key: {key}',
        'roboflow login',
    ]

    for dataset_name, dataset_url in datasets.items():
        commands.append(f'roboflow download -f {format} -l {download_location}/{dataset_name} {dataset_url}')

    os.system(' && '.join(commands))


def validate_arguments():
    program_usage = 'Usage: python create_dataset.py <dataset_directory> <copy_instead_move>=True'
    available_options = [''.join(x) for x in itertools.product(['', 'copy_instead_move='], ['True', 'False', 'true', 'false', '1', '0']) ]
    if len(sys.argv) not in (2, 3):
        print(program_usage)
        sys.exit(1)         
    if len(sys.argv) == 3 and sys.argv[2] not in available_options:
        print(itertools.product(['', 'copy_instead_move='], ['True', 'False', 'true', 'false', '1', '0']))
        print(program_usage)
        sys.exit(1)

def copy_or_move_files(src_dir, dest_dir, copy_instead_move):
    if copy_instead_move:
        shutil.copy(src_dir, dest_dir)
    else:
        shutil.move(src_dir, dest_dir)

def modify_label_file(label_file, class_code):
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

    download_kaggle_datasets()
    download_roboflow_datasets()

    dataset_dir = Path(sys.argv[1]).resolve()
    copy_instead_move = len(sys.argv) == 3 and (sys.argv[2] in ('True', 'true', '1', 'copy_instead_move=True', 'copy_instead_move=true'))

    dataset_parent_directories = ['Blind', 'Suitcase', 'Wheelchair', 'Child_Elderly_Adult']
    dataset_directories = ['test', 'train', 'valid']
    subdirectories = ['images', 'labels']

    # Create directory structure
    for dataset_directory in dataset_directories:
        for subdirectory in subdirectories:
            (dataset_dir / dataset_directory / subdirectory).mkdir(parents=True, exist_ok=True)

    for dataset_parent_directory in dataset_parent_directories:
        parent_dir = dataset_dir / dataset_parent_directory
        sub_dir = next(iter(parent_dir.iterdir()))

        for dataset_directory in dataset_directories:
            new_path = sub_dir / dataset_directory
            image_dir = new_path / 'images'
            label_dir = new_path / 'labels'

            for image_file in image_dir.iterdir(): # TODO: fix these paths...
                dest_dir = dataset_dir / dataset_directory / 'images' / image_file.name
                copy_or_move_files(image_file, dest_dir, copy_instead_move)

            for label_file in label_dir.iterdir():
                if dataset_parent_directory == 'Blind':
                    modify_label_file(label_file, class_for_blind)
                elif dataset_parent_directory == 'Suitcase':
                    modify_label_file(label_file, class_for_suitcase)
                elif dataset_parent_directory == 'Wheelchair':
                    modify_label_file(label_file, class_for_wheelchair)

                dest_dir = dataset_dir / dataset_directory / 'labels' / label_file.name
                copy_or_move_files(label_file, dest_dir, copy_instead_move)

        if not copy_instead_move:
            shutil.rmtree(sub_dir.parent)
            print(f"Removing directory {sub_dir.parent} with all its contents.")

    print('Successfully merged the datasets!')

if __name__ == "__main__":
    main()
