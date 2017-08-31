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

sqlite3.register_adapter(bool, int)
sqlite3.register_converter("BOOLEAN", lambda v: bool(int(v)))
sql_create = '''
CREATE TABLE IF NOT EXISTS block (
     nextblockhash INTEGER,
     ResearchAverageMagnitude REAL,
     ClientVersion TEXT,
     size INTEGER,
     BoincSignature TEXT,
     proofhash TEXT,
     blocktrust TEXT,
     IsSuperBlock INTEGER,
     chaintrust TEXT,
     Magnitude REAL,
     ResearchSubsidy REAL,
     CPIDv2 TEXT,
     merkleroot TEXT,
     previousblockhash TEXT,
     tx TEXT,
     time INTEGER,
     Interest REAL,
     version INTEGER,
     ResearchMagnitudeUnit REAL,
     nonce INTEGER,
     SignatureValid BOOLEAN,
     BoincPublicKey TEXT,
     hash TEXT,
     confirmations INTEGER,
     mint REAL,
     CPID TEXT,
     bits TEXT,
     modifierchecksum TEXT,
     modifier TEXT,
     difficulty REAL,
     NeuralHash TEXT,
     entropybit INTEGER,
     LastPORBlockHash TEXT,
     GRCAddress TEXT,
     flags TEXT,
     ResearchAge REAL,
     CPIDValid BOOLEAN,
     height INTEGER PRIMARY KEY,
     LastPaymentTime TEXT,
     IsContract INTEGER
);'''
conn.execute(sql_create)
blocks = list()


def insertToBDD(item: tuple):
    try:
        conn.execute(sql_insert, item)
        conn.commit()
    except Exception as e:
        print(e)


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
    p = str(pipe, encoding="utf-8").replace("true", "True").replace("false", "False")
    return eval(str(pipe, encoding="utf-8").replace("true", "True").replace("false", "False"))


def get_last_block_id():
    p1 = subprocess.Popen(["gridcoinresearchd", "getblockcount"], stdout=subprocess.PIPE)
    return p1.communicate()[0]


def repairwallet():
    p1 = subprocess.Popen(["gridcoinresearchd", "repairwallet"], stdout=subprocess.PIPE)
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


def validBlock(currentblock):
    if currentblock["hash"] == "None":
        return False
    if currentblock["previousblockhash"] == "None":
        return False

    return True


def do_insert(hash_val: str):
    currentblock = get_block_by_hash(hash_val)
    while not validBlock(currentblock):
        print("Not a validblock, recalling client")
        currentblock = get_block_by_hash(hash_val)

    if not sql_has_block(currentblock["height"]):
        if "nextblockhash" in currentblock:
            insertToBDD(getTuple(currentblock))
            print("Block n°", currentblock["height"])
        return currentblock["previousblockhash"]
    return None


def do_better_insert(hash_val: bytes):
    currentblock = get_block_by_hash(hash_val)
    while not validBlock(currentblock):
        print("Not a validblock, recalling client")
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


if __name__ == '__main__':
    sync_database()
