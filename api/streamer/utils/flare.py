from streamer.utils.contracts import Web3Contact

rpc = 'https://coston-api.flare.network/ext/C/rpc'

address = '0x5BBCc7810D72Cc1720cC97aD144926E556bE1E93'

abi = [
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_addressUpdater",
                "type": "address"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "inputs": [],
        "name": "FTSO_PROTOCOL_ID",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "fastUpdater",
        "outputs": [
            {
                "internalType": "contract IFastUpdater",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "fastUpdatesConfiguration",
        "outputs": [
            {
                "internalType": "contract IFastUpdatesConfiguration",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getAddressUpdater",
        "outputs": [
            {
                "internalType": "address",
                "name": "_addressUpdater",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes21",
                "name": "_feedId",
                "type": "bytes21"
            }
        ],
        "name": "getFeedById",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            },
            {
                "internalType": "int8",
                "name": "",
                "type": "int8"
            },
            {
                "internalType": "uint64",
                "name": "",
                "type": "uint64"
            }
        ],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes21",
                "name": "_feedId",
                "type": "bytes21"
            }
        ],
        "name": "getFeedByIdInWei",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "_value",
                "type": "uint256"
            },
            {
                "internalType": "uint64",
                "name": "_timestamp",
                "type": "uint64"
            }
        ],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_index",
                "type": "uint256"
            }
        ],
        "name": "getFeedByIndex",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            },
            {
                "internalType": "int8",
                "name": "",
                "type": "int8"
            },
            {
                "internalType": "uint64",
                "name": "",
                "type": "uint64"
            }
        ],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_index",
                "type": "uint256"
            }
        ],
        "name": "getFeedByIndexInWei",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "_value",
                "type": "uint256"
            },
            {
                "internalType": "uint64",
                "name": "_timestamp",
                "type": "uint64"
            }
        ],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_index",
                "type": "uint256"
            }
        ],
        "name": "getFeedId",
        "outputs": [
            {
                "internalType": "bytes21",
                "name": "",
                "type": "bytes21"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes21",
                "name": "_feedId",
                "type": "bytes21"
            }
        ],
        "name": "getFeedIndex",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes21[]",
                "name": "_feedIds",
                "type": "bytes21[]"
            }
        ],
        "name": "getFeedsById",
        "outputs": [
            {
                "internalType": "uint256[]",
                "name": "",
                "type": "uint256[]"
            },
            {
                "internalType": "int8[]",
                "name": "",
                "type": "int8[]"
            },
            {
                "internalType": "uint64",
                "name": "",
                "type": "uint64"
            }
        ],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes21[]",
                "name": "_feedIds",
                "type": "bytes21[]"
            }
        ],
        "name": "getFeedsByIdInWei",
        "outputs": [
            {
                "internalType": "uint256[]",
                "name": "_values",
                "type": "uint256[]"
            },
            {
                "internalType": "uint64",
                "name": "_timestamp",
                "type": "uint64"
            }
        ],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256[]",
                "name": "_indices",
                "type": "uint256[]"
            }
        ],
        "name": "getFeedsByIndex",
        "outputs": [
            {
                "internalType": "uint256[]",
                "name": "",
                "type": "uint256[]"
            },
            {
                "internalType": "int8[]",
                "name": "",
                "type": "int8[]"
            },
            {
                "internalType": "uint64",
                "name": "",
                "type": "uint64"
            }
        ],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256[]",
                "name": "_indices",
                "type": "uint256[]"
            }
        ],
        "name": "getFeedsByIndexInWei",
        "outputs": [
            {
                "internalType": "uint256[]",
                "name": "_values",
                "type": "uint256[]"
            },
            {
                "internalType": "uint64",
                "name": "_timestamp",
                "type": "uint64"
            }
        ],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "relay",
        "outputs": [
            {
                "internalType": "contract IRelay",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32[]",
                "name": "_contractNameHashes",
                "type": "bytes32[]"
            },
            {
                "internalType": "address[]",
                "name": "_contractAddresses",
                "type": "address[]"
            }
        ],
        "name": "updateContractAddresses",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "components": [
                    {
                        "internalType": "bytes32[]",
                        "name": "proof",
                        "type": "bytes32[]"
                    },
                    {
                        "components": [
                            {
                                "internalType": "uint32",
                                "name": "votingRoundId",
                                "type": "uint32"
                            },
                            {
                                "internalType": "bytes21",
                                "name": "id",
                                "type": "bytes21"
                            },
                            {
                                "internalType": "int32",
                                "name": "value",
                                "type": "int32"
                            },
                            {
                                "internalType": "uint16",
                                "name": "turnoutBIPS",
                                "type": "uint16"
                            },
                            {
                                "internalType": "int8",
                                "name": "decimals",
                                "type": "int8"
                            }
                        ],
                        "internalType": "struct FtsoV2Interface.FeedData",
                        "name": "body",
                        "type": "tuple"
                    }
                ],
                "internalType": "struct FtsoV2Interface.FeedDataWithProof",
                "name": "_feedData",
                "type": "tuple"
            }
        ],
        "name": "verifyFeedData",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

contract = Web3Contact(rpc, address, abi)
feedId = "0x014554482f55534400000000000000000000000000"  # ETH/USD


def get_latest_price():
    data = contract.read_contract("getFeedById", feedId)
    return {
        "price": data[0],
        "timestamp": data[2]
    }
