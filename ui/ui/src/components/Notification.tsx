import {Button, Image} from "@mantine/core";
import {channel, useNotifications} from "../data-access/notifications";

export default function Notification() {
    const {subscriptions, subscribe, unsubscribe} = useNotifications()
    const { data, isLoading, refetch } = subscriptions

    const isSubscribed = data?.find((s: any) => channel.toLowerCase().endsWith(s.channel.toLowerCase()))
    const text = isSubscribed ?
        "Unsubscribe from volatility alerts" :
        "Subscribe to volatility alerts"

    return (
        <Button
            leftSection={<Image src="push.png" w={20}/>}
            loading={isLoading}
            onClick={
                isSubscribed ?
                () => subscribe().finally(refetch) :
                () => unsubscribe().finally(refetch)
            }
        >
            {text}
        </Button>
    )
}