from genetic.utility import is_number, is_int

def read_config(path, destination_config = None) -> dict:
    config = {}

    with open(path, "r") as config_file:
        lines = config_file.readlines()
        for line in lines:
            
            # Skip comments and empty lines
            if line[0] == "[": continue
            elif line == "\n": continue

            # Unpack key, value pairs
            key, value = line.split(" ")

            # Strip newline characters
            value = value.replace("\n",'')
            
            # Interpret datatypes
            if is_number(value):
                if is_int(float(value)) : value = int(value)
                else: value = float(value)

            if destination_config:
                destination_config[key] = value
            else:
                config[key] = value

    if destination_config: return
    return config

default_config = read_config("genetic/default_config.txt")

def load_config(path : str) -> dict:
    new_config = default_config.copy()
    read_config(path,new_config)
    return new_config

# Testing
if __name__ == "__main__":
    print("\nGENERATE CONFIG FROM default_config.txt")
    config = read_config("default_config.txt")
    print(config)

    print("\nUPDATE CONFIG")
    original = {"this" : 1, "is" : 2, "a" : 3, "test" : 4}
    print('Original')
    print(original)

    print("\nUpdated")
    read_config("default_config.txt", original)
    print(original)