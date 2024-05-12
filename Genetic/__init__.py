from population import Population
from network import FeedForwardNetwork, Genome
from config import load_config
from pickle import dump, load


def save_genome(genome : Genome, path : str):
    with open(path,"wb") as f:
        dump(genome, f)

def load_genome(path : str) -> Genome:
    with open(path,"rb") as f:
        return load(f)

    