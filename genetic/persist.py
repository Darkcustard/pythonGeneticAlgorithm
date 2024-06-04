from genetic.network import Genome

def save_genome(genome : Genome, path : str):
    print(f"Saving best Genome to: {path}")
    with open(path,"wb") as f:
        dump(genome, f)

def load_genome(path : str) -> Genome:
    with open(path,"rb") as f:
        return load(f)