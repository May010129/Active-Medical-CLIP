from train import SimCLR
import yaml
import argparse
from dataloader.dataset_wrapper import DataSetWrapper
import os
import torch.multiprocessing as mp
import torchvision
import torchvision.transforms as transforms
import torch
import torch.nn as nn
import torch.distributed as dist
from apex.parallel import DistributedDataParallel as DDP
from apex import amp

def main():
    config = yaml.load(open("config.yaml", "r"), Loader=yaml.FullLoader)
    parser = argparse.ArgumentParser(description="node rate: additional command line arguments")
    parser.add_argument("--nr", default= 0, type=int, help="ranking within the nodes 0 or 1")
    args = parser.parse_args()

    if args.nr:
        config['nr'] = args.nr
    print("config loaded.")
    ngpus = torch.cuda.device_count()
    os.environ['MASTER_ADDR'] = 'localhost'              #
    os.environ['MASTER_PORT'] = '8888'
    print("Start to distribute data and model.")  
    mp.spawn(train, nprocs=ngpus, args=(ngpus, config))
    

def train(gpu, ngpu, config):
    # 设置当前使用的GPU
    torch.cuda.set_device(gpu)
    rank = config['nr'] * config['gpus'] + gpu	  
    config['rank'] = rank                        
    dist.init_process_group(                                   
    	backend='nccl',                                         
   		init_method='env://',                                   
    	world_size=config['world_size'],                              
    	rank=rank                                               
    )
    config['gpu'] = gpu
    print('load dataset')
    dataset = DataSetWrapper(config['batch_size'], **config['dataset'])
    simclr = SimCLR(dataset, config)
    simclr.train()

if __name__ == "__main__":
    main()
