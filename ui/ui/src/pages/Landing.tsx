import {Button, Center, Image, Stack, Title} from "@mantine/core";
import {IconArrowRight} from "@tabler/icons-react";
import {Link} from "react-router-dom";


function Landing() {
    return (
        <Center c="white" style={{
            top: 0,
            bottom: 0,
            left: 0,
            right: 0,
            margin: 'auto',
            position: 'absolute',
            textAlign: 'center',
        }}>
            <Stack gap='xl'>
                <Center>
                    <Image src="logo_only.png" h={100} w={100} alt="logo"/>
                </Center>
                <Title size="7vw">Welcome to Xtreamly</Title>
                <Title size="4vw">Access AI Powered High Yield</Title>
                <Center>
                    <Button
                        size="xl"
                        maw={300}
                        component={Link}
                        to="/app"
                        rightSection={<IconArrowRight/>
                    }>
                        Enter App
                    </Button>
                </Center>
            </Stack>
        </Center>
    );
}

export default Landing;
