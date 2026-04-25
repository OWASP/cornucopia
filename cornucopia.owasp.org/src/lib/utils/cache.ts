/* eslint-disable no-useless-assignment */
import fs from 'fs';

// Cache the result of a given function on the local filesystem
export async function LocalCache(func: () => unknown, cacheSeconds : number, description : string)
{
    let logMessage = "[LocalCacheAsync] ";
    const filename : string = generateFilename('async-' + description);

    const [cacheStatusOk,cacheAge] = cacheIsOk(filename,cacheSeconds);

    if(cacheStatusOk)
    {
        logMessage += " ðŸŸ¢ Found general request [" + description + "] in cache.";
        logMessage += "\tâ±ï¸ Age is " + cacheAge + " seconds."
        const responseAsString = fs.readFileSync(filename).toString();

        const size = Buffer.byteLength(responseAsString);
        const kiloBytes = Math.round(size / 1024);
        logMessage += "\tðŸ’¿ " + kiloBytes + " kb."

        const response = JSON.parse(responseAsString);
        return response; 
    }
    else
    {
        logMessage += " ðŸŸ  " + description + " not in cache, got from API";
        logMessage += "\tâ±ï¸ Age is " + cacheAge + " seconds."
        
        const result = func();
        const response = await Promise.resolve(result)
        const responseAsJSON = JSON.stringify(response)

        const size = Buffer.byteLength(responseAsJSON);
        const kiloBytes = Math.round(size / 1024);
        logMessage += "\tðŸ’¿ " + kiloBytes + " kb."

        fs.writeFileSync(filename, responseAsJSON);
        console.log(logMessage);
        return response;
    }

}

// The same as LocalCache, but for synchronous functions
export function LocalCacheSync(func: () => unknown, cacheSeconds : number, description : string)
{
    let logMessage = "[LocalCacheSync] ";
    const filename : string = generateFilename('sync-' + description);

    const [cacheStatusOk,cacheAge] = cacheIsOk(filename,cacheSeconds);

    if(cacheStatusOk)
    {
        logMessage += " ðŸŸ¢ Found general request [" + description + "] in cache.";
        logMessage += "\tâ±ï¸ Age is " + cacheAge + " seconds."
        const responseAsString = fs.readFileSync(filename).toString();

        const size = Buffer.byteLength(responseAsString);
        const kiloBytes = Math.round(size / 1024);
        logMessage += "\tðŸ’¿ " + kiloBytes + " kb."

        const response = JSON.parse(responseAsString);
        console.log(logMessage);
        return response; 
    }
    else
    {
        logMessage += " ðŸŸ  " + description + " not in cache, got from API";
        logMessage += "\tâ±ï¸ Age is " + cacheAge + " seconds."
        
        const result = func();
        const responseAsJSON = JSON.stringify(result)

        const size = Buffer.byteLength(responseAsJSON);
        const kiloBytes = Math.round(size / 1024);
        logMessage += "\tðŸ’¿ " + kiloBytes + " kb."

        fs.writeFileSync(filename, responseAsJSON);
        console.log(logMessage);
        return result;
    }
}

function getSecondsAge(input : Date) : number
{
    const today = new Date();
    return Math.round(Math.abs(today.getTime() - input.getTime()) / 1000);
}

function generateFilename(input : string) : string
{
    return 'cache/' + input + '.cache';
}

function cacheIsOk(path : string, maximumAge : number) : [boolean,number]
{

    const fileExists : boolean = fs.existsSync(path);

    if(!fileExists)
        return [false,-1];

    const stats = fs.statSync(path);
    const diff : number =  getSecondsAge(stats.mtime)// Cache age in seconds
    if(diff > maximumAge)
        return [false,diff];

    return [true,diff];
}
