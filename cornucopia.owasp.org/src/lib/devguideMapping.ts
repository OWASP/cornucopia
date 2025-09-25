import {data} from '$lib/devguide'

export class DevGuideMapping {

    public static getUrl(code : string) : string
    {
        return data[code.replaceAll(/[0-9-]+/g,"") as keyof typeof data] || "";
    }
}