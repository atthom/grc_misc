import json
import sqlite3

import subprocess

conn = sqlite3.connect('blockchain.db')

names = "(nextblockhash, ResearchAverageMagnitude, ClientVersion, size, BoincSignature, proofhash, blocktrust, " \
        "IsSuperBlock, chaintrust, Magnitude, ResearchSubsidy, CPIDv2, merkleroot, previousblockhash, tx, time, " \
        "Interest, version, ResearchMagnitudeUnit, nonce, SignatureValid, BoincPublicKey, hash, confirmations, mint, " \
        "CPID, bits, modifierchecksum, modifier, difficulty, NeuralHash, entropybit,  LastPORBlockHash, GRCAddress, " \
        "flags, ResearchAge, CPIDValid, height, LastPaymentTime, IsContract) "
# 40

vals = "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, " \
       "?, ?, ?, ?) "
sql_insert = "INSERT INTO block VALUES " + vals


def insertToBDD(item: tuple):
    try:
        conn.execute(sql_insert, item)
        conn.commit()
    except:
        pass


def insertMany(tuples):
    try:
        conn.executemany(sql_insert, tuples)
        conn.commit()
    except:
        for tupl in tuples:
            insertToBDD(tupl)


def getDict(block: tuple):
    item = dict()
    item["nextblockhash"] = block[0]
    item["ResearchAverageMagnitude"] = block[1]
    item["ClientVersion"] = block[2]
    item["size"] = block[3]
    item["BoincSignature"] = block[4]
    item["proofhash"] = block[5]
    item["blocktrust"] = block[6]
    item["IsSuperBlock"] = block[7]
    item["chaintrust"] = block[8]
    item["Magnitude"] = block[9]
    item["ResearchSubsidy"] = block[10]
    item["CPIDv2"] = block[11]
    item["merkleroot"] = block[12]
    item["previousblockhash"] = block[13]
    item["tx"] = block[14]
    item["time"] = block[15]
    item["Interest"] = block[16]
    item["version"] = block[17]
    item["ResearchMagnitudeUnit"] = block[18]
    item["nonce"] = block[19]
    item["SignatureValid"] = block[20]
    item["hash"] = block[21]
    item["BoincPublicKey"] = block[22]
    item["confirmations"] = block[23]
    item["mint"] = block[24]
    item["CPID"] = block[25]
    item["bits"] = block[26]
    item["modifierchecksum"] = block[27]
    item["modifier"] = block[28]
    item["difficulty"] = block[29]
    item["NeuralHash"] = block[30]
    item["entropybit"] = block[31]
    item["LastPORBlockHash"] = block[32]
    item["GRCAddress"] = block[33]
    item["flags"] = block[34]
    item["ResearchAge"] = block[35]
    item["CPIDValid"] = block[36]
    item["height"] = block[37]
    item["LastPaymentTime"] = block[38]
    item["IsContract"] = block[39]

    return item


def getTuple(block: dict):
    if "BoincSignature" not in block:
        boincSign = "None"
    else:
        boincSign = block["BoincSignature"]

    if "SignatureValid" not in block:
        SignatureValid = "None"
    else:
        SignatureValid = block["SignatureValid"]

    if "BoincPublicKey" not in block:
        BoincPublicKey = "None"
    else:
        BoincPublicKey = block["BoincPublicKey"]

    if "CPIDv2" not in block:
        CPIDv2 = "None"
    else:
        CPIDv2 = block["CPIDv2"]

    if "previousblockhash" not in block and block["height"] == 0:
        previousblockhash = "None"
    else:
        previousblockhash = block["previousblockhash"]

    return (block["nextblockhash"], block["ResearchAverageMagnitude"], block["ClientVersion"], block["size"], boincSign,
            block["proofhash"], block["blocktrust"], block["IsSuperBlock"], block["chaintrust"], block["Magnitude"],
            block["ResearchSubsidy"], CPIDv2, block["merkleroot"], previousblockhash, str(block["tx"]),
            block["time"], block["Interest"], block["version"], block["ResearchMagnitudeUnit"], block["nonce"],
            SignatureValid, BoincPublicKey, block["hash"], block["confirmations"], block["mint"], block["CPID"],
            block["bits"], block["modifierchecksum"], block["modifier"], block["difficulty"], block["NeuralHash"],
            block["entropybit"], block["LastPORBlockHash"], block["GRCAddress"], block["flags"], block["ResearchAge"],
            block["CPIDValid"], block["height"], block["LastPaymentTime"], block["IsContract"])


def pipe_eval(pipe: bytes):
    return eval(str(pipe, encoding="utf-8").replace("true", "True").replace("false", "False"))


def get_last_block_id():
    p1 = subprocess.Popen(["gridcoinresearchd", "getblockcount"], stdout=subprocess.PIPE)
    return p1.communicate()[0]


def get_hash_by_block_id(nb):
    p1 = subprocess.Popen(["gridcoinresearchd", "getblockhash", nb], stdout=subprocess.PIPE)
    return p1.communicate()[0]


def get_block_by_hash(hash_val):
    p1 = subprocess.Popen(["gridcoinresearchd", "getblock", hash_val], stdout=subprocess.PIPE)
    return pipe_eval(p1.communicate()[0])


