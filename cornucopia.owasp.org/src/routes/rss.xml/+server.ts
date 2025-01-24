import type { Blogpost } from "../../domain/blogpost/blogpost.js";
import { LocalCache } from "$lib/utils/cache.js";
import { getBlogposts } from "../../domain/blogpost/blogpostController.js";
import { Text } from "$lib/utils/text.js";
export const prerender = true;
// Header options
const responseInit: ResponseInit = {
  headers: {
    "Cache-Control": `max-age=0, s-max-age=${600}`,
    "Content-Type": "application/xml",
  },
};

let bodyStart =
  '<?xml version="1.0" encoding="UTF-8" ?>' +
  '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">' +
  "<channel>" +
  '<atom:link href="https://cornucopia.owasp.org/rss.xml" rel="self" type="application/rss+xml" />' +
  "<title>OWASP Cornucopia</title>" +
  "<link>https://cornucopia.owasp.org</link>" +
  "<language>en</language>" +
  "<description>Owasp Cornucopia is a CyberSecurity card game, meant to be played in an agile development context. It allows developers to identify and discuss security requirements for their software applications. It is an easy way to introduce the practice of threat modeling in a software development team.</description>" +
  "<image>" +
  "<url>https://cornucopia.owasp.org/images/opengraph.png</url>" +
  "<title>OWASP Cornucopia</title>" +
  "<link>https://cornucopia.owasp.org</link>" +
  "</image>";

let bodyEnd = "</channel>" + "</rss>";

export async function GET() {
  let json = await LocalCache(() => getBlogposts(), 20, "posts");

  let body: string = bodyStart;
  for (let i = 0; i < json.length; i++) {
    let post: Blogpost = json[i];
    body += "<item>";

    // Title
    body += "<title>";
    body += Text.Format(post.title);
    body += "</title>";
   
    // Link
    body += "<link>";
    body += generateLink(post);
    body += "</link>";
    // Description
    body += "<description>";
    body += generateDescription(post);
    body += "</description>";

    // Guid
    body += '<guid isPermaLink="true">';
    body += generateLink(post);
    body += "</guid>";

    // Guid
    body += '<source url="https://cornucopia.owasp.org/rss">';
    body += "OWASP Cornucopia";
    body += "</source>";

    // Category
    for (let j = 0; j < post.tags.length; j++) {
      body += "<category>";
      body += post.tags[j].trim();
      body += "</category>";
    }

    // PubDate
    body += "<pubDate>";
    body += generateDate(post);
    body += "</pubDate>";

    body += "</item>";
  }

  body += bodyEnd;
  return new Response(body, responseInit);
}

function generateDescription(post: Blogpost) {
  let desc: string = post.description?.slice(0, 200)+ "...";
  return desc;
}

function generateDate(post: Blogpost): string {
  let date: string = post.date.toString();
  let year = date.slice(0, 4);
  let month = date.slice(4, 2);
  let day = date.slice(6, 2);

  let d: Date = new Date();
  d.setDate(Number.parseInt(day));
  d.setMonth(Number.parseInt(month));
  d.setFullYear(Number.parseInt(year));
  return d.toUTCString();
}

function generateLink(post: Blogpost): string {
  return "https://cornucopia.owasp.org/news/" + post.path;
}
