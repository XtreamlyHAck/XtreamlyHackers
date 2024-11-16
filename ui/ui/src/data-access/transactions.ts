import {useQuery} from '@tanstack/react-query';
import {useAccount} from "wagmi";
import {get} from "../utils/requests";
import {Transaction} from "../data/transaction";
import {vaults} from "../data/vaults";
import {Vault} from "../data/vault";
import abi from "../data/abi";
import {ethers} from "ethers";
import {rpc} from '../utils/wallet'

const baseUrl = "https://api-sepolia.arbiscan.io/api"
const apiKey = 'UEJA5VG3FMJN75ATC2YFV6V26AUD5GPSHH'

function findVault(transaction: any): Vault {
    return transaction.to && vaults.find((v) =>
        transaction.to.toLowerCase() === v.contract.toLowerCase()
    )
}

function filterTransactions(transactions: any[]) {
    return transactions.filter((t: any) =>
        t.input && t.input.length > 2
        && t.functionName && t.functionName.startsWith("setGreeting")
        && findVault(t)
    )
}

function mapTransaction(transaction: any): Transaction | null {
    const vault = findVault(transaction);
    if (!vault) {
        return null;
    }

    const value = decodeTransactionInput(transaction, vault)
    if (!value) {
        return null;
    }

    return {
        vault,
        value
    };
}

export function useTransactions() {
    const {address} = useAccount()

    return useQuery({
        queryKey: ['transactions'],
        enabled: address !== undefined,
        queryFn: async () => {
            const params = {
                module: "account",
                action: "txlist",
                startblock: 0,
                endblock: 'latest',
                sort: 'desc',
                apiKey,
                address,
            }
            return get(baseUrl, params)
                .then(res => res.json())
                .then(res => res.result)
                .then(filterTransactions)
                .then(res => res.map(mapTransaction))
                .then(res => res.filter((r) => r))
        },
    })
}

function decodeTransactionInput(tx: any, vault: Vault): string | undefined {
    const provider = new ethers.JsonRpcProvider(rpc);
    const contract = new ethers.Contract(vault.contract, abi, provider);
    const decoded = contract.interface.parseTransaction({
        data: tx.input
    });
    return decoded?.args[0]
}