#!/usr/bin/env python3

import sqlite3
import subprocess

conn = sqlite3.connect('blockchain.db')
names = "(hash, confirmations, size, height, version, merkleroot, mint, MoneySupply, time, nonce, bits, difficulty, blocktrust, " \
        "chaintrust, previousblockhash, nextblockhash, flags, proofhash, entropybit, modifier, modifierchecksum, tx, " \
        "CPID, ProjectName, RAC, NetworkRAC, RSAWeight, Magnitude, LastPaymentTime, ResearchSubsidy, ResearchAge, " \
        "ResearchMagnitudeUnit, ResearchAverageMagnitude, LastPORBlockHash, Interest, GRCAddress, ClientVersion, " \
        "CPIDv2, CPIDValid, NeuralHash, IsSuperBlock, IsContract) "

vals = "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, " \
       "?, ?, ?, ?, ?, ?, ?, ?, ?) "
sql_insert = "INSERT INTO block VALUES " + vals

sqlite3.register_adapter(bool, int)
sqlite3.register_converter("BOOLEAN", lambda v: bool(int(v)))
sql_create = '''
CREATE TABLE IF NOT EXISTS block (
     hash TEXT UNIQUE,
     confirmations INTEGER,
     size INTEGER,
     height INTEGER PRIMARY KEY,
     version INTEGER,
     merkleroot TEXT,
     mint REAL,
     MoneySupply INTEGER,
     time INTEGER,
     nonce INTEGER,
     bits TEXT,
     difficulty REAL,
     blocktrust TEXT,
     chaintrust TEXT,
     previousblockhash TEXT UNIQUE,
     nextblockhash TEXT UNIQUE,
     flags TEXT,
     proofhash TEXT,
     entropybit INTEGER,
     modifier TEXT,
     modifierchecksum TEXT,
     tx TEXT,
     CPID TEXT,
     ProjectName TEXT,
     RAC REAL,
     NetworkRAC REAL,
     RSAWeight REAL,
     Magnitude REAL,
     LastPaymentTime TEXT,
     ResearchSubsidy REAL,
     ResearchAge REAL,
     ResearchMagnitudeUnit REAL,
     ResearchAverageMagnitude REAL,
     LastPORBlockHash TEXT,
     Interest REAL,
     GRCAddress TEXT,
     BoincPublicKey TEXT,
     BoincSignature TEXT,
     SignatureValid BOOLEAN,
     ClientVersion TEXT,
     CPIDv2 TEXT,
     CPIDValid BOOLEAN,
     NeuralHash TEXT,
     IsSuperBlock INTEGER,
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
    item["hash"] = block[0]
    item["confirmations"] = block[1]
    item["size"] = block[2]
    item["height"] = block[3]
    item["version"] = block[4]
    item["merkleroot"] = block[5]
    item["mint"] = block[6]
    item["MoneySupply"] = block[7]
    item["time"] = block[8]
    item["nonce"] = block[9]
    item["bits"] = block[10]
    item["difficulty"] = block[11]
    item["blocktrust"] = block[12]
    item["chaintrust"] = block[13]
    item["previousblockhash"] = block[14]
    item["nextblockhash"] = block[15]
    item["flags"] = block[16]
    item["proofhash"] = block[17]
    item["entropybit"] = block[18]
    item["modifier"] = block[19]
    item["modifierchecksum"] = block[20]
    item["tx"] = block[21]
    item["CPID"] = block[22]
    item["ProjectName"] = block[23]
    item["RAC"] = block[24]
    item["NetworkRAC"] = block[25]
    item["RSAWeight"] = block[26]
    item["Magnitude"] = block[27]
    item["LastPaymentTime"] = block[28]
    item["ResearchSubsidy"] = block[29]
    item["ResearchMagnitudeUnit"] = block[30]
    item["ResearchAverageMagnitude"] = block[31]
    item["LastPORBlockHash"] = block[32]
    item["Interest"] = block[33]
    item["GRCAddress"] = block[34]
    item["BoincPublicKey"] = block[35]
    item["BoincSignature"] = block[36]
    item["SignatureValid"] = block[37]
    item["ClientVersion"] = block[38]
    item["CPIDv2"] = block[39]
    item["CPIDValid"] = block[40]
    item["NeuralHash"] = block[41]
    item["IsSuperBlock"] = block[42]
    item["IsContract"] = block[43]
    return item


def getTuple(block: dict):
    if "BoincSignature" not in block:
        block["BoincSignature"] = None
    if "SignatureValid" not in block:
        block["SignatureValid"] = None
    if "BoincPublicKey" not in block:
        block["BoincPublicKey"] = None
    if "CPIDv2" not in block:
        block["CPIDv2"] = None
    if "ProjectName" not in block:
        block["ProjectName"] = None
    if "RAC" not in block:
        block["RAC"] = None
    if "NetworkRAC" not in block:
        block["NetworkRAC"] = None
    if "RSAWeight" not in block:
        block["RSAWeight"] = None
    if "RSAWeight" not in block:
        block["RSAWeight"] = None
    if "ResearchSubsidy" not in block:
        block["ResearchSubsidy"] = None
    if "ResearchAge" not in block:
        block["ResearchAge"] = None
    if "ResearchMagnitudeUnit" not in block:
        block["ResearchMagnitudeUnit"] = None
    if "ResearchAverageMagnitude" not in block:
        block["ResearchAverageMagnitude"] = None
    if "MoneySupply" not in block:
        block["MoneySupply"] = None

    block["tx"] = str(block["tx"])

    return (block["hash"], block["confirmations"], block["size"], block["height"], block["version"],
            block["merkleroot"], block["mint"], block["MoneySupply"], block["time"], block["nonce"], block["bits"],
            block["difficulty"], block["blocktrust"], block["chaintrust"], block["previousblockhash"],
            block["nextblockhash"], block["flags"], block["proofhash"], block["entropybit"], block["modifier"],
            block["modifierchecksum"], block["tx"], block["CPID"], block["ProjectName"], block["RAC"],
            block["NetworkRAC"], block["RSAWeight"], block["Magnitude"], block["LastPaymentTime"],
            block["ResearchSubsidy"], block["ResearchAge"], block["ResearchMagnitudeUnit"],
            block["ResearchAverageMagnitude"], block["LastPORBlockHash"], block["Interest"], block["GRCAddress"],
            block["BoincPublicKey"], block["BoincSignature"], block["SignatureValid"], block["ClientVersion"],
            block["CPIDv2"], block["CPIDValid"], block["NeuralHash"], block["IsSuperBlock"], block["IsContract"])


def pipe_eval(pipe: bytes):
    return eval(str(pipe, encoding="utf-8").replace("true", "True").replace("false", "False"))


def get_last_block_id():
    p1 = subprocess.Popen(["gridcoinresearchd", "getblockcount"], stdout=subprocess.PIPE)
    return p1.communicate()[0]


def getblockhash(index: int):
    p1 = subprocess.Popen(["gridcoinresearchd", "getblockhash", str(index)], stdout=subprocess.PIPE)
    return str(p1.communicate()[0], encoding="utf-8")


def getblock(hash_val: str):
    p1 = subprocess.Popen(["gridcoinresearchd", "getblock", hash_val], stdout=subprocess.PIPE)
    return pipe_eval(p1.communicate()[0])


def sql_block_by_hash(hash_val: str):
    elem = conn.execute('SELECT * FROM block WHERE hash=?', (hash_val,)).fetchone()
    return getDict(elem)


def sql_block_by_height(height):
    elem = conn.execute('SELECT * FROM block WHERE height=?', (height,)).fetchone()
    return getDict(elem)


def sql_has_block_hash(hash_val: str):
    elem = len(conn.execute('SELECT * FROM block WHERE hash=?', (hash_val,)).fetchall())
    return elem == 1


def do_insert(hash_val: str):
    currentblock = getblock(hash_val)

    if not sql_has_block_hash(currentblock["hash"]):
        if "nextblockhash" in currentblock:
            blocks.append(getTuple(currentblock))
            print("Block n°", currentblock["height"])
        if len(blocks) == 100:
            print("Insert")
            insertMany(blocks)
            blocks.clear()
        if "nextblockhash" in currentblock:
            return currentblock["nextblockhash"]
    return None


def insert(hash_val: str):
    next_hash = do_insert(hash_val)
    while next_hash is not None:
        next_hash = do_insert(next_hash)


def check_db():
    hash_list = conn.execute('''SELECT nextblockhash FROM block WHERE nextblockhash NOT IN
    (SELECT hash FROM block)''').fetchall()
    for h in hash_list:
        insert(h[0])


def sync_database():
    print("Sync...")
    hash = getblockhash(1)
    insert(hash)
    print("Checking integrity...")
    check_db()


if __name__ == '__main__':
    sync_database()
