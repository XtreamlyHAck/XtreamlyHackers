// Core styles
import '@mantine/core/styles.css'
// Package styles
// import '@mantine/dates/styles.css'
import '@mantine/notifications/styles.css'
// import '@mantine/dropzone/styles.css';
// import '@mantine/charts/styles.css';
import {generateColors} from '@mantine/colors-generator'

import {createTheme, Loader} from "@mantine/core";
import {RingLoader} from "./components/RingLoader.tsx";

export const brandColor = '#28ab99'
export const brand = generateColors(brandColor)
export const blueColor = '#1d2f86'
export const blue = generateColors(blueColor)
export const redColor = '#cc2332'
export const red = generateColors(redColor)
export const gradientColor = 'linear-gradient(90deg, rgba(29,47,134,1) 0%, rgba(226,226,226,1) 49%, rgba(204,35,50,1) 100%)'
export const gradient = {
    from: blueColor,
    to: redColor,
    deg: 141
};

export const theme = createTheme({
    black: '#040307',
    colors: {
        blue,
        red,
    },
    fontFamily: 'ABCDiatype-Medium, sans-serif',
    fontFamilyMonospace: 'ABCDiatypeSemi-Mono-Medium, monospace',
    headings: {fontFamily: 'ABCDiatype-Medium, sans-serif'},
    components: {
        Loader: Loader.extend({
            defaultProps: {
                loaders: { ...Loader.defaultLoaders, ring: RingLoader },
                color: brandColor,
                type: 'ring',
            },
        }),
        TextInput: {
            styles: () => ({
                label: {
                    display: 'block',
                    textAlign: 'left',
                },
            }),
        },
        Textarea: {
            styles: () => ({
                label: {
                    display: 'block',
                    textAlign: 'left',
                },
            }),
        },
        Select: {
            styles: () => ({
                label: {
                    display: 'block',
                    textAlign: 'left',
                },
            }),
        },
        Button: {
            styles: () => ({
                root: {
                    backgroundColor: brandColor,
                    border: 'none',
                    borderRadius: 40
                },
            }),
        },
    },
})