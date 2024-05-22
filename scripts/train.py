'''
    The script to train YOLO8n model and logs results to MLFlow.
'''

import sys
import pathlib
import argparse
from typing import Dict
from ultralytics import YOLO
import dotenv
import os
import tempfile

import ultralytics

def print_warning(text: str) -> None:
    print(f'\033[93m{text}\033[0m')

def print_error_and_exit(text: str) -> None:
    print(f'\033[93m{text}\033[0m')
    sys.exit(1)

def parse_arguments():
    parser = argparse.ArgumentParser(
        prog='train',
        description='The script trains the YOLO model and send artifacts to MLFlow.'
    )

    parser.add_argument('-e', '--epochs', default=0, type=int, help="Set the number of training epochs. It overrides the default behaviour (value of `0`), which is training ended when no improvement occurs within 10 epochs.", )
    parser.add_argument('-m', '--memory', help='Defines the maximum allowed memory allocation on GPU. 0 means dynamic. If an error occurs such as "torch.cuda.OutOfMemoryError: CUDA out of memory.", decrease this value.', default=0, type=int)
    parser.add_argument('-g', '--goal', choices=['transfer-learning', 'fine-tuning', 'from-scratch'], default="transfer-learning", help='Choose whether to train all layers (learning-from-scratch), a few last layers (transfer-learning) or the very last layer (fine-tuning).')
    parser.add_argument('-t', '--task', choices=['classify', 'detect'], help="Determine whether to train the model for classification or object detection.")
        
    parser.add_argument('-V', '--version', type=str, required=True, help="The version of dataset in use.")
    parser.add_argument('-d', '--data', type=pathlib.Path, required=True, help="The path to the data.yaml file, which defines a dataset structure.")
    parser.add_argument('-v', '--verbose', type=bool, default=False, help="Specifies if training should print a lot of details (True) or minimum (False).")
    parser.add_argument('-p', '--project', type=pathlib.Path, default=tempfile.mkdtemp(), help="Specifies where artifacts should be saved. Defaults to tempdir")
    
    return parser.parse_args()   

def remove_non_yolo_arguments(all_args):
    project_specific_args = [
        'location',
        'goal',
        'memory',
        'task',
        'version'
    ]

    all_args = vars(all_args)
    yolo_args = {
        arg_name: arg_value
        for arg_name, arg_value in all_args.items()
        if arg_name not in project_specific_args
    }

    return yolo_args


def train_locally(yolo_args: Dict[str, str], goal: str, memory: str, task: str):
    print("Training locally")
        
    preset_args = {
        'patience': 10,
        'device': 0, # enforce GPU instead of CPU
        'epochs': 9999 if yolo_args["epochs"] == 0 else yolo_args["epochs"], # train until no improvment is found
        'plots': True
    }

    del yolo_args['epochs'] # already used in preset_args

    match goal:
        case 'transfer-learning':
            preset_args['freeze'] = 19

        case 'fine-tuning':
            preset_args['freeze'] = 22

        case 'from-scratch':
            pass
            
        case _:
            print_error_and_exit(f"Invalid value of the parameter 'goal', which is '{goal}'")

    if memory == 0:
        preset_args["batch"] = -1  # enable dynamic memory allocation on GPU
    else:
        images_per_gb = 16
        preset_args["batch"] = memory * images_per_gb

    yolo_args = {**yolo_args, **preset_args}

    model = YOLO('yolov8n.pt')
    results = model.train(**yolo_args)
    metrics = model.val(data=yolo_args['data'])

def main():
    dotenv.load_dotenv()
    credentials = os.environ['MLFLOW_CREDENTIALS']
    host = 'ml.lukaszm.xyz'

    ultralytics.settings.update({'mlflow': True})
    os.environ['MLFLOW_EXPERIMENT_NAME'] = 'yolo-None'
    os.environ['MLFLOW_TRACKING_URI'] = f'https://{credentials}@{host}'

    args = parse_arguments()
    yolo_args = remove_non_yolo_arguments(args)
    train_locally(yolo_args, args.goal, args.memory, args.task)

if __name__ == '__main__':
    main()
