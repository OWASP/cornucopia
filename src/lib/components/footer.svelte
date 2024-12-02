<script lang="ts">
    import { onMount } from "svelte";

    export let timestamp : Date;
    let timeAgo : string = '';

    function doOnMount()
    {
        let hours : number =  getHoursSince(timestamp);

        if(hours < 1)
        {
            let minutes = Math.ceil(hours * 60);
            timeAgo = ', or ' + minutes + ' minutes ago'
        }
        else if(hours > 1 && hours < 2)
        {
            timeAgo = ', or 1 hour ago'
        }
        else
        {
            timeAgo = ', or ' + Math.ceil(hours) + ' hours ago'
        }
    }

    function getCurrentDate() : string
    {
        return timestamp.toUTCString() 
    }

    function getHoursSince(input : Date) : number
    {
        let now = new Date()
        let difference = Math.abs(now.getTime() - input.getTime());
        let differenceInHours = difference / (1000 * 3600);
        return differenceInHours;
    }

    onMount(doOnMount)
</script>

<footer>
    <div class="flex-container">
        <div class="box">
            <p class="title">OWASP Cornucopia</p>
            <p>
                OWASP Cornucopia is originally created by Colin Watson.
                <br/>It is open source and can be downloaded free of charge from the <a target='_blank' href="https://owasp.org/www-project-cornucopia/">OWASP repository</a>.
                <br/>It is licensed under the Creative Commons Attribution-ShareAlike 3.0 license, so you can copy, 
                distribute and transmit the work, and you can adapt it, and use it commercially, 
                but all provided that you attribute the work and if you alter, transform, 
                or build upon this work, 
                you may distribute the resulting work only under the same or similar license to this one.
                <br/>OWASP does not endorse or recommend commercial products or services.
                <br/>OWASP Cornucopia is licensed under the Creative Commons Attribution-ShareAlike 3.0 license and is © 2012-2024 OWASP Foundation.
            </p>
        </div>
        <div class="box">
            <p class="title">Get the cards</p>
            <p><a href="/webshop">Order online</a></p>
            <p><a href="/printing">Print your own</a></p>
        </div>

        <div class="box">
            <p class="title">Mappings</p>
            <p><a href="https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/">OWASP SCP</a></p>
            <p><a href="https://owasp.org/www-project-application-security-verification-standard/">OWASP ASVS</a></p>
            <p><a href="https://owasp.org/www-project-appsensor/">OWASP APPSENSOR</a></p>
            <p><a href="https://capec.mitre.org/">CAPEC</a></p>
            <p><a href="https://safecode.org/">SAFECODE</a></p>
        </div>
    </div>
    <p class="footer">OWASP and the OWASP logo are trademarks of the <a href="https://owasp.org/">OWASP Foundation</a></p>
    <p class="footer">Last update was {getCurrentDate()}{timeAgo}</p>
    <p class="footer"><a href="/about#license">Licensing information</a> | <a href="/about#acknowledgements">Acknowledgements</a> | <a href="/questionsandanswers">Q & A</a> | <a href="/roadmap">Roadmap</a></p>
    <p class="footer">
        <a href="https://owasp.org/">© OWASP Foundation</a> 
        <span> {new Date().getFullYear()} </span>
        <a href="/rss.xml"><img style="position:relative;top:3px;" height="15px" src="/images/rss.svg" alt="rss" /></a>
        <span> | </span>
        <a href="https://cornucopia.dotnetlab.eu/sitemap.xml">Sitemap</a>
    </p>
</footer>


<style>
    .footer
    {
        width : calc(100% - 2rem);
        text-align: center;
    }

    a
    {
        color:white;
        font-weight: bold;
        text-decoration: none;
        transition: var(--transition);
    }

    a:hover
    {
        opacity: 50%;
    }

    .title
    {
        font-size: 1.5rem;
        font-weight: bold;
    }

    p
    {
        color:var(--white);
        font-family: var(--font-body);
        margin-top:.5rem;
        margin-bottom:.5rem;
    }
    .box
    {
        margin:1rem;
        flex:1;
    }

    .flex-container
    {
        display: flex;
        flex-direction: row;
        align-items: stretch;

    }
    footer
    {
        border-top: 1px solid var(--white);
        width : calc(100% - 2rem);
        background-color: var(--background);
        padding: 1rem;
    }

    @media (max-aspect-ratio: 1/1) 
    {
        .flex-container
        {
            flex-direction: column;
        }

        .box
        {
            width : 90%;
            margin-bottom: 2rem;
        }
    }
</style>