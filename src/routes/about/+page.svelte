<div>
    <h1 id="about">About</h1>
    <hr>
    <p>OWASP Cornucopia is a mechanism in the form of a card game to assist software development teams identify security requirements in Agile, conventional and formal development processes. It is language, platform and technology-agnostic.</p>
    <p>If you have questions concerning OWASP Cornucopia, please search for it first in our <a>Q & A section</a>.</p> 
    <p>If you have other questions, suggestions or ideas please feel free to discuss them on our <a href="https://groups.google.com/a/owasp.org/g/cornucopia-project" rel="nofollow">email list</a> 
    or submit them to our <a href="https://github.com/OWASP/cornucopia/issues">list of issues</a> in our repository.
    If you feel like and have the oportunity to help, do not hesitate to get in touch with us.</p>
    <section id="introduction">
        <a href="#introduction"><h2>Introduction</h2></a>
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
        <h3>How to start</h3>
        <p>To start using Cornucopia:</p>
        <ol>
            <li><b>Either</b> Obtain or buy a pre-printed deck of cards;</li>
            <li><b>Or:</b> Download the free Adobe Illustrator files and get them professionally printed (see: <a href="/printing">printing instructions</a>);</li>
            <li><b>Or:</b> Play the game online at <a rel="noopener" href="https://copi.owasp.org">copi.owasp.org</a>.</li>
            <li>Identify an application, module or component to assess.</li>
            <li>Invite business owners, architects, developers, testers along for a card game.</li>
            <li>Get those infosec folk to provide chocolate, pizza, beer, flowers or all four as prizes.</li>
            <li>Select a portion of the deck to start with.</li>
            <li><a href="/how-to-play">Play the game</a> to discuss & document security requirements (and to win rounds).</li>
            <li>Remember, to have fun!</li>
        </ol>
    </section>
    <section>
        <a href="#mappings"><h2>Mappings</h2></a>
        <p>The other driver for Cornucopia was to link the attacks with requirements and verification techniques. An initial aim had been to reference <a href="http://cwe.mitre.org/" rel="nofollow">CWE</a> weakness IDs, but these proved too numerous, and instead it was decided to map each card to <a href="http://capec.mitre.org/" rel="nofollow">CAPEC</a> software attack pattern IDs which themselves are mapped to CWEs, so the desired result is achieved.</p>
        <p>Each Website App Edition card is also mapped to the 36 primary security stories in the <a href="https://safecode.org/resource-secure-development-practices/fundamental-practices-secure-software-development-2/" rel="nofollow">SAFECode document</a>, as well as to the OWASP <a href="https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/" rel="nofollow">SCP</a> v2, <a href="https://owasp.org/www-project-application-security-verification-standard/" rel="nofollow">ASVS</a> v4.0.3 and <a href="https://owasp.org/www-project-appsensor/" rel="nofollow">AppSensor</a> (application attack detection and response) to help teams create their own security-related stories for use in Agile processes.</p>
        <p>Likewise, each Mobile App Edition is mapped to CAPEC and the SAFECode stories, but instead of SCP, ASVS and AppSensor, each card is mapped to OWASP's <a href="https://mas.owasp.org/MASVS/" rel="nofollow">Mobile Application Security Verification Standard (MASVS)</a> v2.0 and <a href="https://mas.owasp.org/MASTG/" rel="nofollow">Mobile Application Security Testing Guide (MASTG)</a> v2.0.</p>
    </section>
    <section id="gamification">
        <a href="#gamification"><h2>Other Security Gamification</h2></a>
        <p>If you are interested in using gaming for security, also see <a href="https://www.microsoft.com/en-gb/download/details.aspx?id=20303" rel="nofollow">Elevation of Privilege: The Threat Modeling Game</a>, <a href="http://securitycards.cs.washington.edu/" rel="nofollow">Security Cards</a> from the University of Washington, the commercial card game <a href="http://www.controlalthack.com/" rel="nofollow">Control-Alt-Hack</a> (<a href="http://www.youtube.com/watch?v=Kpnvsgiiz8s" rel="nofollow">presentation</a>), <a href="https://owasp.org/www-project-snakes-and-ladders" rel="nofollow">OWASP Snakes and Ladders</a>, <a href="https://owasp.org/www-project-cumulus/" rel="nofollow">OWASP Cumulus</a>, and web application security training tools incorporating gamification such as <a href="https://owasp.org/www-project-hackademic-challenges" rel="nofollow">OWASP Hackademic Challenges Project</a>, <a href="https://owasp.org/www-project-security-shepherd" rel="nofollow">OWASP Security Shepherd</a> and <a href="http://itsecgames.blogspot.co.uk/" rel="nofollow">ITSEC Games</a>.</p>
        <p>Additionally, Adam Shostack maintains a list of tabletop security games and related resources at <a href="https://shostack.org/games.html" rel="nofollow">Tabletop Security Games + Cards</a>.</p>
    </section>
    <section id="acknowledgements">
        <a href="#acknowledgements"><h2>Acknowledgements</h2></a>
        <h3>Volunteers</h3>
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
    </section>
    <section id="license">
        <a href="#license"><h2>License</h2></a>
    <p>
        Created by Colin Watson.<br>
        OWASP Cornucopia is open source and can be downloaded free of charge from the <a rel="noopener" href="https://github.com/OWASP/cornucopia/blob/master/README.md#license">Github repository</a>.<br>
        OWASP Cornucopia is free to use.<br>
        It is licensed under the Creative Commons Attribution-ShareAlike 3.0 license, so you can copy, distribute and transmit the work, and you can adapt it, and use it commercially, but all provided that you attribute the work and if you alter, transform, or build upon this work, you may distribute the resulting work only under the same or similar license to this one.<br>
        OWASP and the OWASP logo are trademarks of the OWASP Foundation
    </p>
    </section>
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
        padding-left : 1rem;
        width : 95%;
        margin: auto;
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