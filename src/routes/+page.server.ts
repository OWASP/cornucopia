import { getSuits } from "../domain/suit/suitController";

export function load()
{
    return {
        suits : getSuits(),
    }
}

