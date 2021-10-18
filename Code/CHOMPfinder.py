import os
dirname = os.path.dirname(__file__)


CHOMP = {
    "[0]": {"nim": 0, "moves": []},
    "[1]": {"nim": 0, "moves": []},

} # A dict of board states and their Nim values

CONDENSED_ZEROS = []

def make_key(key):
    ###
    # Takes a key list and converts it to a hashable string to store in thje CHOMP dict
    ###
    return str(key)

def get_key(keystring):
    ###
    # Takes a string of a chomp board and converts it to its equivlent list
	# Starts as string and returns an array
    ###
    keystring = keystring [1:-1] # trim off quote marks
    key = []
    key = keystring.split(", ") # strip commas and spaces, this may only work for single digit strings
    for i in range(0, len(key), 1):
        key[i] = int(key[i])
    return key

def get_children(seed):
    ###
    # Takes a seed list and returns all of its direct children in a list
    ###
    key = make_key(seed) # makes kid hashable
    if not(key in CHOMP):
        CHOMP[key] = {"nim": "IDK", "moves": []}
    if CHOMP[key]["moves"] == []:
        kindergarden = [] # container for children
        for col in reversed(range(len(seed))):  #go over list backwards, hitting each stack
            for height in range(seed[col], -1, -1): #look at board if we remove top peices of current stack
                left = seed[0:col]
                if height != 0:
                    left.append(height)
                right= seed[col+1:]
                for i in range(0, len(right), 1):
                    if right[i] > height:
                        right[i] = height
                    if right[i] != 0:
                        left.append(right[i])
                if left != []:
                    kindergarden.append(left)
        i = 0
        while(i<len(kindergarden)):
            if(kindergarden[i]==seed):
                kindergarden.remove(kindergarden[i])
            else:
                i+=1
        CHOMP[key]["moves"] = kindergarden
    return CHOMP[key]["moves"]

def check_nim_or_add(kid):
    ###
    # Check the Nim value of a key in CHOMP, if no value exists for key, add a dumby value
    # then, if the nim value for the key is None (or not found) return -1, else return the nim value
    ###
    key = make_key(kid) # makes kid hashable
    if not(key in CHOMP):
        # CHOMP[key] = {"nim": "IDK", "moves": []}
        CHOMP[key] = {"nim": "IDK", "moves": []}
    if CHOMP[key]["nim"] == "IDK":
        find_child_nim(kid)
    return CHOMP[key]["nim"]

def find_child_nim(seed):
    ###
    # Recursive function that takes a list and returns its Nim value if it has been found, otherwise it finds it
    ###
    seedKindergarden = get_children(seed)
    MEXlist = []
    for child in seedKindergarden:
        childNim = check_nim_or_add(child)
        if childNim != -1:
            MEXlist.append(childNim)
        else:
            find_child_nim(child)
    nim = get_MEX(MEXlist)
    seedKey = make_key(seed)
    if not(seedKey in CHOMP):
        CHOMP[seedKey] = {"nim": "IDK", "moves": []}
        # CHOMP[seedKey] = {"nim": "IDK"}
    CHOMP[seedKey]["nim"] = int(nim)

def get_MEX(MEXlist):
    ###
    # Takes a list and returns the minimun excluded value
    ###
    nList = set(MEXlist)
    mex = 0
    while mex in nList:
        mex += 1
    return mex

def clean_print(dict):
    filename = os.path.join(dirname, "Clean_print.txt")
    f = open(filename, "w")
    for k, v in dict.items():
        # print(k, v)
        f.write("Key: ")
        f.write(k)
        f.write("\n")
        f.write(str(v))
        f.write("\n")
        f.write("\n")

def zero_print(dict):
    filename = os.path.join(dirname, "zero_print.txt")
    f = open(filename, "w")
    for k, v in dict.items():
        if v["nim"] == 0:
            CONDENSED_ZEROS.append(print_condensed(get_key(k)))
            f.write(k)
            f.write("\n")

def zero_print_no_twos(dict):
    filename = os.path.join(dirname, "zero_print_no_twos.txt")
    f = open(filename, "w")
    for k, v in dict.items():
        if v["nim"] == 0:
            key = get_key(k)
            if key[0] == 3:
                f.write(k)
                f.write(str(print_condensed(key)))
                f.write("\n")
                # print(k)

def print_condensed(listele):
    holding = []
    for i in reversed(range(3)):
        i+=1
        holding.append(listele.count(i))
        i-=1
    return holding

def write_condensed(CONDENSED_ZEROS):
    filename = os.path.join(dirname, "condensed_list_size.txt")
    f = open(filename, "w")
    CONDENSED_ZEROS = sorted(CONDENSED_ZEROS, key = lambda x: (x[0] + x[1] + x[2]))
    # CONDENSED_ZEROS = sorted(CONDENSED_ZEROS, key = lambda x: ( x[2], x[0], x[1]))
    for i in CONDENSED_ZEROS:
        f.write(str(i))
        f.write("\n")
    # g = open("C:\\Users\Ezra\Box\Summer Research 2020\Ezra's Stuff\condensed_list_size_1_2_3.txt", "w")
    # # CONDENSED_ZEROS = sorted(CONDENSED_ZEROS, key = lambda x: (x[0] + x[1] + x[2]))
    # CONDENSED_ZEROS = sorted(CONDENSED_ZEROS, key = lambda x: (x[0] + x[1] + x[2], x[2], x[1], x[0]))
    # # CONDENSED_ZEROS = sorted(CONDENSED_ZEROS, key = lambda x: ( x[2], x[0], x[1]))
    # for j in CONDENSED_ZEROS:
    #     g.write(str(j))
    #     g.write("\n")
    # h = open("C:\\Users\Ezra\Box\Summer Research 2020\Ezra's Stuff\condensed_list_size_3_1_2.txt", "w")
    # # CONDENSED_ZEROS = sorted(CONDENSED_ZEROS, key = lambda x: (x[0] + x[1] + x[2]))
    # CONDENSED_ZEROS = sorted(CONDENSED_ZEROS, key = lambda x: (x[0] + x[1] + x[2], x[2], x[0], x[1]))
    # # CONDENSED_ZEROS = sorted(CONDENSED_ZEROS, key = lambda x: ( x[2], x[0], x[1]))
    # for k in CONDENSED_ZEROS:
    #     h.write(str(k))
    #     h.write("\n")

def main() :
    seed = []
    for i in range(30):
        seed.append(3)
    # for i in range(10):
    #     seed.append(1)
    print("Finding Children.")
    find_child_nim(seed)
    print("Printing.")
    clean_print(CHOMP)
    zero_print(CHOMP)
    zero_print_no_twos(CHOMP)
    write_condensed(CONDENSED_ZEROS)
    print("Done!")
main()
