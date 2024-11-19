<div>
  <h1>How to play Cornucopia?</h1>
  <p>It is possible to play Cornucopia in many different ways. Here is one way explained in this Youtube video</p>
  <iframe src="https://www.youtube.com/embed/XXTPXozIHow?si=uIi_VXDtSBkS027S" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

  <h2>Primary method</h2>
  <ul>
    <li>A - Preparations
      <ul>
        <li>A1. Obtain a deck, or print your own Cornucopia deck and separate/cut out the cards</li>
        <li>A2. Identify an application or application process to review; this might be a concept, design or an actual implementation</li>
        <li>A3. Create a data flow diagram</li>
        <li>A4. Identify and invite a group of 3-6 architects, developers, testers and other business stakeholders together and sit around a table (try to include someone fairly familiar with application security)</li>
        <li>A5. Have some prizes to hand (gold stars, chocolate, pizza, beer or flowers depending upon your office culture). See our "Prizes and Swags" section for ideas.</li>
      </ul>
    </li>
    <li>B - Play
      <ul>One suit - Cornucopia - acts as trumps. Aces are high (i.e. they beat Kings). It helps if there is someone dedicated to documenting the results who is not playing.
        <li>B1. Remove the Jokers and a few low-score (2, 3, 4) cards from Cornucopia suit to ensure each player will have the same number of cards</li>
        <li>B2. Shuffle the pack and deal all the cards</li>
        <li>B3. To begin, choose a player randomly who will play the first card - they can play any card from their hand except from the trump suit - Cornucopia
        <li>B4. To play a card, each player must read it out aloud, and explain how (or not) the threat could apply (the player gets a point for attacks that work, and the group thinks it is an actionable bug) - don’t try to think of mitigations at this stage, and don’t exclude a threat just because it is believed it is already mitigated - someone record the card on the score sheet</li>
        <li>B5. Play clockwise, each person must play a card in the same way; if you have any card of the matching lead suit you must play one of those, otherwise they can play a card from any other suit. Only a higher card of the same suit, or the trump suit Cornucopia, wins the hand.</li>
        <li>B6. The person who wins the round, leads the next round (i.e. they play first), and thus defines the next lead suit</li>
        <li>B7. Repeat until all the cards are played</li>
      </ul>
    </li>
    <li>C - Scoring
      <ul>The objective is to identify applicable threats, and win hands (rounds):
        <li>C1. Score +1 for each card you can identify as a valid threat to the application under consideration</li>
        <li>C2. Score +1 if you win a round</li>
        <li>C3. Once all cards have been played, whoever has the most points wins</li>
      </ul>
    </li>
    <li>D - Closure
      <ul>
        <li>D1. Review all the applicable threats and the matching security requirements
        <li>D2. Create user stories, specifications and test cases as required for your development methodology
      </ul>
    </li>
  </ul>
  <p>
    See Márk Vinkovits leading a threat modelling <a href="https://www.youtube.com/watch?v=9dVDqeO6y3A&ab_channel=OWASPHU">talk and group session</a> playing Cornucopia in the OWASP track @hacktivityconf 1510.
  </p>
  <h2>Alternative game rules</h2>
  <p>
    If you are new to the game, remove the two Joker cards to begin with. Add the Joker cards back in once people become more familiar with the process. Apart from the “trumps card game” rules described above which are very similar to the EoP, the deck can also be played as the “twenty-one card game” (also known as “pontoon” or “blackjack”) which normally reduces the number of cards played in each round.
    <br/>Practice on an imaginary application, or even a future planned application, rather than trying to find fault with existing applications until the participants are happy with the usefulness of the game.
    <br/>Consider just playing with one suit to make a shorter session – but try to cover all the suits for every project. Or even better just play one hand with some pre-selected cards, and score only on the ability to identify security requirements. Perhaps have one game of each suit each day for a week or so, if the participants cannot spare long enough for a full deck.
    <br/>Some teams have preferred to play a full hand of cards, and then discuss what is on the cards after each round (instead of after each person plays a card).
    <br/>Another suggestion is that if a player fails to identify the card is relevant, allow other players to suggest ideas, and potentially let them gain the point for the card. Consider allowing extra points for especially good contributions.
    <br/>You can even play by yourself. Just use the cards to act as thought-provokers. Involving more people will be beneficial though.
    <br/>In Microsoft's EoP guidance, they recommend cheating as a good game strategy.
  </p>
</div>


  <style>
    h2
    {
        font-weight: bold;
    }
    h1,p,li
    {
      color:var(--background);
    }
    a,p,li
    {
        font-size: 1.3rem;
        font-family: var(--font-body);
        text-align: justify;
    }
    div
    {
        width : 50%;
        margin:auto;
        margin-top: 2rem;
    }

    iframe
    {
        width : 100%;
        height : 100%;
        min-height: 28.58rem;
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

    @media (max-aspect-ratio: 1/1) 
    {
       div
       {
        margin:auto;
        width : 90%;
       } 
    }
  </style>