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

import requests
import json
import configparser
import sys

config = configparser.ConfigParser()
config.read('config.ini')
url = config['Bitcoin']['Url']
user = config['Bitcoin']['RpcUser']
pwd = config['Bitcoin']['RpcPassword']

headers = {'content-type': 'text/plain;'}

# Get the last block hash added to the blockchain a.k.a best block hash
jsonrpc = '{"jsonrpc": "1.0", "id":"curltest", "method": "getbestblockhash", "params": [] }'
best_block_hash = requests.post(url, headers=headers, data=jsonrpc, auth=(user, pwd)).json()['result']

# Check if user specified a target block
if len(sys.argv) == 2 :
    target = int(sys.argv[1])
    source_block_hash = best_block_hash
# Check if user specified a target block and a source block
elif len(sys.argv) == 3 :
    target = int(sys.argv[1])
    source = int(sys.argv[2])
    # Get source block hash
    jsonrpc = '{"jsonrpc": "1.0", "id":"curltest", "method": "getblockhash", "params": [%i] }' % (source)
    source_block_hash = requests.post(url, headers=headers, data=jsonrpc, auth=(user, pwd)).json()['result']
# Else, it will parse all the blockchain from the best block hash known
else :
    target = 0
    source_block_hash = best_block_hash

# Get source block data
jsonrpc = '{"jsonrpc": "1.0", "id":"curltest", "method": "getblock", "params": ["%s", 2] }' % (source_block_hash)
block = requests.post(url, headers=headers, data=jsonrpc, auth=(user, pwd)).json()['result']
# Write source block
sys.stdout.write(json.dumps(block)+'\n')
# Needed variables to parse the blockchain
block_height = block['height']
previous_block_hash = block['previousblockhash']

# Reading the blockchain from the end
# Looping to get previous block data (transactions included)
while int(block_height) >= target:
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
    if int(block_height) == target:
        break
    # Previous block hash is the next block to parse
    previous_block_hash = block['previousblockhash']
