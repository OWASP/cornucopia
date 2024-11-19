<div>
    <h1 id="about">About</h1>
    <h2>OWASP Cornucopia</h2>
    <p>
         The idea behind Cornucopia is to help development teams, especially those using Agile methodologies, to identify application security requirements and develop security-based user stories.
    <br/>Although the idea had been waiting for enough time to progress it, the final motivation came when <a href="http://www.safecode.org/">SAFECode</a> published its <a href="https://safecode.org/publication/SAFECode_Agile_Dev_Security0712.pdf">Practical Security Stories and Security Tasks for Agile Development Environments</a> in July 2012.
    <br/>Cornucopia was created and first used for developer training in August 2012.
    </p>
    <p>
         The Microsoft SDL team had already published its super <a href="https://www.microsoft.com/en-gb/download/details.aspx?id=20303">Elevation of Privilege: The Threat Modeling Game (EoP)</a> but that did not seem to address the most appropriate kind of issues that web application development teams mostly have to address.
    <br/>EoP is a great concept and game strategy, and was <a href="https://www.microsoft.com/security/blog/2010/03/02/announcing-elevation-of-privilege-the-threat-modeling-game/">published</a> under a <a href="http://creativecommons.org/licenses/by/3.0/">Creative Commons Attribution License</a>.
    <br/>Cornucopia is based the concepts and game ideas in EoP, but those have been modified to be more relevant to the types of issues website app and mobile app developers encounter. 
    <br/>It attempts to introduce threat-modelling ideas into development teams that use Agile methodologies, or are more focused on web application weaknesses than other types of software vulnerabilities or are not familiar with STRIDE and DREAD.
    </p>
    <h2 id="acknowledgements">Acknowledgements</h2>
    <h3 id="volunteers">Volunteers</h3>
    <p>
        Cornucopia is developed, maintained, updated and promoted by a worldwide team of volunteers. The contributors to date have been:
    </p>
    <ul>
        <li>Artim Banyte</li>    
        <li>Simon Bennetts</li>    
        <li>Thomas Berson</li>    
        <li>Tom Brennan</li>    
        <li>Graham Bryant</li>    
        <li>Fabio Cerullo</li>    
        <li>Oana Cornea</li> 
        <li>Johanna Curiel</li> 
        <li>Todd Dahl</li>
        <li>Ruggero DallAglio</li>
        <li>Luis Enriquez</li>
        <li>André Ferreira</li>
        <li>Ken Ferris</li> 
        <li>Darío De Filippis</li> 
        <li>Norbert Gaspar</li> 
        <li>Spyros Gasteratos</li> 
        <li>Sebastien Gioria</li> 
        <li>Xavier Godard</li> 
        <li>Tobias Gondrom</li> 
        <li>Timo Goosen</li>
        <li>Anthony Harrison</li> 
        <li>Martin Haslinger</li> 
        <li>John Herrlin</li> 
        <li>Jerry Hoff</li> 
        <li>Toby Irvine</li> 
        <li>Marios Kourtesis</li>
        <li>Franck Lacosta</li>
        <li>Mathias Lemaire</li>
        <li>Jim Manico</li> 
        <li>Mark Miller</li> 
        <li>Cam Morris</li> 
        <li>Grant Ongers</li> 
        <li>Susana Romaniz</li> 
        <li>Ravishankar Sahadevan</li> 
        <li>Tao Sauvage</li> 
        <li>Max Alejandro Gómez Sánchez Vergaray</li> 
        <li>Johan Sydseter</li> 
        <li>Wagner Voltz</li> 
        <li>Stephen de Vries</li> 
        <li>Colin Watson</li> 
    </ul>

    <p>
        Please let us know if we have missed anyone from this list.
    </p>
    <h3 id="others">Others</h3>
    <ul>
        <li>Adam Shostack and the Microsoft SDL Team for the Elevation of Privilege (EoP) Threat Modelling Game, published under a Creative Commons Attribution license, as the inspiration for Cornucopia and from which many ideas, especially the game theory, were copied.</li>    
        <li>Keith Turpin and contributors to the “OWASP Secure Coding Practices - Quick Reference Guide”, originally donated to OWASP by Boeing, which is used as the primary source of security requirements information to formulate the content of the cards.</li>    
        <li>Contributors, supporters, sponsors and volunteers to the OWASP ASVS, AppSensor, Web Framework Security Matrix and MASVS/MASTG projects, Mitre’s Common Attack Pattern Enumeration and Classification (CAPEC), and SAFECode’s “Practical Security Stories and Security Tasks for Agile Development Environments” which are all used in the cross-references provided.</li>    
        <li>Playgen for providing an illuminating afternoon seminar on task gamification, and tartanmaker.com for the online tool to help create the original card back pattern.</li>    
        <li>Blackfoot UK Limited for creating and donating print-ready design files, the OWASP Foundation for instigating the creation of an OWASP-branded box and leaflet, and Secure Delivery Ltd for developing and donating Copi, the platform to play Cornucopia and EoP online.</li>    
        <li>OWASP's hard-working employees.</li>    
        <li>Current and past OWASP Cornucopia project contributors.</li> 
        <li>Colin Watson as author of OWASP Cornucopia Ecommerce Edition, the original card deck.</li> 
    </ul>



    <h2 id="license">License</h2>
    <p>
        Created by Colin Watson.<br>
        OWASP Cornucopia is open source and can be downloaded free of charge from the <a rel="noopener" href="https://github.com/OWASP/cornucopia/blob/master/README.md#license">Github repository</a>.<br>
        OWASP Cornucopia is free to use.<br>
        It is licensed under the Creative Commons Attribution-ShareAlike 3.0 license, so you can copy, distribute and transmit the work, and you can adapt it, and use it commercially, but all provided that you attribute the work and if you alter, transform, or build upon this work, you may distribute the resulting work only under the same or similar license to this one.<br>
        OWASP and the OWASP logo are trademarks of the OWASP Foundation
    </p>

    <img alt="Logo of the OWASP foundation" src="/images/owasp-logo.png"/>
</div>

<style>
    h2,h3
    {
        font-weight: bold;
    }
    img
    {
        width : 60%;
        margin-left:20%;
    }

    div
    {
        padding : 2rem;
        width : 60%;
        margin: auto;
        margin-top: 2rem;
        font-size: 1.2rem;
    }
        @media (max-aspect-ratio: 1/1)
        {
            div
            {
                width : 100%;
            }

            img
            {
                width : calc(100% - 4rem);
                margin-left: 2rem
            }
        }
    a,p
    {
        font-size: 1.3rem;
        font-family: var(--font-body);
    }

    a
    {
        display: inline-block;
        text-decoration: none;
        font-weight: bold;
        color:var(--background);
    }

    a:hover
    {
        opacity: 70%;
        color: rgb(41, 0, 176);
    }
</style>