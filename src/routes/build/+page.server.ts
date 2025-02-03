import { PRIVATE_GITHUB_KEY } from '$env/static/private'
import { LocalCache } from '$lib/utils/cache.js';
let options : RequestInit = 
{
    method : 'GET',
    headers : 
    {
        'Accept' : "application/vnd.github+json",
        'Authorization' : "Bearer " + PRIVATE_GITHUB_KEY,
        'X-GitHub-Api-Version' : "2022-11-28",
    }
}

/*
export async function load({params})
{
    return {
        commits : await LocalCache(getCommits,3600,"get-all-commits"),
    }
}
*/

async function getCommits()
{

    let response = await fetch('https://api.github.com/repos/jefmeijvis/cornucopia.dotnetlab.eu/commits',options);
    let json = await response.json();
    console.dir(json);

    for(let i = 0 ; i < json.length ; i++)
    {
        let commit : any = json[i];
        let sha : string = commit.sha;
        let details = await LocalCache(()=>getDetails(sha),3600,'github-details-' + sha);
        json[i].status = details.state; 
        json[i].details = details;
    }

    return json;
}

async function getDetails(sha : string) : Promise<any>
{
    let url = "https://api.github.com/repos/jefmeijvis/cornucopia.dotnetlab.eu/commits/" + sha + "/status";
    let detailsResponse = await fetch(url,options);
    let details = await detailsResponse.json();
    return details;
}
