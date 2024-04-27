import os
import argparse
from typing import Dict
import dotenv
import pathlib
import subprocess
import mlflow
from ultralytics import settings

def print_warning(text: str) -> None:
    print("\033[93m{}\033[0m".format(text))
    

def parse_arguments():
    parser = argparse.ArgumentParser(
        prog='train',
        description='The script trains the YOLO model placing artifacts as weights and results in the proper locations.'
    )

    parser.add_argument('-e', '--epochs', default=0, type=int, help="Set the number of training epochs. It overrides the default behaviour (value of `0`), which is training ended when no improvement occurs within 10 epochs.", )
    parser.add_argument('-m', '--memory', help='Defines the maximum allowed memory allocation on GPU. 0 means dynamic. If an error occurs such as "torch.cuda.OutOfMemoryError: CUDA out of memory.", decrease this value.', default=0, type=int)
    parser.add_argument('-g', '--goal', choices=['transfer-learning', 'fine-tuning', 'from-scratch'], default="transfer-learning", help='Choose whether to train all layers (learning-from-scratch), a few last layers (transfer-learning) or the very last layer (fine-tuning).')    
    parser.add_argument('-l', '--location', choices=["remote", "local"], help="Specify whether to train remotely or locally.", default="local")
    parser.add_argument('-t', '--task', choices=['classify', 'detect'], help="Determine whether to train the model for classification or object detection.")
        
    parser.add_argument('-d', '--data', type=pathlib.Path, required=True, help="The path to the data.yaml file, which defines a dataset structure.")
    parser.add_argument('-v', '--verbose', type=bool, default=False, help="Specifies if training should print a lot of details (True) or minimum (False).")
    
    return parser.parse_args()
    

def remove_non_yolo_arguments(all_args):
    project_specific_args = [
        'location',
        'goal',
        'memory',
        'task'
    ]

    all_args = vars(all_args)
    yolo_args = { arg_name: arg_value for arg_name, arg_value in all_args.items() if arg_name not in project_specific_args }
        
    return yolo_args

def train_locally(yolo_args: Dict[str, str], goal: str, memory: str, task: str):
    print("Training locally")
    settings.update({'mlflow': True})
        
    exit_code = subprocess.run(['which', 'yolo'], env=os.environ).returncode
    if exit_code != 0:
        print_warning('It looks like your you do NOT have `yolo` in your path. Install it and/or enter the proper virtual environment.')
    
    preset_args = {
        'patience': 10,
        'device': 0, # enforce GPU instead of CPU
        'epochs': 9999 if yolo_args["epochs"] == 0 else yolo_args["epochs"], # train until no improvment is found
        'plots': True,
        'project': f'{task}-with-yolo-{goal}'
    }
    
    match goal:
        case 'transfer-learning':
            preset_args['freeze'] = "19"

        case 'fine-tuning':
            preset_args['freeze'] = "22"

        case 'from-scratch':
            pass
            
        case _:
            print(f"Invalid value of the parameter 'goal', which is '{goal}'")
            exit(1)

    if memory == 0:
        preset_args["batch"] = -1  # enable dynamic memory allocation on GPU
    else:
        images_per_gb = 16
        preset_args["batch"] = memory * images_per_gb
        
    yolo_args = {**yolo_args, **preset_args}
    
    args = ' '
    for key, value in yolo_args.items():
        value = str(value)
        args += f'{key}={value} '

    training_command = f'yolo {task} train {args}'
    print("Command:", training_command)
    os.system(training_command)

def train_remotely(yolo_args: Dict[str, str], goal: str, memory: str, task: str):
    print("Training remotely")
    credentials = dotenv.dotenv_values(".env")
    # upload dataset if not exists
    # send training command
    # download artifacts
    # save artifacts to the proper server/locally in repo

def main():
    args = parse_arguments()
    yolo_args = remove_non_yolo_arguments(args) 

    match args.location:
        case "local": 
            train_locally(yolo_args, args.goal, args.memory, args.task)

        case "remote":
            train_remotely(yolo_args, args.goal, args.memory, args.task)
    

if __name__ == '__main__':
    main()
    

