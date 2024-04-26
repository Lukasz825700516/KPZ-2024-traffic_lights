import os
import argparse
from typing import Dict
import dotenv

def parse_arguments():
    parser = argparse.ArgumentParser(
        prog='train',
        description='The script trains the YOLO model placing artifacts as weights and results the proper places.'
    )

    parser.add_argument('-l', '--location', choices=["remote", "local"], help="Specify whether to train remotely or locally.", default="local")
    
    return parser.parse_args()

def remove_non_yolo_arguments(all_args):
    project_specific_args = [
        'location'
    ]

    all_args = vars(all_args)
    yolo_args = { arg_name: arg_value for arg_name, arg_value in all_args.items() if arg_name not in project_specific_args }
        
    return yolo_args

def train_locally(yolo_args: Dict[str, str]):
    print("Training locally")
    # pass yolo args to command
    # save with an appropriate framework

def train_remotely(yolo_args: Dict[str, str]):
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
            train_locally(yolo_args)

        case "remote":
            train_remotely(yolo_args)
    

if __name__ == '__main__':
    main()
    

