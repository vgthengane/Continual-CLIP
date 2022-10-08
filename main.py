
import os
import json
import hydra
import logging
from omegaconf import DictConfig

import torch
import statistics
from torch.utils.data import DataLoader
from continuum.metrics import Logger

from continual_clip import utils
from continual_clip.models import load_model
from continual_clip.datasets import build_cl_scenarios


@hydra.main(config_path=None, config_name=None, version_base="1.1") 
def continual_clip(cfg: DictConfig) -> None:

    cfg.workdir = utils.get_workdir(path=os.getcwd())
    cfg.dataset_root = os.path.join(cfg.workdir, cfg.dataset_root)

    utils.save_config(cfg)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    cfg.class_order = utils.get_class_order(os.path.join(cfg.workdir, cfg.class_order))
    model  = load_model(cfg, device)
    eval_dataset, classes_names = build_cl_scenarios(
        cfg, is_train=False, transforms=model.transforms
    )
    model.classes_names = classes_names

    with open(cfg.log_path, 'w+') as f: 
        pass

    acc_list = []
    metric_logger = Logger(list_subsets=["test"])
    for task_id, _ in enumerate(eval_dataset):
        logging.info(f"Evaluation for task {task_id} has started.")
        model.adaptation(task_id)

        eval_loader = DataLoader(eval_dataset[:task_id + 1], batch_size=cfg.batch_size)
        for inputs, targets, task_ids in eval_loader:
            inputs, targets = inputs.to(device), targets.to(device)
            outputs = model(inputs)
            metric_logger.add([outputs.cpu().argmax(dim=1), targets.cpu(), task_ids], subset="test")

        acc_list.append(100 * metric_logger.accuracy)
        with open(cfg.log_path, 'a+') as f:
            f.write(json.dumps({
                'task': task_id,
                'acc': round(100 * metric_logger.accuracy, 2),
                'avg_acc': round(100 * metric_logger.average_incremental_accuracy, 2),
                'forgetting': round(100 * metric_logger.forgetting, 6),
                'acc_per_task': [round(100 * acc_t, 2) for acc_t in metric_logger.accuracy_per_task],
                'bwt': round(100 * metric_logger.backward_transfer, 2),
                'fwt': round(100 * metric_logger.forward_transfer, 2),
            }) + '\n')
            metric_logger.end_task()

    with open(cfg.log_path, 'a+') as f:
        f.write(json.dumps({
            'last': round(acc_list[-1], 2), 
            'avg': round(statistics.mean(acc_list), 2)
        }) + '\n')

        

















if __name__ == "__main__":
    continual_clip()