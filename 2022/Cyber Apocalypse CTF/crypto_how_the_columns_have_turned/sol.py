from numpy import block


max_key = 820394623162117 - 1

keys = [0,0,0,0,729513912306026]

ciphers = [
    b'VEOAOTNRDCEEIFHIVHMVOETYDEDTESTHTCHLSRPDAIYAATOSTEGIIIOCIPYLTNOTLRTRNLEEUNBEOSFNANDHTUFTEETREEEEOEDHNRNYA',
    b'AAVPDESEETURAFFDUCEDAEECNEMOROCEANHPTTGROITCYSSSETTSKTTRLRIUAVSONOISECNJISAFAATAPATWORIRCETYUIPUEEHHAIHOG',
    b'NABPSVKELHRIALDVEHLORCNNOERUNGTAEEEHEHDORLIEEAOTITUTEAUEARTEFISESGTAYAGBTHCEOTWLSNTWECESHHBEIOYPNCOLICCAF',
    b'NIRYHFTOSSNPECMPNWSHFSNUTCAGOOAOTGOITRAEREPEEPWLHIPTAPEOOHPNSKTSAATETTPSIUIUOORSLEOAITEDFNDUHSNHENSESNADR',
    b'NUTFAUPNKROEOGNONSRSUWFAFDDSAAEDAIFAYNEGYSGIMMYTAANSUOEMROTRROUIIOODLOIRERVTAMNITAHIDNHRENIFTCTNLYLOTFINE'
]

def deriveKey(key):
    derived_key = []

    for i, char in enumerate(key):
        previous_letters = key[:i]
        new_number = 1
        for j, previous_char in enumerate(previous_letters):
            if previous_char > char:
                derived_key[j] += 1
            else:
                new_number += 1
        derived_key.append(new_number)
    return derived_key


def transpose(array):
    return [row for row in map(list, zip(*array))]


def flatten(array):
    return "".join([chr(i) for sub in array for i in sub])

def decrypt(ct, key_len):
    b_nums = len(ct) // key_len
    
    blocks = [ct[i:i + b_nums] for i in range(0, len(ct), b_nums)]
    pt = [blocks[i][::-1] for i in range(key_len)]
    pt = transpose(pt)
    #print(pt)
    return flatten(pt)

def decrypt2(ct, key):
    key_len = len(key)
    b_nums = len(ct) // key_len

    derived_key = deriveKey(key)
    
    blocks = [ct[i:i + b_nums] for i in range(0, len(ct), b_nums)]
    pt = [blocks[derived_key[i]-1][::-1] for i in range(key_len)]
    pt = transpose(pt)
    return flatten(pt)

def twistedColumnarEncrypt(pt, key):
    derived_key = deriveKey(key)

    width = len(key)

    blocks = [pt[i:i + width] for i in range(0, len(pt), width)]
    blocks = transpose(blocks)

    ct = [blocks[derived_key.index(i + 1)][::-1] for i in range(width)]
    ct = flatten(ct)
    return ct

[print(decrypt2(c,str(keys[-1]))) for c in ciphers]

#HTB{THELCGISVULNERABLEWENEEDTOCHANGEIT}
