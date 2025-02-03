import fs from 'fs';

// Cache the result of a given function on the local filesystem
export async function LocalCache(func : Function, cacheSeconds : number, description : string)
{
    let logMessage = "[LocalCacheAsync] ";
    let filename : string = generateFilename('async-' + description);

    let [cacheStatusOk,cacheAge] = cacheIsOk(filename,cacheSeconds);

    if(cacheStatusOk)
    {
        logMessage += " 🟢 Found general request [" + description + "] in cache.";
        logMessage += "\t⏱️ Age is " + cacheAge + " seconds."
        let responseAsString = fs.readFileSync(filename).toString();

        const size = Buffer.byteLength(responseAsString);
        const kiloBytes = Math.round(size / 1024);
        logMessage += "\t💿 " + kiloBytes + " kb."

        let response = JSON.parse(responseAsString);
        console.log(logMessage);
        return response; 
    }
    else
    {
        logMessage += " 🟠 " + description + " not in cache, got from API";
        logMessage += "\t⏱️ Age is " + cacheAge + " seconds."
        
        let result = func();
        let response = await Promise.resolve(result)
        let responseAsJSON = JSON.stringify(response)

        const size = Buffer.byteLength(responseAsJSON);
        const kiloBytes = Math.round(size / 1024);
        logMessage += "\t💿 " + kiloBytes + " kb."

        fs.writeFileSync(filename, responseAsJSON);
        console.log(logMessage);
        return response;
    }

}

// The same as LocalCache, but for synchronous functions
export function LocalCacheSync(func : Function, cacheSeconds : number, description : string)
{
    let logMessage = "[LocalCacheSync] ";
    let filename : string = generateFilename('sync-' + description);

    let [cacheStatusOk,cacheAge] = cacheIsOk(filename,cacheSeconds);

    if(cacheStatusOk)
    {
        logMessage += " 🟢 Found general request [" + description + "] in cache.";
        logMessage += "\t⏱️ Age is " + cacheAge + " seconds."
        let responseAsString = fs.readFileSync(filename).toString();

        const size = Buffer.byteLength(responseAsString);
        const kiloBytes = Math.round(size / 1024);
        logMessage += "\t💿 " + kiloBytes + " kb."

        let response = JSON.parse(responseAsString);
        console.log(logMessage);
        return response; 
    }
    else
    {
        logMessage += " 🟠 " + description + " not in cache, got from API";
        logMessage += "\t⏱️ Age is " + cacheAge + " seconds."
        
        let result = func();
        let responseAsJSON = JSON.stringify(result)

        const size = Buffer.byteLength(responseAsJSON);
        const kiloBytes = Math.round(size / 1024);
        logMessage += "\t💿 " + kiloBytes + " kb."

        fs.writeFileSync(filename, responseAsJSON);
        console.log(logMessage);
        return result;
    }
}

function getSecondsAge(input : Date) : number
{
    let today = new Date();
    return Math.round(Math.abs(today.getTime() - input.getTime()) / 1000);
}

function generateFilename(input : string) : string
{
    return 'cache/' + input + '.cache';
}

function cacheIsOk(path : string, maximumAge : number) : [boolean,number]
{

    let fileExists : boolean = fs.existsSync(path);

    if(!fileExists)
        return [false,-1];

    let stats = fs.statSync(path);
    let diff : number =  getSecondsAge(stats.mtime)// Cache age in seconds
    if(diff > maximumAge)
        return [false,diff];

    return [true,diff];
}