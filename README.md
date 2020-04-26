# Blockchain extractor

Blockchain extractor is a Python program which extracts all Bitcoin blockchain data using Bitcoin Core.  
It aims at providing the purest dataset thanks to a transparent collection method, limiting processing between ground truth and the output.  
It collects data at application level using RPC (Remote Procedure Call) to request Bitcoin Core and writes a line corresponding to a full block JSON response.

## Getting Started

### Built With

* [Bitcoin](https://bitcoin.org/) - Bitcoin is an innovative payment network and a new kind of money.
* [Pypy](https://www.pypy.org/) - A fast, compliant alternative implementation of Python.

### Prerequisites

You need an access to a [Bitcoin Core](https://bitcoin.org/en/download) full node with a synchronized blockchain.  
Follow this [tutorial](https://bitcoin.org/en/full-node).  
Configure your bitcoin.conf file to allow Remote Procedure Call :
```sh
server=1 # Enabled Remote Procedure Call
rpcport=8332 # Default RPC port
rpcbind=NodeIpBinding # Remove this option if you are in localhost
rpcallowip=IpAcceptedForRPC # Remove this option if you are in localhost
rpcuser=BitcoinUser # Needed for RPC Auth
rpcpassword=BitcoinPassword # Needed for RPC Auth
```

### Installing

Clone this repository and install dependencies using pip3 :
```sh
pip3 install configparser
pip3 install requests
```

### Running
Edit **config.ini** :
```ini
[Bitcoin]
Url = http://127.0.0.1:8332/ # Node ip and port
RpcUser = BitcoinUser # RPC user
RpcPassword = BitcoinPassword # RPC password
```

This code runs faster with Pypy :
```sh
nohup pypy3 blockchain-extractor.py 2> blockchain.err | gzip -c > blockchain.gz &
```
The output file size for blockchain.gz is close to **500 GB**, with a collection duration close to **32 hours**.  

## Documentation
### Processing
Get the **last block** :
```sh
zcat blockchain.gz | head -n1
```

Get the **first block** also called **genesis** :
```sh
zcat blockchain.gz | tail -n1
```

### Result
[Bitcoin core : GetBlock](https://bitcoin.org/en/developer-reference#getblock)  
[Bitcoin core : GetRawTransaction](https://bitcoin.org/en/developer-reference#getrawtransaction)

**Each line of the output file contains a full JSON block like below :**
```sh
{
  "hash" : "hash",     (string) the block hash (same as provided)
  "confirmations" : n,   (numeric) The number of confirmations, or -1 if the block is not on the main chain
  "size" : n,            (numeric) The block size
  "strippedsize" : n,    (numeric) The block size excluding witness data
  "weight" : n           (numeric) The block weight as defined in BIP 141
  "height" : n,          (numeric) The block height or index
  "version" : n,         (numeric) The block version
  "versionHex" : "00000000", (string) The block version formatted in hexadecimal
  "merkleroot" : "xxxx", (string) The merkle root
  "tx" : [               (array of json objects) Transactions description
    {
      "txid": "id",     (string) The transaction id (same as provided)
      "hash": "id",     (string) The transaction hash (differs from txid for witness transactions)
      "version": n,     (numeric) The version
      "size": n,        (numeric) The serialized transaction size
      "vsize": n,       (numeric) The virtual transaction size (differs from size for witness transactions)
      "weight": n,      (numeric) The transaction weight (between vsize*4-3 and vsize*4)
      "locktime" : ttt, (numeric) The lock time
      "vin": [          (array of json objects)
        {
          "txid": "id",                 (string) The transaction id
          "vout": n,                    (numeric)
          "scriptSig": {                (json object) The script
            "asm": "asm",               (string) asm
            "hex": "hex"                (string) hex
          },
          "sequence": n                 (numeric) The script sequence number
          "txinwitness": ["hex", ...]   (array of string) hex-encoded witness data (if any)
        },...
      ],
      "vout": [     (array of json objects)
        {
          "value": x.xxx,           (numeric) The value in BTC
          "n": n,                   (numeric) index
          "scriptPubKey": {         (json object)
            "asm": "asm",           (string) the asm
            "hex": "hex",           (string) the hex
            "reqSigs" : n,          (numeric) The required sigs (if any)
            "type": "pubkeyhash"    (string) The type, eg 'pubkeyhash'
            "addresses" : [         (json array of string)
                "address"           (string) bitcoin address
                ,...
            ]
          }
        }
      ],
      "hex" : "data",               (string) The serialized, hex-encoded data for 'txid'
    },...
  ],
  "time" : ttt,                 (numeric) The block time in seconds since epoch (Jan 1 1970 GMT)
  "mediantime" : ttt,           (numeric) The median block time in seconds since epoch (Jan 1 1970 GMT)
  "nonce" : n,                  (numeric) The nonce
  "bits" : "1d00ffff",          (string) The bits
  "difficulty" : x.xxx,         (numeric) The difficulty
  "chainwork" : "xxxx",         (string) Expected number of hashes required to produce the chain up to this block (in hex)
  "nTx" : n,                    (numeric) The number of transactions in the block.
  "previousblockhash" : "hash", (string) The hash of the previous block
  "nextblockhash" : "hash"      (string) The hash of the next block
}
```

### [Block 170](https://blockstream.info/block/00000000d1145790a8694403d4063f323d499e655c83426834d4ce2f8dd4a2ee) example

```json
{
  "hash": "00000000d1145790a8694403d4063f323d499e655c83426834d4ce2f8dd4a2ee",
  "confirmations": 627543,
  "strippedsize": 490,
  "size": 490,
  "weight": 1960,
  "height": 170,
  "version": 1,
  "versionHex": "00000001",
  "merkleroot": "7dac2c5666815c17a3b36427de37bb9d2e2c5ccec3f8633eb91a4205cb4c10ff",
  "tx": [
    {
      "txid": "b1fea52486ce0c62bb442b530a3f0132b826c74e473d1f2c220bfa78111c5082",
      "hash": "b1fea52486ce0c62bb442b530a3f0132b826c74e473d1f2c220bfa78111c5082",
      "version": 1,
      "size": 134,
      "vsize": 134,
      "weight": 536,
      "locktime": 0,
      "vin": [
        {
          "coinbase": "04ffff001d0102",
          "sequence": 4294967295
        }
      ],
      "vout": [
        {
          "value": 50.00000000,
          "n": 0,
          "scriptPubKey": {
            "asm": "04d46c4968bde02899d2aa0963367c7a6ce34eec332b32e42e5f3407e052d64ac625da6f0718e7b302140434bd725706957c092db53805b821a85b23a7ac61725b OP_CHECKSIG",
            "hex": "4104d46c4968bde02899d2aa0963367c7a6ce34eec332b32e42e5f3407e052d64ac625da6f0718e7b302140434bd725706957c092db53805b821a85b23a7ac61725bac",
            "type": "pubkey"
          }
        }
      ],
      "hex": "01000000010000000000000000000000000000000000000000000000000000000000000000ffffffff0704ffff001d0102ffffffff0100f2052a01000000434104d46c4968bde02899d2aa0963367c7a6ce34eec332b32e42e5f3407e052d64ac625da6f0718e7b302140434bd725706957c092db53805b821a85b23a7ac61725bac00000000"
    },
    {
      "txid": "f4184fc596403b9d638783cf57adfe4c75c605f6356fbc91338530e9831e9e16",
      "hash": "f4184fc596403b9d638783cf57adfe4c75c605f6356fbc91338530e9831e9e16",
      "version": 1,
      "size": 275,
      "vsize": 275,
      "weight": 1100,
      "locktime": 0,
      "vin": [
        {
          "txid": "0437cd7f8525ceed2324359c2d0ba26006d92d856a9c20fa0241106ee5a597c9",
          "vout": 0,
          "scriptSig": {
            "asm": "304402204e45e16932b8af514961a1d3a1a25fdf3f4f7732e9d624c6c61548ab5fb8cd410220181522ec8eca07de4860a4acdd12909d831cc56cbbac4622082221a8768d1d09[ALL]",
            "hex": "47304402204e45e16932b8af514961a1d3a1a25fdf3f4f7732e9d624c6c61548ab5fb8cd410220181522ec8eca07de4860a4acdd12909d831cc56cbbac4622082221a8768d1d0901"
          },
          "sequence": 4294967295
        }
      ],
      "vout": [
        {
          "value": 10.00000000,
          "n": 0,
          "scriptPubKey": {
            "asm": "04ae1a62fe09c5f51b13905f07f06b99a2f7159b2225f374cd378d71302fa28414e7aab37397f554a7df5f142c21c1b7303b8a0626f1baded5c72a704f7e6cd84c OP_CHECKSIG",
            "hex": "4104ae1a62fe09c5f51b13905f07f06b99a2f7159b2225f374cd378d71302fa28414e7aab37397f554a7df5f142c21c1b7303b8a0626f1baded5c72a704f7e6cd84cac",
            "type": "pubkey"
          }
        },
        {
          "value": 40.00000000,
          "n": 1,
          "scriptPubKey": {
            "asm": "0411db93e1dcdb8a016b49840f8c53bc1eb68a382e97b1482ecad7b148a6909a5cb2e0eaddfb84ccf9744464f82e160bfa9b8b64f9d4c03f999b8643f656b412a3 OP_CHECKSIG",
            "hex": "410411db93e1dcdb8a016b49840f8c53bc1eb68a382e97b1482ecad7b148a6909a5cb2e0eaddfb84ccf9744464f82e160bfa9b8b64f9d4c03f999b8643f656b412a3ac",
            "type": "pubkey"
          }
        }
      ],
      "hex": "0100000001c997a5e56e104102fa209c6a852dd90660a20b2d9c352423edce25857fcd3704000000004847304402204e45e16932b8af514961a1d3a1a25fdf3f4f7732e9d624c6c61548ab5fb8cd410220181522ec8eca07de4860a4acdd12909d831cc56cbbac4622082221a8768d1d0901ffffffff0200ca9a3b00000000434104ae1a62fe09c5f51b13905f07f06b99a2f7159b2225f374cd378d71302fa28414e7aab37397f554a7df5f142c21c1b7303b8a0626f1baded5c72a704f7e6cd84cac00286bee0000000043410411db93e1dcdb8a016b49840f8c53bc1eb68a382e97b1482ecad7b148a6909a5cb2e0eaddfb84ccf9744464f82e160bfa9b8b64f9d4c03f999b8643f656b412a3ac00000000"
    }
  ],
  "time": 1231731025,
  "mediantime": 1231716245,
  "nonce": 1889418792,
  "bits": "1d00ffff",
  "difficulty": 1,
  "chainwork": "000000000000000000000000000000000000000000000000000000ab00ab00ab",
  "nTx": 2,
  "previousblockhash": "000000002a22cfee1f2c846adbd12b3e183d4f97683f85dad08a79780a84bd55",
  "nextblockhash": "00000000c9ec538cab7f38ef9c67a95742f56ab07b0a37c5be6b02808dbfb4e0"
}

```

## Authors

* [ethicnology](https://github.com/ethicnology)
* [Matthieu Latapy](https://www-complexnetworks.lip6.fr/~latapy/)