def sql_block_by_hash(hash_val: str):
    elem = conn.execute('SELECT * FROM block WHERE hash=?', (hash_val,)).fetchone()
    return getDict(elem)


def sql_block_by_height(height):
    elem = conn.execute('SELECT * FROM block WHERE height=?', (height,)).fetchone()
    return getDict(elem)


def sql_has_block(height):
    elem = len(conn.execute('SELECT * FROM block WHERE height=?', (height,)).fetchall())
    return elem == 1


def sql_has_block_hash(hash_val: str):
    elem = len(conn.execute('SELECT * FROM block WHERE hash=?', (hash_val,)).fetchall())
    return elem == 1


def do_insert(hash_val: str):
    currentblock = get_block_by_hash(hash_val)

    if not sql_has_block(currentblock["height"]):
        if "nextblockhash" in currentblock:
            insertToBDD(getTuple(currentblock))
            print("Block n°", currentblock["height"])
        return currentblock["previousblockhash"]
    return None


blocks = list()


def do_better_insert(hash_val: str):
    currentblock = get_block_by_hash(hash_val)

    if not sql_has_block(currentblock["height"]):
        if "nextblockhash" in currentblock:
            blocks.append(getTuple(currentblock))
            print("Block n°", currentblock["height"])
        if len(blocks) == 100:
            print("Insert")
            insertMany(blocks)
            blocks.clear()
        if "previousblockhash" in currentblock:
            return currentblock["previousblockhash"]
    return None


def handle_insert(hash_val: bytes):
    next_hash = do_better_insert(hash_val)
    while next_hash is not None:
        next_hash = do_better_insert(next_hash)


def check_db():
    hash_list = conn.execute('''SELECT previousblockhash FROM block WHERE previousblockhash NOT IN
    (SELECT hash FROM block)''').fetchall()
    for h in hash_list:
        print(h)
        handle_insert(h[0])


def sync_database():
    print("Sync...")
    nb = get_last_block_id()
    hash = get_hash_by_block_id(nb)
    handle_insert(hash)
    print("Checking integrity...")
    check_db()


p1 = subprocess.Popen(["gridcoinresearchd", "list", "network"], stdout=subprocess.PIPE)
print(str(p1.communicate()[0], encoding="utf-8"))

"""

A dict fetched by the sql table should have this look :
(take care that the order is not garanteed)
    {
        'BoincPublicKey': '075ce33a17eac7a513dd3afd5ce6f4b49f1c28e7e2473a525b6b6f51c674bb1a',
        'BoincSignature': 'MEQCIA3gIgcVHE8rdFbWbGFUbwFLGmh/3+qBK2IQjXcw+jseAiAL7If7N9GfMijDUfkq0uDOd7bCQJd0yzZfgQlcXDwCEg==',
        'CPID': '8cfe9864e18db32a334b7de997f5a4f2',
        'CPIDValid': 1,
        'CPIDv2': '8cfe9864e18db32a334b7de997f5a4f2',
        'ClientVersion': 'v3.5.8.4-g-research',
        'GRCAddress': 'SCZE6pX79dCU5eXb5Q5fUMmNKAG9Tsrvmf',
        'Interest': 0.11,
        'IsContract': 0,
        'IsSuperBlock': 0,
        'LastPORBlockHash': 'c7a1fef6c02ceea32efdd04d89931dabf42aebe42a79de90b5a324ba36d49649',
        'LastPaymentTime': '01-24-2017 22:10:40',
        'Magnitude': 90.0,
        'NeuralHash': '',
        'ResearchAge': 0.270556,
        'ResearchAverageMagnitude': 90.0,
        'ResearchMagnitudeUnit': 0.225,
        'ResearchSubsidy': 5.48,
        'SignatureValid': 0,
        'bits': '1c08c713',
        'blocktrust': '1d2a3fc900',
        'chaintrust': '73e0f0cf86557b2bb40f58d5b9d39693c2c893c4fe568da696164ea677f8121',
        'confirmations': 195218,
        'difficulty': 29.16459076,
        'entropybit': 0,
        'flags': 'proof-of-stake proof-of-research',
        'hash': '04c43c3c801737c2b5e7f65c316ee5d60c636a810df12518e8b96c267841e96cc38d0478288fd892b3c74fe79b659f4ff33c53c4cd69064ee7949c097b68fdf9b6',
        'height': 799744,
        'merkleroot': '6176180bb6d047c8ba092f8591310006aea17b966290fc3bc54caea6116302d1',
        'mint': 5.58970124,
        'modifier': '350aa02f555a3b84',
        'modifierchecksum': '0530a51f',
        'nextblockhash': 'a9b34f9bc5094ff8e0470213e1e978d23934f45e24aa4682a865d34bcad47812',
        'nonce': 307465,
        'previousblockhash': 'a2f66b374af57bd16b29c44f2e0797e69b21f38d265f7ae63346d75b7ceda623',
        'proofhash': '00000244d7badcca070de90352f0579bbad08f65c9f1d64410a0e06f588d0228',
        'size': 1198,
        'time': 1485319360,
        'tx': "['2a40e543f970d48d9d04fec7c9ca78e946daba375fbfb5ed92bf5e182803b510', "
              "'ac8774c6648dfb224832b18965b5f80d12885375421836b6047abc135c282eb6']",
        'version': 7
    }

"""
