import {Center, Group, Loader, Stack, Table, Text, Title} from "@mantine/core";
import {useAccount} from "wagmi";
import ConnectWallet from "./ConnectWallet.tsx";
import {useTransactions} from "../data-access/transactions";
import {Transaction} from "../data/transaction";
import {IconReload} from "@tabler/icons-react";

function UITransaction({transaction}: {transaction: Transaction}) {
    const {
        type,
        asset,
        risk,
    } = transaction.vault

    return (
        <Table.Tr>
            <Table.Td>{type}</Table.Td>
            <Table.Td>{asset}</Table.Td>
            <Table.Td>{risk}</Table.Td>
            <Table.Td>
                <Stack gap={1} ta="right">
                    ${transaction.value}
                    {/*<Earning amount={earnings}/>*/}
                </Stack>
            </Table.Td>
        </Table.Tr>
    );
}

function TransactionsTable() {
    const {isConnected, isConnecting} = useAccount()
    const { isError, isLoading, data } = useTransactions()

    if (isConnecting || isLoading) {
        return (
            <Center>
                <Loader size={70}/>
            </Center>
        )
    }

    if (!isConnected) {
        return <ConnectWallet/>
    }

    if (isError) {
        return <Text ta='center'>Unable to fetch your transactions. Please connect to the internet and try again.</Text>
    }

    return (
        <Table
            style={{
                fontSize: '25px'
            }}
            verticalSpacing="lg"
            horizontalSpacing="lg"
        >
            <Table.Thead>
                <Table.Tr fs="30px">
                    <Table.Th>Vault</Table.Th>
                    <Table.Th>Asset</Table.Th>
                    <Table.Th>Risk</Table.Th>
                    <Table.Th ta='right'>Amount ($)</Table.Th>
                </Table.Tr>
            </Table.Thead>
            <Table.Tbody>
                {
                    data?.map((t, i) => <UITransaction key={i} transaction={t!}/>)
                }
            </Table.Tbody>
        </Table>
    );
}

export default function Transactions() {
    const {refetch, isRefetching} = useTransactions()

    return (
        <>
            <Group justify="center">
                <Title ta='center'>Transactions</Title>
                {isRefetching ? <Loader/> : <IconReload size={36} onClick={() => refetch()}/>}
            </Group>
            <TransactionsTable />
        </>
    )
}