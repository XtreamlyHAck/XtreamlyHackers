import {Vault} from "./vault";

export interface Transaction {
    vault: Vault;
    value: string;
}
