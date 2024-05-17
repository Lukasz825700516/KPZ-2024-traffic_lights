'''
    The script to train YOLO8n model and logs results to MLFlow.
'''

import sys
import pathlib
import argparse
from typing import Dict
import mlflow
from ultralytics import YOLO
import dotenv
import os

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
    yolo_args = {
        arg_name: arg_value
        for arg_name, arg_value in all_args.items()
        if arg_name not in project_specific_args
    }

    return yolo_args


def save_results(hyperparameters: Dict[str, str], model, metrics, results, task: str, goal: str) -> None:
    dotenv.load_dotenv()
    credentials = os.environ['MLFLOW_CREDENTIALS']
    host = 'ml.lukaszm.xyz'
    port = '80'
    mlflow.set_tracking_uri(uri=f'https://{credentials}@{host}:{port}')

    mlflow.set_experiment(f'yolo-{task}')
    with mlflow.start_run():

        mlflow.set_tag('Goal', goal)
        signature = mlflow.infer_signature(hyperparameters['data'], results)

        for key, value in metrics.results_dict.items():
            mlflow.log_metric(key, value)

        mlflow.log_params(hyperparameters)
        mlflow.log_param("ap_class_index", metrics.ap_class_index.tolist())
        mlflow.log_param("curves", metrics.curves)
        mlflow.log_param("names", metrics.names)
        mlflow.log_param("plot", metrics.plot)
        mlflow.log_param("speed", metrics.speed)
        mlflow.log_param("task", metrics.task)

        mlflow.pytorch.log_model(
            pytorch_model=model,
            artifact_path='last_run/',
            signature=signature,
            registered_model_name='YOLO8n',
        )
     

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

    save_results(yolo_args, model, metrics, results, task, goal)


def main():
    args = parse_arguments()
    yolo_args = remove_non_yolo_arguments(args)
    train_locally(yolo_args, args.goal, args.memory, args.task)

if __name__ == '__main__':
    main()
