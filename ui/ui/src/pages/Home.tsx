import {Box, SegmentedControl, SimpleGrid, Stack, Text, Title} from "@mantine/core";
import VaultCard from "../components/VaultCard";
import Transactions from "../components/Transactions";
import {useVaults} from "../data-access/vaults";
import {useState} from "react";


function Home() {
    const { data } = useVaults()
    const [ risk, setRisk ] = useState<string>("low")
    const vault = data?.find((v) => v.risk === risk)

    return (
        <Stack c="white">
            <Stack ta="center">
                <Title>
                    Start Earning now !
                </Title>
                <Text>
                    !!! DISCLAIMER !!!
                </Text>
            </Stack>

            <Stack ta="center" mt={20}>
                <Title order={3}>Pick your risk appetite</Title>
                <SegmentedControl
                    radius="xl"
                    value={risk}
                    onChange={setRisk}
                    data={[
                        { label: <Text c="green">LOW</Text>, value: 'low' },
                        { label: <Text c="orange">MEDIUM</Text>, value: 'med' },
                        { label: <Text c="red">HIGH</Text>, value: 'high' },
                    ]}
                />
            </Stack>

            <SimpleGrid
                cols={{ base: 1, md: 1 }}
            >
                {
                    vault && <VaultCard vault={vault}/>
                }
            </SimpleGrid>
            <Box my={15}/>
            <Transactions/>
        </Stack>
    );
}

export default Home;
