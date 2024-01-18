from train import SimCLR
import yaml
from dataloader.dataset_wrapper import DataSetWrapper

def main():
    print('load config')
    config = yaml.load(open("config.yaml", "r"), Loader=yaml.FullLoader)

    print('load dataset')
    dataset = DataSetWrapper(config['batch_size'], **config['dataset'])
    print('dataset loaded')

    print('start training')
    simclr = SimCLR(dataset, config)
    simclr.train()


if __name__ == "__main__":
    main()
