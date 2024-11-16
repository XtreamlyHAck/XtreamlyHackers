import {Button, Card, Group, NumberInput, Stack, Title} from "@mantine/core";
import {IconMinus, IconPlus} from "@tabler/icons-react";

export default function CustomVaults() {
    return (
        <Card
            shadow="sm"
            padding="lg"
            radius="lg"
            bg="rgba(0,0,0, 0.2)"
            c="white"
            mih={200}
        >
            <Title ta="center">Custom Vaults</Title>
            <Title
                size='1.4rem'
                style={{
                    position: 'absolute',
                    top: '50%',
                    left: '50%',
                    transform: 'translate(-50%, 10%) rotate(-30deg)',
                    zIndex: 20,
                }}
            >
                COMING SOON...
            </Title>
            <Stack
                gap={20}
                style={{
                    filter: 'blur(40px)',
                    position: 'relative',
                }}
            >
                <NumberInput label="Amount ($)" size="lg"/>
                <Group justify="right">
                    <Button size="md" leftSection={<IconPlus/>}>
                        Deposit
                    </Button>
                    <Button size="md" leftSection={<IconMinus/>}>
                        Withdraw
                    </Button>
                </Group>
            </Stack>
        </Card>
    )
}
