import {useQuery, useQueryClient} from '@tanstack/react-query';
import {Vault} from '../data/vault';
import {vaults} from '../data/vaults';
import {useReadContract, useWriteContract} from "wagmi";
import abi from "../data/abi.ts";
import {toastError, toastSuccess} from "../components/ui-toast.tsx";

export function useVaults() {
    return useQuery({
        queryKey: ['vaults'],
        queryFn: async () => vaults,
    })
}


export function useVault(vault: Vault) {
    const balance = useBalance(vault)
    const vaultAction = useVaultAction(vault)

    const action = (...args: Parameters<typeof vaultAction>) => vaultAction(...args).then(() => balance.refetch())

    return {
        loading: balance.isFetching,
        balance: balance.data as string,
        vaultAction: action
    }
}


export function useVaultAction(vault: Vault) {
    const { writeContractAsync } = useWriteContract()
    const queryClient = useQueryClient();

    const message: any = {
        deposit: 'Deposited',
        withdrawal: 'Withdrew',
    }

    return (action: string, amount: number) => writeContractAsync({
        abi,
        address: vault.contract,
        // functionName: action,
        functionName: 'setGreeting',
        args: [amount]
    })
        .then(() => {
            toastSuccess(`${message[action]} ${amount} into ${vault.title} successfully.`);
            setTimeout(() => {
                queryClient.refetchQueries({ queryKey: ['transactions'] })
            }, 1000)
        })
        .catch(() => toastError(`Unable to ${action} ${amount} from ${vault.title}.`))
}

export function useBalance(vault: Vault) {
    return useReadContract({
        abi,
        address: vault.contract,
        // functionName: 'balance',
        functionName: 'greeting',
    })
}