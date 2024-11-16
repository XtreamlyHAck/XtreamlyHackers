import {PushAPI, CONSTANTS} from '@pushprotocol/restapi';
import {useAccount, useClient} from "wagmi";
import {BrowserProvider, JsonRpcSigner} from 'ethers'
import {toastError, toastSuccess} from "../components/ui-toast.tsx";
import {useQuery} from "@tanstack/react-query";

export const channel = "eip155:11155111:0xF6581727750412981985e8744916DCd95F13Abe5"

export function clientToSigner(client: any, address: any) {
    const {chain, transport} = client
    const network = {
        chainId: chain.id,
        name: chain.name,
        ensAddress: chain.contracts?.ensRegistry?.address,
    }
    const provider = new BrowserProvider(transport, network)
    const signer = new JsonRpcSigner(provider, address)
    return signer
}

async function getUser(client: any, address: any) {
    const signer = clientToSigner(client, address)
    return PushAPI.initialize(signer, {
        env: CONSTANTS.ENV.STAGING,
    });
}

async function subscribe(client: any, address: any) {
    const user = await getUser(client, address)
    return user.notification.subscribe(channel)
        .then(() => toastSuccess("You have subscribed to volatility alerts"))
        .catch((e) => toastError(e))
}

async function unsubscribe(client: any, address: any) {
    const user = await getUser(client, address)
    return user.notification.unsubscribe(channel)
        .then(() => toastSuccess("You have unsubscribed from volatility alerts"))
        .catch((e) => toastError(e))
}

async function subscriptions(client: any, address: any) {
    const user = await getUser(client, address)
    return user.notification.subscriptions()
}

export function useNotifications() {
    const {address} = useAccount()
    const client = useClient()

    return {
        subscribe: () => subscribe(client, address),
        unsubscribe: () => unsubscribe(client, address),
        subscriptions: useQuery({
            queryKey: ['notifications'],
            enabled: address !== undefined,
            queryFn: async () => subscriptions(client, address),
        })
    }
}