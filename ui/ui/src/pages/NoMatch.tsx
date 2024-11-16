import { Center } from "@mantine/core";

function NoMatch() {
  return (
    <Center>
      <h1>Page Not Found</h1>
      <p>
        The specified file was not found on this website. Please check the URL
        for mistakes and try again.
      </p>
    </Center>
  );
}

export default NoMatch;
