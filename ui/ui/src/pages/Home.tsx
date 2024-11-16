import {Box, SimpleGrid, Stack, Text, Title} from "@mantine/core";
import VaultCard from "../components/VaultCard";
import Transactions from "../components/Transactions";
import CustomVaults from "../components/CustomVaults";
import {useVaults} from "../data-access/vaults";


function Home() {
    const { data } = useVaults()

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
            <SimpleGrid
                cols={{ base: 1, md: 3 }}
            >
                {
                    data && data.map((vault, i) => (
                        <VaultCard key={i} vault={vault}/>
                    ))
                }
            </SimpleGrid>
            <CustomVaults/>
            <Box my={15}/>
            <Transactions/>
        </Stack>
    );
}

export default Home;
