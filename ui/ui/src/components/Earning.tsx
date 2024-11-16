import {Text} from "@mantine/core";


export default function Earning(
    {
        amount,
        parenthesis
    }: {
        amount: number,
        parenthesis?: boolean
    }
) {
    let color = 'white';
    if (amount < 0) {
        color = 'red';
    }
    if (amount > 0) {
        color = 'green';
    }

    return (
        <Text c={color}>
            {parenthesis && '('}
            {amount >= 0 ? '+' : '-'}
            ${Math.abs(amount)}
            {parenthesis && ')'}
        </Text>
    )
}