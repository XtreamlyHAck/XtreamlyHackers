import "@nomicfoundation/hardhat-verify";
import "dotenv/config";
import { artifacts, ethers, run } from 'hardhat';
import { VolatilityApiContract } from '../typechain-types';
import { VolatilityApiInstance } from "../typechain-types/contracts/web2VolatilityInteractor.sol/VolatilityApi";
const VolatilityApi: VolatilityApiContract = artifacts.require('VolatilityApi');

const VERIFIER_SERVER_URL = "http://0.0.0.0:8002/IJsonApi/prepareResponse";

async function getAttestationData(): Promise<any> {

    return await (await fetch(VERIFIER_SERVER_URL,
        {
            method: "POST",
            headers: { "X-API-KEY": "12345", "Content-Type": "application/json" },
            body: JSON.stringify({
                "attestationType": "0x4a736f6e41706900000000000000000000000000000000000000000000000000",
                "sourceId": "0x5745423200000000000000000000000000000000000000000000000000000000",
                "messageIntegrityCode": "0x0000000000000000000000000000000000000000000000000000000000000000",
                "requestBody": {
                    "url": "http://localhost:8000/volatility",
                    "postprocessJq": "{volatility: .predictions[0]}",
                    "abi_signature": '{"struct Volatility":{"volatility":"uint256"}}'
                }
            })
        })).json();
}

async function main() {
    const attestationData = await getAttestationData();

    if (!attestationData.response) {
        throw new Error(`Error verifying ${JSON.stringify(attestationData)}`)
    }
    console.log(attestationData.response);

    const [deployer] = await ethers.getSigners();

    console.log("Deploying contracts with the account:", deployer.address);

    // const jsonApi: VolatilityApiInstance = await VolatilityApi.at("0xf37e9ACe5D12a95C72Cb795A9178E6fFF34040eE") //new()
    const jsonApi: VolatilityApiInstance = await VolatilityApi.new()

    await jsonApi.addVolatility(attestationData.response);

    try {
        const result = await run("verify:verify", {
            address: jsonApi.address,
            constructorArguments: [],
        })

        console.log(result)
    } catch (e: any) {
        console.log(e.message)
    }
}

main().then(() => process.exit(0))