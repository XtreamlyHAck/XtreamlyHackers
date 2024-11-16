import {Anchor, Box, Container, Group, Loader} from '@mantine/core';
import {Link, useLocation} from 'react-router-dom';
import styles from './Header.module.scss';
import {useAccount} from 'wagmi';


function Header() {
    const imageSize = 50;
    const { isReconnecting, isDisconnected } = useAccount()
    const {pathname} = useLocation()
    
    if (pathname === "/") {
        return null;
    }

    return (
        <Box component="header" className={styles.header}>
            <Container size="xl">
                <Group justify="space-between">
                    <Anchor component={Link} to="/app" className='dfa'>
                        <img src="logo.png" alt="Logo" width={imageSize * 2} height={imageSize}/>
                    </Anchor>
                    {
                        !isDisconnected && isReconnecting ?
                            <Loader size={55}/>
                            : <w3m-button/>
                    }
                </Group>
            </Container>
        </Box>
    );
}

export default Header;