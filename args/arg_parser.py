import argparse
import util


class ArgParser(object):
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Population-Based Training')
        self.parser.add_argument('--gpu_ids', type=str, default='0',
                                 help='Comma-separated list of GPUs to use.')
        self.parser.add_argument('--batch_size', type=int, default=32, help='Batch size.')
        self.parser.add_argument('--num_workers', type=int, default=4, help='Number of workers per data loader.')
        self.parser.add_argument('--num_epochs', type=int, default=30,
                                 help='Number of epochs to train for. If 0, train forever.')
        self.parser.add_argument('--population_size', type=int, default=3,
                                 help='Number of models in a population.')
        self.parser.add_argument('--dataset', type=str, default='CIFAR10', choices=('CIFAR10',),
                                 help='Dataset to train on.')
        self.parser.add_argument('--ckpt_dir', type=str, default='ckpts/',
                                 help='Directory to save checkpoints and population info.')
        self.parser.add_argument('--name', type=str, required=True, help='Experiment name.')
        self.parser.add_argument('--model', type=str, default='resnet50', help='Model name.')
        self.parser.add_argument('--metric_name', type=str, default='val_loss',
                                 help='Metric to optimize during PBT. Make sure to also set --maximize_metric')
        self.parser.add_argument('--maximize_metric', type=util.str_to_bool, default=False,
                                 help='If true, maximize the metric. Else minimize.')
        self.parser.add_argument('--max_eval', type=int, default=1000,
                                 help='Max number of examples to evaluate from the training set.')
        self.parser.add_argument('--max_ckpts', type=int, default=3,
                                 help='Max number of recent checkpoints to keep per model.')
        self.parser.add_argument('--save_dir', type=str, default='logs', help='Directory for saving logs.')
        self.parser.add_argument('--learning_rate', type=float, default=1e-1, help='Initial learning rate.')
        self.parser.add_argument('--optimizer', type=str, default='sgd', choices=('sgd', 'adam'), help='Optimizer.')
        self.parser.add_argument('--sgd_momentum', type=float, default=0.9, help='SGD momentum (SGD only).')
        self.parser.add_argument('--sgd_dampening', type=float, default=0.9, help='SGD momentum (SGD only).')
        self.parser.add_argument('--adam_beta_1', type=float, default=0.9, help='Adam beta 1 (Adam only).')
        self.parser.add_argument('--adam_beta_2', type=float, default=0.999, help='Adam beta 2 (Adam only).')
        self.parser.add_argument('--weight_decay', type=float, default=5e-4,
                                 help='Weight decay (i.e., L2 regularization factor).')
        self.parser.add_argument('--iters_per_print', type=int, default=4,
                                 help='Number of iterations between printing loss to the console and TensorBoard.')
        self.parser.add_argument('--search_space', type=str, default='lr,momentum,weight_decay')

    def parse_args(self):
        args = self.parser.parse_args()
        args.gpu_ids = [int(i) for i in str(args.gpu_ids).split(',') if int(i) >= 0]
        args.device = 'cpu' if len(args.gpu_ids) == 0 else 'cuda:{}'.format(args.gpu_ids[0])
        args.search_space = str(args.search_space).split(',')

        return args
