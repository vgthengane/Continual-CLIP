
import os
import json
import yaml

from omegaconf import DictConfig, OmegaConf



def get_class_order(file_name: str) -> list:
    r"""TO BE DOCUMENTED"""
    with open(file_name, "r+") as f:
        data = yaml.safe_load(f)
        return data["class_order"]


def get_class_ids_per_task(args):
    yield args.class_order[:args.initial_increment]
    for i in range(args.initial_increment, len(args.class_order), args.increment):
        yield args.class_order[i:i + args.increment]

def get_class_names(classes_names, class_ids_per_task):
    return [classes_names[class_id] for class_id in class_ids_per_task]


def get_dataset_class_names(workdir, dataset_name, long=False):
    with open(os.path.join(workdir, "dataset_reqs", f"{dataset_name}_classes.txt"), "r") as f:
        lines = f.read().splitlines()
    return [line.split("\t")[-1] for line in lines]


def save_config(config: DictConfig) -> None:
    OmegaConf.save(config, "config.yaml")


def get_workdir(path):
    split_path = path.split("/")
    workdir_idx = split_path.index("Continual-CLIP")
    return "/".join(split_path[:workdir_idx+1])


