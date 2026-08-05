from datasets import load_dataset

from dataset_registry import DATASETS


class DatasetManager:

    def __init__(self):

        self.datasets = DATASETS

    def list_datasets(self):

        print("=" * 50)

        print("Available Datasets")

        print("=" * 50)

        for name in self.datasets:

            print(name)

    def get_dataset(self, name):

        return self.datasets[name]

if __name__ == "__main__":

    manager = DatasetManager()

    manager.list_datasets()

    