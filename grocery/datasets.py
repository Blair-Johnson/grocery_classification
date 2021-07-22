import os
from os.path import isfile, join

class Combined:
    """Class for constructing and storing the path-label mappings for the 
        combined Grocery-Product-Classification and GroceryStoreDatasets

        ...

        Attributes:
            GPC_path : str
                root path to Grocery-Product-Classification repository
            GSD_path : str
                root path to GroceryStoreDataset repository
            dataset : dict
                Dictionary containing the {path:label} mappings for the tf.data
                API
            labels : set
                Union of sets of labels from each dataset
            GPC_map : dict
                Dictionary of {path:label} mappings for the GPC dataset
            GSD_map : dict
                Dictionary of {path:label} mappings for the GSD dataset
            GPC_labels : set
                Set of labels for the GPC dataset
            GSD_labels : set 
                Set of labels for the GSD dataset
    """
        
    def __init__(self, GPC_root_path: str, GSD_root_path: str):
        """Args:
            GPC_root_path : str
                String path to the Grocery-Product-Classification dataset from
                GitHub:
                https://github.com/abhinavsagar/Grocery-Product-Classification.git
            GSD_root_path : str
                String path to the GrocerStoreDataset repository from GitHub:
                https://github.com/marcusklasson/GroceryStoreDataset.git
        """
        self.GPC_path = GPC_root_path
        self.GSD_path = GSD_root_path
        self.GPC_labels = set()
        self.GSD_labels = set()
        self.GPC_map = {}
        self.GSD_map = {}
        self.__parse_and_combine()

    def __parse_GPC_paths(self):
        for dir_path, dir_names, _ in os.walk(self.GPC_path):
            for label in [label for label in dir_names if label.isupper()]:
                self.GPC_labels.add(label.lower())
                for class_path, _, image_paths in os.walk(join(dir_path,
                label)):
                    for path in image_paths:
                        self.GPC_map[join(class_path, path)] = label.lower()

    def __parse_GSD_paths(self):
        # This is atrocious but it works
        included_splits = ['train', 'test', 'val']
        categories = ['Fruit', 'Packages', 'Vegetables']
        sub_paths = [join(join(self.GSD_path, 'dataset'), split) for split in
                    included_splits] 
        for sub_path in sub_paths:
            for category_path in [join(sub_path, category) for category in categories]:
                for _, labels, _ in os.walk(category_path):
                    for label in labels:
                        self.GSD_labels.add(label.lower())
                        for label_path, sub_labels, images in os.walk(join(category_path,
                                                                        label)): 
                            for image in images:
                                self.GSD_map[join(label_path, image)] = label.lower()
                            for sub_label in sub_labels:
                                for sub_label_path, _, subimages in os.walk(join(
                                                            label_path, sub_label)):
                                    for subimage in subimages:
                                        self.GSD_map[join(sub_label_path,
                                        subimage)] = label.lower()

    def __parse_and_combine(self):
        self.__parse_GPC_paths()
        self.__parse_GSD_paths()
        self.labels = self.GPC_labels.union(self.GSD_labels)
        self.dataset = self.GPC_map.copy()
        self.dataset.update(self.GSD_map)
