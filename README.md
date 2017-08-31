# Gridcoin Misc Scripts

Misc Scripts for or related to [Gridcoin](gridcoin.us).

### Setup:

- You need python3.4 or higher to launch the script. Lower version of python should work also but I didn't try it.
- You don't need to launch the script in the Gridcoin installation folder. 
- You have to launch the Gridcoin daemon if you want to sync the database

### Getting Started:

#### Sync the database

```python
[...]

def sync_database():
    print("Sync...")
    nb = get_last_block_id()
    hash = get_hash_by_block_id(nb)
    handle_insert(hash)
    print("Checking integrity...")
    check_db()

    
if __name__ == '__main__':
    sync_database()

```

Running the script directly will sync the database. *sync_database()* fetch the latest blocks from the client to the database. *check_db()* will verify if some parts of the database is missing and fetch it.

The script can be stopped at any moment without any trouble.  *check_db()* should handle theses interruptions. 

#### Fetch information from the database

*database.db* should be in the same folder as your script. The database is made with sqlite3. [**Sqlite3 Documentation**](https://docs.python.org/3.5/library/sqlite3.html).

```python
def sql_block_by_hash(hash_val: str):
    elem = conn.execute('SELECT * FROM block WHERE hash=?', (hash_val,)).fetchone()
    return getDict(elem)
  
block = sql_block_by_hash('04c43c3c801737c2b5e7f65c316ee5d60c636a810df12518e8b96c267841e96cc38d0478288fd892b3c74fe79b659f4ff33c53c4cd69064ee7949c097b68fdf9b6')
print(block)
```

This code below is fetching a block in the database. A dict fetched by the sql table should have this look :

```python
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
```



**Buy me a Gridcoin Coffe ? S5u3bTUxmfraYoYJ367dP7hhhJvR7jR274**