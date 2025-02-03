export type Blogpost =
{ 
    title : string,
    path : string,
    author : string,
    markdown : string,
    tags : string[],
    hidden : boolean,
    date : string,
    description : string    
}