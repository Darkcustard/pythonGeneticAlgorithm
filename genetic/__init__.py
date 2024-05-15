from genetic.population import Population
from genetic.network import FeedForwardNetwork, Genome
from genetic.config import load_config
from pickle import dump, load


def save_genome(genome : Genome, path : str):
    print(f"Saving best Genome to: {path}")
    with open(path,"wb") as f:
        dump(genome, f)

def load_genome(path : str) -> Genome:
    with open(path,"rb") as f:
        return load(f)

    