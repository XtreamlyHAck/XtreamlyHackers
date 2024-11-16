import {Button, Card, Center, Group, Loader, NumberInput, Stack, Text, Title} from "@mantine/core";
import {IconMinus, IconPlus} from "@tabler/icons-react";
import {useAppKit} from '@reown/appkit/react';
import {useAccount} from "wagmi";
import {isInRange, useForm} from "@mantine/form";
import {useState} from "react";
import {Vault} from "../data/vault";
import {useVault} from "../data-access/vaults.ts";
import Earning from "./Earning.tsx";
import Notification from "./Notification.tsx";

// One contract per vault

// functionname,args
// withdraw,[amount]
// deposit,[amount]
// balance,[]
// transactions,[]

// BE: restrategize,[vault, open, close]


export default function VaultCard(
    {
        vault
    } :
    {
        vault: Vault;
    }
) {
    const {open} = useAppKit()
    const {isConnected} = useAccount()
    const [action, setAction] = useState('');
    const { loading, balance, vaultAction } = useVault(vault)

    const handleSubmit = async ({amount}: {amount: number}) => {
        await vaultAction(action, amount)
    };

    const form = useForm({
        mode: 'uncontrolled',
        initialValues: {
            amount: 0,
        },
        validate: {
            amount: isInRange({min: 1, max: 10000000}, 'Amount must be >= 1 and <= 1,000,000')
        },
    });

    let riskColor = 'red';
    if (vault.risk === 'low') {
        riskColor = 'green';
    }
    if (vault.risk === 'med') {
        riskColor = 'orange';
    }

    return (
        <Card
            shadow="sm"
            padding="lg"
            radius="lg"
            bg="rgba(0,0,0, 0.2)"
            c="white"
        >
            <Stack>
                <Stack gap={0}>
                    <Title ta="center">{vault.title}</Title>
                    <Text ta="center" c={riskColor}>{vault.riskDescription}</Text>
                </Stack>
                {
                    loading &&
                    <Center>
                        <Loader size={60}/>
                    </Center>
                }
                {
                    !loading &&
                    <Stack gap={0}>
                        <Title order={3} ta="center">Current Exposure</Title>
                        <Group justify="center" gap={10}>
                            <Text size="lg">{balance ? `$${balance}` : 'No Exposure'}</Text>
                            {balance && <Earning amount={10} parenthesis/>}
                        </Group>
                    </Stack>
                }

                <form onSubmit={form.onSubmit(handleSubmit)}>
                    <Stack gap={20}>
                        <NumberInput
                            label="Amount ($)"
                            size="lg"
                            radius="lg"
                            required
                            key={form.key('amount')}
                            {...form.getInputProps('amount')}
                        />
                        <Group justify="right">
                            <Notification/>
                            <Button
                                size="md"
                                leftSection={<IconPlus/>}
                                type="submit"
                                onClick={() => !isConnected ? open() : setAction('deposit')}
                            >
                                Deposit
                            </Button>
                            <Button
                                size="md"
                                leftSection={<IconMinus/>}
                                type="submit"
                                onClick={() => !isConnected ? open() : setAction('withdraw')}
                            >
                                Withdraw
                            </Button>
                        </Group>
                    </Stack>
                </form>
            </Stack>
        </Card>
    )
}