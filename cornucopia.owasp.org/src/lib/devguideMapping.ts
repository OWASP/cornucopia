import {data} from '$lib/devguide'

export class DevGuideMapping {

    constructor() {
    }

    public static getUrl(code : string) : string
    {
        let url = data[code.replaceAll(/[0-9-]+/g,"")  as keyof typeof data];
        return url ? url : "";
    }
}