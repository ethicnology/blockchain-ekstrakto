# Blockchain extractor is a Python program which extracts all Bitcoin blockchain data using Bitcoin Core.
# Copyright (C) 2020  ethicnology

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import configparser
import json
import requests
import sys

config = configparser.ConfigParser()
config.read('config.ini')
url = config['Bitcoin']['Url']
user = config['Bitcoin']['RpcUser']
pwd = config['Bitcoin']['RpcPassword']

headers = {'content-type': 'text/plain;'}

# If there are no arguments specified,
# blockchain extraction will start from the last block mined a.k.a best block to the first block mined a.k.a genesis block
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--source", type=int, help="Specify the first block from which you start the extraction")
parser.add_argument("-t", "--target", type=int, help="Specify the last block you want to extract", default=0)
args = parser.parse_args()

# If None, get the last block hash added to the blockchain a.k.a best block hash
if args.source is None :
    jsonrpc = '{"jsonrpc": "1.0", "id":"curltest", "method": "getbestblockhash", "params": [] }'
    source_block_hash = requests.post(url, headers=headers, data=jsonrpc, auth=(user, pwd)).json()['result']
else :
    jsonrpc = '{"jsonrpc": "1.0", "id":"curltest", "method": "getblockhash", "params": [%i] }' % (args.source)
    source_block_hash = requests.post(url, headers=headers, data=jsonrpc, auth=(user, pwd)).json()['result']

# Get source block data
jsonrpc = '{"jsonrpc": "1.0", "id":"curltest", "method": "getblock", "params": ["%s", 2] }' % (source_block_hash)
block = requests.post(url, headers=headers, data=jsonrpc, auth=(user, pwd)).json()['result']
# Write source block
sys.stdout.write(json.dumps(block)+'\n')
# Needed variables to parse the blockchain
block_height = block['height']
previous_block_hash = block['previousblockhash']
sys.stderr.write(str(block_height)+'\n')

# Reading the blockchain from the end
# Looping to get previous block data (transactions included)
while int(block_height) > args.target:
    jsonrpc = '{"jsonrpc": "1.0", "id":"curltest", "method": "getblock", "params": ["%s", 2] }' % (previous_block_hash)
    try:
        block = requests.post(url, headers=headers, data=jsonrpc, auth=(user, pwd))
        block.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    block = block.json()['result']
    # Write current block
    sys.stdout.write(json.dumps(block)+'\n')
    block_height = block['height']
    # Write block height to stderr
    sys.stderr.write(str(block_height)+'\n')
    sys.stderr.flush()
    # Break while if the target is reached
    if int(block_height) == args.target:
        break
    # Previous block hash is the next block to parse
    previous_block_hash = block['previousblockhash']
