import {Vault} from "./vault";

export const vaults: Vault[] = [
    new Vault({
        type: 'long',
        risk: 'low',
        apy: 2,
        asset: 'ETH',
        contract: '0xf9feadAA7dbef738ee821ef339754194BC0d98ac',
    }),
    new Vault({
        type: 'long',
        risk: 'med',
        apy: 5,
        asset: 'ETH',
        contract: '0xf9feadAA7dbef738ee821ef339754194BC0d98ac',
    }),
    new Vault({
        type: 'long',
        risk: 'high',
        apy: 10,
        asset: 'ETH',
        contract: '0xf9feadAA7dbef738ee821ef339754194BC0d98ac',
    }),
    // new Vault({
    //     type: 'short',
    //     risk: 'low',
    //     apy: 2,
    //     asset: 'ETH',
    //     contract: '0xf9feadAA7dbef738ee821ef339754194BC0d98ac',
    // }),
    // new Vault({
    //     type: 'short',
    //     risk: 'med',
    //     apy: 5,
    //     asset: 'ETH',
    //     contract: '0xf9feadAA7dbef738ee821ef339754194BC0d98ac',
    // }),
    // new Vault({
    //     type: 'short',
    //     risk: 'high',
    //     apy: 10,
    //     asset: 'ETH',
    //     contract: '0xf9feadAA7dbef738ee821ef339754194BC0d98ac',
    // }),
]