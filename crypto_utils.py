import pickle

def dump(o):
    return pickle.dumps(o).hex()

def load(o):
    return pickle.loads(bytearray.fromhex(o))

