<div>
    <h1>Questions & Answers</h1>
    <section id="copy">
        <a href="#copy"><h3>Can I copy or edit the game?</h3></a>
        <p>
            Yes of course. All OWASP materials are free to do with as you like provided you comply with the Creative Commons Attribution-ShareAlike 3.0 license. Perhaps if you create a new version, you might donate it to the OWASP Cornucopia Project?
        </p>
    </section>

    <section id="getinvolved">
        <a href="#getinvolved"><h3>How can I get involved?</h3></a>
        <p>
            If you have questions, suggestions or ideas, please feel free to discuss them on our <a href="https://groups.google.com/a/owasp.org/g/cornucopia-project" rel="nofollow">email list</a> 
    or submit them to our <a href="https://github.com/OWASP/cornucopia/issues">list of issues</a> in our repository.
    If you feel like and have the oportunity to help, do not hesitate to get in touch with us.
        </p>
    </section>

    <section id="attackers">
        <a href="#attackers"><h3>How were the attackers’ names chosen?</h3></a>
        <p>
            EoP begins every description with words like "An attacker can...". These have to be phrased as an attack but I was not keen on the anonymous terminology, wanting something more engaging, and therefore used personal names. These can be thought of as external or internal people or aliases for computer systems. But instead of just random names, I thought how they might reflect the OWASP community aspect. Therefore, apart from "Alice and Bob", the original Ecommerce Website Edition used the given (first) names of current and recent OWASP employees and Board members (assigned in no order), and then randomly selected the remaining 50 or so names from the current list of paying individual OWASP members. No name was used more than once, and where people had provided two personal names, we dropped one part to try to ensure no-one can be easily identified. Names were not deliberately allocated to any particular attack, defence or requirement. The cultural and gender mix simply reflects theses sources of names, and is not meant to be world-representative. Some names have been changed over the years to include some more recent project volunteers.
        </p>
    </section>

    <section id="images">
        <a href="#images"><h3>Why aren’t there any images on the card faces?</h3></a>
        <p>
            There is quite a lot of text on the cards, and the cross-referencing takes up space too. But it would be great to have additional design elements included.
            Please get in touch with us if you would like to contribute.
        </p>
    </section>

    <section id="ranking">
        <a href="#ranking"><h3>Are the attacks ranked by the number on the card?</h3></a>
        <p>
            Only approximately. The risk will be application and organisation dependent, due to varying security and compliance requirements, so your own severity rating may place the cards in some other order than the numbers on the cards.
        </p>
    </section>

    <section id="time">
        <a href="#time"><h3>How long does it take to play a round of cards using the full deck?</h3></a>
        <p>
            This depends upon the amount of discussion and how familiar the players are with application security concepts. But perhaps allow 1.5 to 2.0 hours for 4-6 people.
        </p>
    </section>

    <section id="who-plays">
        <a href="#who-plays"><h3>What sort of people should play the game?</h3></a>
        <p>
            Always try to have a mix of roles who can contribute alternative perspectives. But include someone who has a reasonable knowledge of application vulnerability terminology. Otherwise try to include a mix of architects, developers, testers and a relevant project manager or business owner.
        </p>
    </section>

    <section id="notes">
        <a href="#notes"><h3>Who should take notes and record scores?</h3></a>
        <p>
            It is better if that someone else, not playing the game, takes notes about the requirements identified and issues discussed. This could be used as training for a more junior developer, or performed by the project manager. Some organisations have made a recording to review afterwards when the requirements are written up more formally.
        </p>
    </section>

    <section id="full-deck">
        <a href="#full-deck"><h3>Should we always use the full deck of cards?</h3></a>
        <p>
            No. A smaller deck is quicker to play. Start your first game with only enough cards for two or three rounds. Always consider removing cards that are not appropriate at all of the target application or function being reviewed. For the first few times people play the game it is also usually better to remove the Aces and the two Jokers. It is also usual to play the game without any trumps suit until people are more familiar with the idea.
        </p>
    </section>

    <section id="invented-attack">
        <a href="#invented-attack"><h3>What should players do when they have an Ace card that says “invented a new X attack”?</h3></a>
        <p>
            The player can make up any attack they think is valid, but must match the suit of the card e.g. data validation and encoding). With players new to the game, it can be better to remove these to begin with.
        </p>
    </section>

    <section id="detailed-information">
        <a href="#detailed-information"><h3>I don’t understand what the attack means on each card - is there more detailed information?</h3></a>
        <p>
            Yes, please look up the card in our <a href="/cards">card browser</a> on this website. This site specificly created to help players understand each attack.
        </p>
    </section>
    <img alt="Logo of the OWASP foundation" src="/images/owasp-logo.png"/>
</div>

<style>
    h3
    {
        font-weight: bold;
        margin:0;
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