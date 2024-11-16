export interface VaultType {
    type: 'long' | 'short';
    risk: 'low' | 'med' | 'high';
    apy: number;
    asset: string;
    contract: `0x${string}`
}

export class Vault {
    type!: 'long' | 'short';
    risk!: 'low' | 'med' | 'high';
    apy!: number;
    asset!: string;
    contract!: `0x${string}`;

    constructor({type, risk, apy, asset, contract}: VaultType) {
        this.type = type;
        this.risk = risk;
        this.apy = apy;
        this.asset = asset;
        this.contract = contract;
    }

    get title(): string {
        const t = this.type.charAt(0).toUpperCase() + this.type.slice(1);
        return `${t} ${this.asset} Vault`;
    }

    get apyPerc(): string {
        return `+${this.apy}% APY`;
    }

    get riskDescription(): string {
        return `${this.risk} (${this.apyPerc})`;
    }
}
