<table>
<thead>
<tr class="header">
<th><p><embed src="media/image1.emf" style="width:2.97233in;height:0.73566in" /></p>
<p><strong>Cornucopia</strong></p>
<p><strong>Ecommerce Website Edition</strong> <strong>v1.21-EN</strong></p>
<blockquote>
<p>OWASP Cornucopia is a mechanism to assist software development teams identify security requirements in Agile, conventional and formal development processes</p>
</blockquote>
<p>Author</p>
<p>Colin Watson</p>
<p>Project Leaders</p>
<p>Colin Watson and Darío De Filippis</p>
<p>Reviewers</p>
<p>Tom Brennan, Johanna Curiel and Timo Goosen</p>
<p>Acknowledgments</p>
<blockquote>
<p>Microsoft SDL Team for the Elevation of Privilege Threat Modelling Game, published under a Creative Commons Attribution license, as the inspiration for Cornucopia and from which many ideas, especially the game theory, were copied.</p>
<p>Keith Turpin and contributors to the “OWASP Secure Coding Practices - Quick Reference Guide”, originally donated to OWASP by Boeing, which is used as the primary source of security requirements information to formulate the content of the cards.</p>
<p>Contributors, supporters, sponsors and volunteers to the OWASP ASVS, AppSensor and Web Framework Security Matrix projects, Mitre’s Common Attack Pattern Enumeration and Classification (CAPEC), and SAFECode’s “Practical Security Stories and Security Tasks for Agile Development Environments” which are all used in the cross-references provided.</p>
<p>Playgen for providing an illuminating afternoon seminar on task gamification, and tartanmaker.com for the online tool to help create the card back pattern.</p>
<p>Blackfoot UK Limited for creating and donating print-ready design files, Tom Brennan and the OWASP Foundation for instigating the creation of an OWASP-branded box and leaflet, and OWASP employees, especially Kate Hartmann, for managing the ordering, stocking and despatch of printed card decks. Oana Cornea and other participants at the AppSec EU 2015 project summit for their help in creating the demonstration video. Colin Watson as author and co-project leader with Darío De Filippis, along with other OWASP volunteers (named on the last page) who have helped in many ways.</p>
</blockquote>
<p>OWASP does not endorse or recommend commercial products or services</p>
<p>© 2012-2018 OWASP Foundation</p>
<p>This document is licensed under the Creative Commons Attribution-ShareAlike 3.0 license</p></th>
<th><img src="media/image2.png" style="width:4.922in;height:7.20268in" /></th>
<th></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>Introduction</p>
<p>The idea behind Cornucopia is to help development teams, especially those using Agile methodologies, to identify application security requirements and develop security-based user stories. Although the idea had been waiting for enough time to progress it, the final motivation came when <a href="http://www.safecode.org/">SAFECode</a> published its Practical Security Stories and Security Tasks for Agile Development Environments in July 2012.</p>
<p>The Microsoft SDL team had already published its super Elevation of Privilege: The Threat Modeling Game (EoP) but that did not seem to address the most appropriate kind of issues that web application development teams mostly have to address. EoP is a great concept and game strategy, and was published under a <a href="http://creativecommons.org/licenses/by/3.0/">Creative Commons Attribution License</a>.</p>
<p>Cornucopia Ecommerce Website Edition is based the concepts and game ideas in EoP, but those have been modified to be more relevant to the types of issues ecommerce website developers encounter. It attempts to introduce threat-modelling ideas into development teams that use Agile methodologies, or are more focused on web application weaknesses than other types of software vulnerabilities or are not familiar with STRIDE and DREAD.</p>
<p>Cornucopia Ecommerce Website Edition is referenced as an information resource in the PCI Security Standard Council’s Information Supplement <a href="https://www.pcisecuritystandards.org/pdfs/PCI_DSS_v2_eCommerce_Guidelines.pdf">PCI DSS E-commerce Guidelines</a>, v2, January 2013.</p>
<p>The card deck (pack)</p>
<p>Instead of EoP’s STRIDE suits (sets of cards with matching designs), Cornucopia suits are based on the structure of the <a href="https://www.owasp.org/index.php/OWASP_Secure_Coding_Practices_-_Quick_Reference_Guide">OWASP Secure Coding Practices - Quick Reference Guide</a> (SCP), but with additional consideration of sections in the <a href="https://www.owasp.org/index.php/Category:OWASP_Application_Security_Verification_Standard_Project">OWASP Application Security Verification Standard</a>, the <a href="https://www.owasp.org/index.php/OWASP_Testing_Project">OWASP Testing Guide</a> and David Rook’s Principles of Secure Development. These provided five suits, and a sixth called “Cornucopia” was created for everything else:</p>
<ul>
<li><p>Data validation and encoding (VE)</p></li>
<li><p>Authentication (AT)</p></li>
<li><p>Session management (SM)</p></li>
<li><p>Authorization (AZ)</p></li>
<li><p>Cryptography (CR)</p></li>
<li><p>Cornucopia (C)</p></li>
</ul>
<p>Similar to poker-playing cards, each suit contains 13 cards (Ace, 2-10, Jack, Queen and King) but, unlike EoP, there are also two Joker cards. The content was mainly drawn from the SCP.</p>
<p>Mappings</p>
<p>The other driver for Cornucopia is to link the attacks with requirements and verification techniques. An initial aim had been to reference <a href="http://cwe.mitre.org/">CWE</a> weakness IDs, but these proved too numerous, and instead it was decided to map each card to <a href="http://capec.mitre.org/">CAPEC</a> software attack pattern IDs which themselves are mapped to CWEs, so the desired result is achieved.</p>
<p>Each card is also mapped to the 36 primary security stories in the SAFECode document, as well as to the OWASP SCP v2, ASVS v3.0.1 and <a href="https://www.owasp.org/index.php/OWASP_AppSensor_Project">AppSensor</a> (application attack detection and response) to help teams create their own security-related stories for use in Agile processes.</p></td>
<td></td>
<td><p>Game strategy</p>
<p>Apart from the content differences, the game rules are virtually identical to <a href="http://social.technet.microsoft.com/wiki/contents/articles/285.elevation-of-privilege-the-game.aspx">those for EoP</a>.</p>
<p>Printing the cards</p>
<p>Check the Cornucopia project page for how to obtain pre-printed decks on glossy card.</p>
<p>The cards can be printed from this document in black &amp; white but are more effective in color. The cards in the later pages of this document have been laid out to fit on one type of pre-scored business A4 card sheets. This appeared to be the quickest way to initially provide to create playing cards quickly. Avery product codes C32015 and C32030 have been tested successfully, but any 10 up 85mm x 54 mm cards on A4 paper should work with a little adjustment. Other stationery suppliers like Ryman and Sigel produce similar sheets. These card sheets are not inexpensive, so care should be taken in deciding what to print and using what media and printer type.</p>
<p>The cards can of course just be printed on any size of paper or card and then cut-up manually, or a commercial printer would be able to print larger volumes and cut the cards to size. The cut lines are shown on the penultimate page of this document, but Avery also produce a landscape A4 templates that can be used as a guide.</p>
<p>Printing and cutting up can take an hour or so, and using a faster printer helps. Try to print add higher quality to increase legibility. An optional card back design (in OWASP tartan) has been provided as the last page of this document. There is no special alignment needed. Dual-sided printing needs special care taken. You could customize the card faces or the backs for your own organization’s preferences.</p>
<p>Customization</p>
<p>After you have used Cornucopia a few times, you may feel that some cards are less relevant to your applications, or the threats are different for your organization. Edit this document yourself to make the cards more suitable for your teams, or create new decks completely.</p>
<p>Provide feedback</p>
<p>If you have ideas or feedback on the use of OWASP Cornucopia, please share them. Even better if you create alternative versions of the cards, or produce professional print-ready versions, please share that with the volunteers who created this edition and with the wider application development and application security community.</p>
<p>The best place to use to discuss or contribute is the mailing list for the OWASP project:</p>
<ul>
<li><p>Mailing list<br />
<a href="https://lists.owasp.org/mailman/listinfo/owasp_cornucopia">https://lists.owasp.org/mailman/listinfo/owasp_cornucopia</a></p></li>
<li><p>Project home page<br />
<a href="https://www.owasp.org/index.php/OWASP_Cornucopia">https://www.owasp.org/index.php/OWASP_Cornucopia</a></p></li>
</ul>
<p>All OWASP documents and tools are free to download and use. OWASP Cornucopia is licensed under the Creative Commons Attribution-ShareAlike 3.0 license.</p></td>
</tr>
</tbody>
</table>

<table>
<tbody>
<tr class="odd">
<td><p>Instructions</p>
<p>The text on each card describes an attack, but the attacker is given a name, which are unique across all the cards. The name can represent a computer system (e.g. the database, the file system, another application, a related service, a botnet), an individual person (e.g. a citizen, a customer, a client, an employee, a criminal, a spy), or even a group of people (e.g. a competitive organization, activists with a common cause). The attacker might be remote in some other device/location, or local/internal with access to the same device, host or network as the application is running on. The attacker is always named at the start of each description. An example is:</p>
<blockquote>
<p><em>William has control over the generation of session identifiers</em></p>
</blockquote>
<p>This means the attacker (William) can create new session identifiers that the application accepts. The attacks were primarily drawn from the security requirements listed in the SCP, v2 but then supplemented with verification objectives from the OWASP “Application Security Verification Standard for Web Applications”, the security focused stories in SAFECode’s “Practical Security Stories and Security Tasks for Agile Development Environments”, and finally a review of the cards in EOP.</p>
<p>Further guidance about each card is available in the online Wiki Deck at <a href="https://www.owasp.org/index.php/Cornucopia_-_Ecommerce_Website_Edition_-_Wiki_Deck">https://www.owasp.org/index.php/Cornucopia_-_Ecommerce_Website_Edition_-_Wiki_Deck</a></p>
<p>Lookups between the attacks and five resources are provided on most cards:</p>
<ul>
<li><p>Requirements in “Secure Coding Practices (SCP) - Quick Reference Guide”, v2, OWASP, November 2010<br />
<a href="https://www.owasp.org/index.php/File:OWASP_SCP_Quick_Reference_Guide_v2.pdf">https://www.owasp.org/index.php/File:OWASP_SCP_Quick_Reference_Guide_v2.pdf</a></p></li>
<li><p>Verification IDs in “Application Security Verification Standard (ASVS) for Web Applications”, OWASP, v3.0.1, 2016 (excluding sections 18 and 19)<br />
<a href="https://www.owasp.org/images/3/33/OWASP_Application_Security_Verification_Standard_3.0.1.pdf">https://www.owasp.org/images/3/33/OWASP_Application_Security_Verification_Standard_3.0.1.pdf</a></p></li>
<li><p>Attack detection points IDs in “AppSensor”, OWASP, August 2010-2015<br />
<a href="https://www.owasp.org/index.php/AppSensor_DetectionPoints">https://www.owasp.org/index.php/AppSensor_DetectionPoints</a></p></li>
<li><p>IDs in “Common Attack Pattern Enumeration and Classification (CAPEC)”, v2.8, Mitre Corporation, November 2015<br />
<a href="http://capec.mitre.org/data/archive/capec_v2.8.zip">http://capec.mitre.org/data/archive/capec_v2.8.zip</a></p></li>
<li><p>Security-focused stories in "Practical Security Stories and Security Tasks for Agile Development Environments", SAFECode, July 2012<br />
http://safecode.org/publication/SAFECode_Agile_Dev_Security0712.pdf</p></li>
</ul>
<p>A look-up means the attack is included within the referenced item, but does not necessarily encompass the whole of its intent. For structured data like CAPEC, the most specific reference is provided but sometimes a cross-reference is provided that also has more specific (child) examples. There are no lookups on the six Aces and two Jokers. Instead these cards have some general tips in italicized text.</p>
<p>It is possible to play Cornucopia in many different ways. Here is one way, demonstrated online in a video at <a href="https://youtu.be/i5Y0akWj31k">https://youtu.be/i5Y0akWj31k</a>, which uses the new (May 2015) score/record sheet at <a href="https://www.owasp.org/index.php/File:Cornucopia-scoresheet.pdf">https://www.owasp.org/index.php/File:Cornucopia-scoresheet.pdf</a></p></td>
<td></td>
<td><p>A - Preparations</p>
<ol type="1">
<li><p>Obtain a deck, or print your own deck of Cornucopia cards (see page 2 of this document) and separate/cut out the cards</p></li>
<li><p>Identify an application or application process to review; this might be a concept, design or an actual implementation</p></li>
<li><p>Create a data flow diagram, user stories, or other artefacts to help the review</p></li>
<li><p>Identify and invite a group of 3-6 architects, developers, testers and other business stakeholders together and sit around a table (try to include someone fairly familiar with application security)</p></li>
<li><p>Have some prizes to hand (gold stars, chocolate, pizza, beer or flowers depending upon your office culture)</p></li>
</ol>
<p>B - Play</p>
<p>One suit - <em>Cornucopia</em> - acts as trumps. Aces are high (i.e. they beat Kings). It helps if there is a non-player to document the issues and scores..</p>
<ol type="1">
<li><p>Remove the Jokers and a few low-score (2, 3, 4) cards from <em>Cornucopia</em> suit to ensure each player will have the same number of cards</p></li>
<li><p>Shuffle the deck and deal all the cards</p></li>
<li><p>To begin, choose a player randomly who will play the first card - they can play any card from their hand except from the trump suit - <em>Cornucopia</em></p></li>
<li><p>To play a card, each player must read it out aloud, and explain (see the online Wiki Deck for tips) how the threat could apply (the player gets a point for attacks that might work which the group thinks is an actionable bug) - do not try to think of mitigations at this stage, and do not exclude a threat just because of a belief that it is already mitigated - someone note the card and record the issues raised</p></li>
<li><p>Play clockwise, each person must play a card in the same way; if you have any card of the matching lead suit you must play one of those, otherwise they can play a card from any other suit. Only a higher card of the same suit, or the highest card in the trump suit <em>Cornucopia</em>, wins the hand</p></li>
<li><p>The person who wins the round, leads the next round (i.e. they play first), and thus defines the next lead suit</p></li>
<li><p>Repeat until all the cards are played</p></li>
</ol>
<p>C - Scoring</p>
<p>The objective is to identify applicable threats, and win hands (rounds):</p>
<ol type="1">
<li><p>Score +1 for each card you can identify as a valid threat to the application under consideration</p></li>
<li><p>Score +1 if you win a round</p></li>
<li><p>Once all cards have been played, whoever has the most points wins</p></li>
</ol>
<p>D - Closure</p>
<ol type="1">
<li><p>Review all the applicable threats and the matching security requirements</p></li>
<li><p>Create user stories, specifications and test cases as required for your development methodology.</p></li>
</ol></td>
</tr>
</tbody>
</table>

<table>
<tbody>
<tr class="odd">
<td><p>Alternative game rules</p>
<p>If you are new to the game, remove the Aces and two Joker cards to begin with. Add the Joker cards back in once people become more familiar with the process. Apart from the “trumps card game” rules described above which are very similar to the EoP, the deck can also be played as the “twenty-one card game” (also known as “pontoon” or “blackjack”) which normally reduces the number of cards played in each round.</p>
<p>Practice on an imaginary application, or even a future planned application, rather than trying to find fault with existing applications until the participants are happy with the usefulness of the game.</p>
<p>Consider just playing with one suit to make a shorter session – but try to cover all the suits for every project. Or even better just play one hand with some pre-selected cards, and score only on the ability to identify security requirements. Perhaps have one game of each suit each day for a week or so, if the participants cannot spare long enough for a full deck.</p>
<p>Some teams have preferred to play a full hand of cards, and then discuss what is on the cards after each round (instead of after each person plays a card).</p>
<p>Another suggestion is that if a player fails to identify the card is relevant, allow other players to suggest ideas, and potentially let them gain the point for the card. Consider allowing extra points for especially good contributions.</p>
<p>You can even play by yourself. Just use the cards to act as thought-provokers. Involving more people will be beneficial though.</p>
<p>In Microsoft's EoP guidance, they recommend cheating as a good game strategy.</p>
<p>Development framework-specific modified card decks</p>
<p>At the end of 2012, the <a href="https://www.owasp.org/index.php/Category:Framework_Security_Matrix">OWASP Framework Security Matrix</a> was published which documents built in security controls in some commonly used languages and frameworks for web and mobile application development. With certain provisos it is useful to consider how using these controls can simplify the identification of additional requirements – provided of course the controls are included, enabled and configured correctly.</p>
<p>Consider removing the following cards from the decks if you are confidence they are addressed by the way you are using the language/framework. Items in parentheses are “maybes”.</p></td>
<td></td>
<td><p>Internal coding standards and libraries</p>
<p>Add your own list of excluded cards based on your organisation’s coding standards (provided they are confirmed by appropriate verification steps in the development lifecycle).</p>
<table>
<thead>
<tr class="header">
<th>Your coding standards and libraries</th>
<th></th>
<th></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>Data validation and encoding</p>
<p><em>[your list]</em></p>
<p>Authentication</p>
<p><em>[your list]</em></p></td>
<td><p>Session management</p>
<p><em>[your list]</em></p>
<p>Authorization</p>
<p><em>[your list]</em></p></td>
<td><p>Cryptography</p>
<p><em>[your list]</em></p>
<p>Cornucopia</p>
<p><em>[your list]</em></p></td>
</tr>
</tbody>
</table>
<p>Compliance requirement decks</p>
<p>Create a smaller deck by only including cards for a particular compliance requirement.</p>
<table>
<thead>
<tr class="header">
<th>Compliance requirement</th>
<th></th>
<th></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>Data validation and encoding</p>
<p><em>[compliance list]</em></p>
<p>Authentication</p>
<p><em>[compliance list]</em></p></td>
<td><p>Session management</p>
<p><em>[compliance list]</em></p>
<p>Authorization</p>
<p><em>[compliance list]</em></p></td>
<td><p>Cryptography</p>
<p><em>[compliance list]</em></p>
<p>Cornucopia</p>
<p><em>[compliance list]</em></p></td>
</tr>
</tbody>
</table>
<p>International versions of Cornucopia</p>
<p>Cornucopia is available in the following languages:</p>
<ul>
<li><p>EN<br />
https://www.owasp.org/index.php/File:OWASP-Cornucopia-Ecommerce_Website.docx</p></li>
<li><p>FR<br />
https://github.com/grandtom/OWASP-Cornucopia-Translate-Cards---FR</p></li>
<li><p>PT-BR<br />
https://github.com/wagnerfusca/OWASP-Cornucopia-Translate-Cards---PT</p></li>
</ul></td>
</tr>
</tbody>
</table>

<table>
<tbody>
<tr class="odd">
<td></td>
<td></td>
<td><p><a href="https://www.owasp.org/index.php/Cornucopia_-_Ecommerce_Website_Edition_-_Wiki_Deck">https://www.owasp.org/index.php/Cornucopia_-_Ecommerce_Website_Edition_-_Wiki_Deck</a></p>
<p><a href="https://www.owasp.org/index.php/OWASP_Cornucopia#tab=FAQs">https://www.owasp.org/index.php/OWASP_Cornucopia - tab=FAQs</a></p></td>
</tr>
</tbody>
</table>

<table>
<tbody>
<tr class="odd">
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr class="even">
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr class="odd">
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td><table>
<tbody>
<tr class="odd">
<td></td>
</tr>
<tr class="even">
<td></td>
</tr>
<tr class="odd">
<td></td>
</tr>
<tr class="even">
<td></td>
</tr>
<tr class="odd">
<td><a href="https://github.com/grandtom/OWASP-Cornucopia-Translate-Cards---FR"><br />
Frequently asked questions<em>1. Can I copy or edit the game?<br />
</em>Yes of course. All OWASP materials are free to do with as you like provided you comply with the Creative Commons Attribution-ShareAlike 3.0 license. Perhaps if you create a new version, you might donate it to the OWASP Cornucopia Project?<em>2. How can I get involved?</em><br />
Please send ideas or offers of help to the project’s mailing list.<em>3. How were the attackers’ names chosen?</em><br />
EoP begins every description with words like "An attacker can...". These have to be phrased as an attack but I was not keen on the anonymous terminology, wanting something more engaging, and therefore used personal names. These can be thought of as external or internal people or aliases for computer systems. But instead of just random names, I thought how they might reflect the OWASP community aspect. Therefore, apart from "Alice and Bob", I use the given (first) names of current and recent OWASP employees and Board members (assigned in no order), and then randomly selected the remaining 50 or so names from the current list of paying individual OWASP members. No name was used more than once, and where people had provided two personal names, I dropped one part to try to ensure no-one can be easily identified. Names were not deliberately allocated to any particular attack, defence or requirement. The cultural and gender mix simply reflects theses sources of names, and is not meant to be world-representative. In v1.20, the name on VE-10 changed to reflect the project’s new co-leader - this card is also the only one with two names in the attack.<em>4. Why aren’t there any images on the card faces?</em><br />
There is quite a lot of text on the cards, and the cross-referencing takes up space too. But it would be great to have additional design elements included. Any volunteer<em>5. Are the attacks ranked by the number on the card?</em><br />
Only approximately. The risk will be application and organisation dependent, due to varying security and compliance requirements, so your own severity rating may place the cards in some other order than the numbers on the cards.<em>6. How long does it take to play a round of cards using the full deck?</em><br />
This depends upon the amount of discussion and how familiar the players are with application security concepts. But perhaps allow 1.5 to 2.0 hours for 4-6 people.<em>7. What sort of people should play the game?</em><br />
Always try to have a mix of roles who can contribute alternative perspectives. But include someone who has a reasonable knowledge of application vulnerability terminology. Otherwise try to include a mix of architects, developers, testers and a relevant project manager or business owner.<em>8. Who should take notes and record scores?</em><br />
It is better if that someone else, not playing the game, takes notes about the requirements identified and issues discussed. This could be used as training for a more junior developer, or performed by the project manager. Some organisations have made a recording to review afterwards when the requirements are written up more formally.<em>9. Should we always use the full deck of cards?</em><br />
No. A smaller deck is quicker to play. Start your first game with only enough cards for two or three rounds. Always consider removing cards that are not appropriate at all of the target application or function being reviewed. For the first few times people play the game it is also usually better to remove the Aces and the two Jokers. It is also usual to play the game without any trumps suit until people are more familiar with the idea.<em>10. What should players do when they have an Ace card that says “invented a new X attack”?<br />
</em>The player can make up any attack they think is valid, but must match the suit of the card e.g. data validation and encoding). With players new to the game, it can be better to remove these to begin with (see also FAQ 9).<em>11. I don’t understand what the attack means on each card - is there more detailed information?<br />
</em>Yes, the online Wiki Deck at was created to help players understand the attacks. See <em>12. My company wants to print its own version of OWASP Cornucopia - what license do we need to refer to?<br />
</em>Please refer to the full answer to this question on the project’s web pages at<br />
<br />
<strong><span class="smallcaps">Data Validation &amp; Encoding</span>A<span class="smallcaps">Data Validation &amp; EncodingData Validation &amp; Encoding</span>2<span class="smallcaps">Data Validation &amp; Encoding</span>3</strong>You have invented a new attack against Data Validation and Encoding(no card)Brian can gather information about the underlying configurations, schemas, logic, code, software, services and infrastructure due to the content of error messages, or poor configuration, or the presence of default installation files or old, test, backup or copies of resources, or exposure of source codeRobert can input malicious data because the allowed protocol format is not being checked, or duplicates are accepted, or the structure is not being verified, or the individual data elements are not being validated for format, type, range, length and a whitelist of allowed characters or formats<em>Read more about this topic in OWASP’s free Cheat Sheets on Input Validation, XSS Prevention, DOM-based XSS Prevention, SQL Injection Prevention, and Query Parameterization</em><span class="smallcaps">OWASP SCP</span>69, 107-109, 136, 137, 153, 156, 158, 162OWASP ASVS1.10, 4.5, 8.1, 11.5, 19.1, 19.5OWASP AppSensorHT1-3CAPEC54, 541<span class="smallcaps">SAFECode</span>4, 23OWASP Cornucopia Ecommerce Website Edition</a> v1.20-EN</td>
</tr>
</tbody>
</table></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>8, 9, 11-14, 16, 159, 190, 191</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>5.1, 5.16, 5.17, 5.18, 5.19, 5.20, 11.1, 11.2</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>RE7-8, AE4-7, IE2-3,CIE1,CIE3-4,HT1-3</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>28,48,126,165,213,220,221,261,262,271,272</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>3, 16, 24, 35</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
</tr>
<tr class="even">
<td></td>
<td><blockquote>
<p><strong><span class="smallcaps">Data Validation &amp; Encoding</span></strong></p>
</blockquote></td>
<td><strong>4</strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Data Validation &amp; Encoding</span></strong></p>
</blockquote></td>
<td><strong>5</strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Data Validation &amp; Encoding</span></strong></p>
</blockquote></td>
<td><strong>6</strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Data Validation &amp; Encoding</span></strong></p>
</blockquote></td>
<td><strong>7</strong></td>
</tr>
<tr class="odd">
<td></td>
<td></td>
<td>Dave can input malicious field names or data because it is not being checked within the context of the current user and process</td>
<td></td>
<td>Jee can bypass the centralized encoding routines since they are not being used everywhere, or the wrong encodings are being used</td>
<td></td>
<td>Jason can bypass the centralized validation routines since they are not being used on all inputs</td>
<td></td>
<td>Jan can craft special payloads to foil input validation because the character set is not specified/enforced, or the data is encoded multiple times, or the data is not fully converted into the same format the application uses (e.g. canonicalization) before being validated, or variables are not strongly typed</td>
</tr>
<tr class="even">
<td></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>8, 10, 183</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>4.16, 5.16, 5.17, 15.1</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>RE3-6,AE8-11,SE1,3-6,IE2-4,HT1-3</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>28, 31, 48, 126, 162, 165, 213, 220, 221,261</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>24, 35</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>3, 15, 18-22 168</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>1.7, 5.15, 5.21, 5.22, 5.23</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>-</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>28, 31, 152, 160, 468</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>2, 17</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>3, 168</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>1.7, 5.6, 5.19</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>IE2-3</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>28</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>3, 16, 24</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>4, 5, 7, 150</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>5.6, 11.8</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>IE2-3, EE1-2</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>28, 153, 165</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>3, 16, 24</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
</tr>
</tbody>
</table>

<table>
<tbody>
<tr class="odd">
<td></td>
<td><blockquote>
<p><strong><span class="smallcaps">Data Validation &amp; Encoding</span></strong></p>
</blockquote></td>
<td><strong>8</strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Data Validation &amp; Encoding</span></strong></p>
</blockquote></td>
<td><strong>9</strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Data Validation &amp; Encoding</span></strong></p>
</blockquote></td>
<td><strong>10</strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Data Validation &amp; Encoding</span></strong></p>
</blockquote></td>
<td><strong>J</strong></td>
</tr>
<tr class="even">
<td></td>
<td></td>
<td>Sarah can bypass the centralized sanitization routines since they are not being used comprehensively</td>
<td></td>
<td>Shamun can bypass input validation or output validation checks because validation failures are not rejected and/or sanitized</td>
<td></td>
<td>Darío can exploit the trust the application places in a source of data (e.g. user-definable data, manipulation of locally stored data, alteration to state data on a client device, lack of verification of identity during data validation such as Darío can pretend to be Colin)</td>
<td></td>
<td>Dennis has control over input validation, output validation or output encoding code or routines so they can be bypassed</td>
</tr>
<tr class="odd">
<td></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>15, 169</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>1.7, 5.21, 5.23</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>-</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>28, 31, 152, 160, 468</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>2, 17</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>6, 21, 22, 168</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>5.3</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>IE2-3</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>28</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>3, 16, 24</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>2, 19, 92, 95, 180</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>5.19, 10.6, 16.2, 16.3, 16.4, 16.5, 16.8</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>IE4, IE5</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>12, 51, 57, 90,111,145,194,195,202,218,463</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>14</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>1, 17</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>5.5, 5.18</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>RE3, RE4</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>87, 207, 554</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>2, 17</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
</tr>
<tr class="even">
<td></td>
<td><blockquote>
<p><strong><span class="smallcaps">Data Validation &amp; Encoding</span></strong></p>
</blockquote></td>
<td><strong>Q</strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Data Validation &amp; Encoding</span></strong></p>
</blockquote></td>
<td><strong>K</strong></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr class="odd">
<td></td>
<td></td>
<td>Geoff can inject data into a client or device side interpreter because a parameterised interface is not being used, or has not been implemented correctly, or the data has not been encoded correctly for the context, or there is no restrictive policy on code or data includes</td>
<td></td>
<td>Gabe can inject data into an server-side interpreter (e.g. SQL, OS commands, Xpath, Server JavaScript, SMTP) because a strongly typed parameterised interface is not being used or has not been implemented correctly</td>
<td></td>
<td>(no card)</td>
<td></td>
<td>(no card)</td>
</tr>
<tr class="even">
<td></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>10, 15, 16, 19, 20</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>5.15, 5.22, 5.23, 5.24, 5.25</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>IE1, RP3</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>28, 31, 152, 160, 468</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>2, 17</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>15, 19-22, 167, 180, 204, 211, 212</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>5.10, 5.11, 5.12, 5.13, 5.14, 5.16, 5.21</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>CIE1-2</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>23, 28, 76, 152, 160, 261</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>2, 19, 20</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
</tbody>
</table>

<table>
<tbody>
<tr class="odd">
<td></td>
<td><blockquote>
<p><strong><span class="smallcaps">Authentication</span></strong></p>
</blockquote></td>
<td><strong>A</strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Authentication</span></strong></p>
</blockquote></td>
<td></td>
<td><blockquote>
<p><strong><span class="smallcaps">Authentication</span></strong></p>
</blockquote></td>
<td><strong>2</strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Authentication</span></strong></p>
</blockquote></td>
<td><strong>3</strong></td>
</tr>
<tr class="even">
<td></td>
<td></td>
<td>You have invented a new attack against Authentication</td>
<td></td>
<td>(no card)</td>
<td></td>
<td>James can undertake authentication functions without the real user ever being aware this has occurred (e.g. attempt to log in, log in with stolen credentials, reset the password)</td>
<td></td>
<td>Muhammad can obtain a user's password or other secrets such as security questions, by observation during entry, or from a local cache, or from memory, or in transit, or by reading it from some unprotected location, or because it is widely known, or because it never expires, or because the user cannot change her own password</td>
</tr>
<tr class="odd">
<td></td>
<td></td>
<td><p><em>Read more about this topic in OWASP’s free</em></p>
<p><em>Authentication Cheat Sheet</em></p></td>
<td></td>
<td></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>47, 52</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>2.12, 8.4, 8.10</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>UT1</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>-</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>28</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>36-7, 40, 43, 48, 51, 119, 139-40, 146</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>2.2, 2.17, 2.24, 8.7, 9.1, 9.4, 9.5, 9.9, 9.11</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>-</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>37, 546</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>28</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
</tr>
<tr class="even">
<td></td>
<td><blockquote>
<p><strong><span class="smallcaps">Authentication</span></strong></p>
</blockquote></td>
<td><strong>4</strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Authentication</span></strong></p>
</blockquote></td>
<td><strong>5</strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Authentication</span></strong></p>
</blockquote></td>
<td><strong>6</strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Authentication</span></strong></p>
</blockquote></td>
<td><strong>7</strong></td>
</tr>
<tr class="odd">
<td></td>
<td></td>
<td>Sebastien can easily identify user names or can enumerate them</td>
<td></td>
<td>Javier can use default, test or easily guessable credentials to authenticate, or can use an old account or an account not necessary for the application</td>
<td></td>
<td>Sven can reuse a temporary password because the user does not have to change it on first use, or it has too long or no expiry, or it does not use an out-of-band delivery method (e.g. post, mobile app, SMS)</td>
<td></td>
<td>Cecilia can use brute force and dictionary attacks against one or many accounts without limit, or these attacks are simplified due to insufficient complexity, length, expiration and re-use requirements for passwords</td>
</tr>
<tr class="even">
<td></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>33, 53</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>2.18, 2.28</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>AE1</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>383</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>28</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>54, 175, 178</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>2.19</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>AE12, HT3</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>70</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>28</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>37, 45, 46, 178</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>2.22</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>-</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>50</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>28</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>33, 38, 39, 41, 50, 53</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>2.7, 2.20, 2.23, 2.25, 2.27</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>AE2, AE3</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>2, 16</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>27</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
</tr>
</tbody>
</table>

<table>
<tbody>
<tr class="odd">
<td></td>
<td><blockquote>
<p><strong><span class="smallcaps">Authentication</span></strong></p>
</blockquote></td>
<td><strong>8</strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Authentication</span></strong></p>
</blockquote></td>
<td><strong>9</strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Authentication</span></strong></p>
</blockquote></td>
<td><strong>10</strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Authentication</span></strong></p>
</blockquote></td>
<td><strong>J</strong></td>
</tr>
<tr class="even">
<td></td>
<td></td>
<td>Kate can bypass authentication because it does not fail secure (i.e. it defaults to allowing unauthenticated access)</td>
<td></td>
<td>Claudia can undertake more critical functions because authentication requirements are too weak (e.g. do not use strong authentication such as two factor), or there is no requirement to re-authenticate for these</td>
<td></td>
<td>Pravin can bypass authentication controls because a centralized standard, tested, proven and approved authentication module/framework/service, separate to the resource being requested, is not being used</td>
<td></td>
<td>Mark can access resources or services because there is no authentication requirement, or it was mistakenly assumed authentication would be undertaken by some other system or performed in some previous action</td>
</tr>
<tr class="odd">
<td></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>28</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>2.6</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>-</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>115</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>28</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>55, 56</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>2.1, 2.9, 2.26, 2.31, 4.15</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>-</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>21</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>14, 28</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>25, 26, 27</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>1.7, 2.30</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>-</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>90, 115</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>14, 28</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>23, 32, 34</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>2.1</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>-</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>115</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>14, 28</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
</tr>
<tr class="even">
<td></td>
<td><blockquote>
<p><strong><span class="smallcaps">Authentication</span></strong></p>
</blockquote></td>
<td><strong>Q</strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Authentication</span></strong></p>
</blockquote></td>
<td><strong>K</strong></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr class="odd">
<td></td>
<td></td>
<td>Jaime can bypass authentication because it is not enforced with equal rigor for all types of authentication functionality (e.g. register, password change, password recovery, log out, administration) or across all versions/channels (e.g. mobile website, mobile app, full website, API, call centre)</td>
<td></td>
<td>Olga can influence or alter authentication code/routines so they can be bypassed</td>
<td></td>
<td>(no card)</td>
<td></td>
<td>(no card)</td>
</tr>
<tr class="even">
<td></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>23, 29, 42, 49</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>2.1, 2.8</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>-</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>36, 50, 115, 121, 179</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>14, 28</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>24</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>2.4, 13.2</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>-</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>115, 207, 554</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>14, 28</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
</tbody>
</table>

<table>
<tbody>
<tr class="odd">
<td></td>
<td><blockquote>
<p><strong><span class="smallcaps">Session Management</span></strong></p>
</blockquote></td>
<td><strong>A</strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Session Management</span></strong></p>
</blockquote></td>
<td></td>
<td><blockquote>
<p><strong><span class="smallcaps">Session Management</span></strong></p>
</blockquote></td>
<td><strong>2</strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Session Management</span></strong></p>
</blockquote></td>
<td><strong>3</strong></td>
</tr>
<tr class="even">
<td></td>
<td></td>
<td>You have invented a new attack against Session Management</td>
<td></td>
<td>(no card)</td>
<td></td>
<td>William has control over the generation of session identifiers</td>
<td></td>
<td>Ryan can use a single account in parallel since concurrent sessions are allowed</td>
</tr>
<tr class="odd">
<td></td>
<td></td>
<td><em>Read more about this topic in OWASP’s free Cheat Sheets on Session Management, and Cross Site Request Forgery (CSRF) Prevention</em></td>
<td></td>
<td></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>58, 59</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>3.10</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>SE2</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>31, 60, 61</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>28</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>68</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>3.16, 3.17, 3.18</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>-</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>-</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>28</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
</tr>
<tr class="even">
<td></td>
<td><blockquote>
<p><strong><span class="smallcaps">Session Management</span></strong></p>
</blockquote></td>
<td><strong>4</strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Session Management</span></strong></p>
</blockquote></td>
<td><strong>5</strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Session Management</span></strong></p>
</blockquote></td>
<td><strong>6</strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Session Management</span></strong></p>
</blockquote></td>
<td><strong>7</strong></td>
</tr>
<tr class="odd">
<td></td>
<td></td>
<td>Alison can set session identification cookies on another web application because the domain and path are not restricted sufficiently</td>
<td></td>
<td>John can predict or guess session identifiers because they are not changed when the user's role alters (e.g. pre and post authentication) and when switching between non-encrypted and encrypted communications, or are not sufficiently long and random, or are not changed periodically</td>
<td></td>
<td>Gary can take over a user's session because there is a long or no inactivity timeout, or a long or no overall session time limit, or the same session can be used from more than one device/location</td>
<td></td>
<td>Casey can utilize Adam's session after he has finished, because there is no log out function, or he cannot easily log out, or log out does not properly terminate the session</td>
</tr>
<tr class="even">
<td></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>59, 61</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>3.12</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>SE2</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>31, 61</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>28</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>60, 62, 66, 67, 71, 72</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>3.2, 3.7, 3.11</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>SE4-6</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>31</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>28</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>64, 65</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>3.3, 3.4, 3.16, 3.17, 3.18</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>SE5, SE6</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>21</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>28</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>62, 63</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>3.2, 3.5</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>-</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>21</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>28</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
</tr>
</tbody>
</table>

<table>
<tbody>
<tr class="odd">
<td></td>
<td><blockquote>
<p><strong><span class="smallcaps">Session Management</span></strong></p>
</blockquote></td>
<td><strong>8</strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Session Management</span></strong></p>
</blockquote></td>
<td><strong>9</strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Session Management</span></strong></p>
</blockquote></td>
<td><strong>10</strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Session Management</span></strong></p>
</blockquote></td>
<td><strong>J</strong></td>
</tr>
<tr class="even">
<td></td>
<td></td>
<td>Matt can abuse long sessions because the application does not require periodic re-authentication to check if privileges have changed</td>
<td></td>
<td>Ivan can steal session identifiers because they are sent over insecure channels, or are logged, or are revealed in error messages, or are included in URLs, or are accessible un-necessarily by code which the attacker can influence or alter</td>
<td></td>
<td>Marce can forge requests because per-session, or per-request for more critical actions, strong random tokens (i.e. anti-CSRF tokens) or similar are not being used for actions that change state</td>
<td></td>
<td>Jeff can resend an identical repeat interaction (e.g. HTTP request, signal, button press) and it is accepted, not rejected</td>
</tr>
<tr class="odd">
<td></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>96</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>-</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>-</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>21</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>28</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>69, 75, 76, 119, 138</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>3.6, 8.7, 10.3</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>SE4-6</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>31, 60</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>28</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>73, 74</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>4.13</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>IE4</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>62, 111</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>18</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p><span class="smallcaps">-</span></p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>15.1, 15.2</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>IE5</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>60</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>12, 14</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
</tr>
<tr class="even">
<td></td>
<td><blockquote>
<p><strong><span class="smallcaps">Session Management</span></strong></p>
</blockquote></td>
<td><strong>Q</strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Session Management</span></strong></p>
</blockquote></td>
<td><strong>K</strong></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr class="odd">
<td></td>
<td></td>
<td>Salim can bypass session management because it is not applied comprehensively and consistently across the application</td>
<td></td>
<td>Peter can bypass the session management controls because they have been self-built and/or are weak, instead of using a standard framework or approved tested module</td>
<td></td>
<td>(no card)</td>
<td></td>
<td>(no card)</td>
</tr>
<tr class="even">
<td></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>58</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>3.1</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>-</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>21</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>14, 28</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>58, 60</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>1.7</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>-</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>21</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>14, 28</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
</tbody>
</table>

<table>
<tbody>
<tr class="odd">
<td></td>
<td><blockquote>
<p><strong><span class="smallcaps">Authorization</span></strong></p>
</blockquote></td>
<td><strong>A</strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Authorization</span></strong></p>
</blockquote></td>
<td></td>
<td><blockquote>
<p><strong><span class="smallcaps">Authorization</span></strong></p>
</blockquote></td>
<td><strong>2</strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Authorization</span></strong></p>
</blockquote></td>
<td><strong>3</strong></td>
</tr>
<tr class="even">
<td></td>
<td></td>
<td>You have invented a new attack against Authorization</td>
<td></td>
<td>(no card)</td>
<td></td>
<td>Tim can influence where data is sent or forwarded to</td>
<td></td>
<td>Christian can access information, which they should not have permission to, through another mechanism that does have permission (e.g. search indexer, logger, reporting), or because it is cached, or kept for longer than necessary, or other information leakage</td>
</tr>
<tr class="odd">
<td></td>
<td></td>
<td><em>Read more about this topic in OWASP’s Development and Testing Guides</em></td>
<td></td>
<td></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>44</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>4.1, 4.16, 16.1</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>-</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>153</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>8, 10, 11</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>51, 100, 135, 139, 140, 141, 150</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>4.1, 8.2, 9.1-9.6, 9.11, 16.6, 16.7</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>-</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>69, 213</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>8, 10, 11</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
</tr>
<tr class="even">
<td></td>
<td><blockquote>
<p><strong><span class="smallcaps">Authorization</span></strong></p>
</blockquote></td>
<td><strong>4</strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Authorization</span></strong></p>
</blockquote></td>
<td><strong>5</strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Authorization</span></strong></p>
</blockquote></td>
<td><strong>6</strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Authorization</span></strong></p>
</blockquote></td>
<td><strong>7</strong></td>
</tr>
<tr class="odd">
<td></td>
<td></td>
<td>Kelly can bypass authorization controls because they do not fail securely (i.e. they default to allowing access)</td>
<td></td>
<td>Chad can access resources (including services, processes, AJAX, Flash, video, images, documents, temporary files, session data, system properties, configuration data, registry settings, logs) he should not be able to due to missing authorization, or due to excessive privileges (e.g. not using the principle of least privilege)</td>
<td></td>
<td>Eduardo can access data he does not have permission to, even though he has permission to the form/page/URL/entry point</td>
<td></td>
<td>Yuanjing can access application functions, objects, or properties he is not authorized to access</td>
</tr>
<tr class="even">
<td></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>79, 80</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>4.8</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>-</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>122</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>8, 10, 11</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><span class="smallcaps">OWASP SCP</span> 70,81,83-4,87-9, 99,117,131-2,142,154,170,179</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>4.1, 4.4, 4.9,, 19.3</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>ACE1-4, HT2</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>75, 87, 95, 126, 149, 155, 203, 213, 264-5</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>8, 10, 11, 13</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>81, 88, 131</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>4.1, 4.4</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>ACE1-4</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>122</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>8, 10, 11</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>81, 85, 86, 131</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>4.1, 4.4</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>ACE1-4</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>122</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>8, 10, 11</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
</tr>
</tbody>
</table>

<table>
<tbody>
<tr class="odd">
<td></td>
<td><blockquote>
<p><strong><span class="smallcaps">Authorization</span></strong></p>
</blockquote></td>
<td><strong>8</strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Authorization</span></strong></p>
</blockquote></td>
<td><strong>9</strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Authorization</span></strong></p>
</blockquote></td>
<td><strong>10</strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Authorization</span></strong></p>
</blockquote></td>
<td><strong>J</strong></td>
</tr>
<tr class="even">
<td></td>
<td></td>
<td>Tom can bypass business rules by altering the usual process sequence or flow, or by undertaking the process in the incorrect order, or by manipulating date and time values used by the application, or by using valid features for unintended purposes, or by otherwise manipulating control data</td>
<td></td>
<td>Mike can misuse an application by using a valid feature too fast, or too frequently, or other way that is not intended, or consumes the application's resources, or causes race conditions, or over-utilizes a feature</td>
<td></td>
<td>Richard can bypass the centralized authorization controls since they are not being used comprehensively on all interactions</td>
<td></td>
<td>Dinis can access security configuration information, or access control lists</td>
</tr>
<tr class="odd">
<td></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>10, 32, 93, 94, 189</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>4.10, 4.15, 4.16, 8.13, 15.1</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>ACE3</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>25, 39, 74, 162, 166, 207</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>8, 10, 11, 12</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>94</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>4.14, 15.2</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>AE3, FIO1-2, UT2-4, STE1-3</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>26, 29, 119, 261</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>1, 35</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>78, 91</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>1.7, 4.11</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>ACE1-4</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>36, 95, 121, 179</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>8, 10, 11</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>89, 90</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>4.10, 13.2</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>-</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>75, 133, 203</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>8, 10, 11</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
</tr>
<tr class="even">
<td></td>
<td><blockquote>
<p><strong><span class="smallcaps">Authorization</span></strong></p>
</blockquote></td>
<td><strong>Q</strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Authorization</span></strong></p>
</blockquote></td>
<td><strong>K</strong></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr class="odd">
<td></td>
<td></td>
<td>Christopher can inject a command that the application will run at a higher privilege level</td>
<td></td>
<td>Ryan can influence or alter authorization controls and permissions, and can therefore bypass them</td>
<td></td>
<td>(no card)</td>
<td></td>
<td>(no card)</td>
</tr>
<tr class="even">
<td></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>209</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>5.12</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>-</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>17, 30, 69, 234</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>8, 10, 11</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>77, 89, 91</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>4.9, 4.10, 13.2</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>-</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>207, 554</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>8, 10, 11</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
</tbody>
</table>

<table>
<tbody>
<tr class="odd">
<td></td>
<td><blockquote>
<p><strong><span class="smallcaps">Cryptography</span></strong></p>
</blockquote></td>
<td><strong>A</strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Cryptography</span></strong></p>
</blockquote></td>
<td></td>
<td><blockquote>
<p><strong><span class="smallcaps">Cryptography</span></strong></p>
</blockquote></td>
<td><strong>2</strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Cryptography</span></strong></p>
</blockquote></td>
<td><strong>3</strong></td>
</tr>
<tr class="even">
<td></td>
<td></td>
<td>You have invented a new attack against Cryptography</td>
<td></td>
<td>(no card)</td>
<td></td>
<td>Kyun can access data because it has been obfuscated rather than using an approved cryptographic function</td>
<td></td>
<td>Axel can modify transient or permanent data (stored or in transit), or source code, or updates/patches, or configuration data, because it is not subject to integrity checking</td>
</tr>
<tr class="odd">
<td></td>
<td></td>
<td><em>Read more about this topic in OWASP’s free Cheat Sheets on Cryptographic Storage, and Transport Layer Protection</em></td>
<td></td>
<td></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>105, 133, 135</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>-</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>-</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>-</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>21, 29</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>92, 205, 212</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>8.11, 11.7, 13.2, 19.5, 19.6, 19.7, 19.8</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>SE1, IE4</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>31, 39, 68, 75, 133, 145, 162, 203,438-9,442</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>12, 14</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
</tr>
<tr class="even">
<td></td>
<td><blockquote>
<p><strong><span class="smallcaps">Cryptography</span></strong></p>
</blockquote></td>
<td><strong>4</strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Cryptography</span></strong></p>
</blockquote></td>
<td><strong>5</strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Cryptography</span></strong></p>
</blockquote></td>
<td><strong>6</strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Cryptography</span></strong></p>
</blockquote></td>
<td><strong>7</strong></td>
</tr>
<tr class="odd">
<td></td>
<td></td>
<td>Paulo can access data in transit that is not encrypted, even though the channel is encrypted</td>
<td></td>
<td>Kyle can bypass cryptographic controls because they do not fail securely (i.e. they default to unprotected)</td>
<td></td>
<td>Romain can read and modify unencrypted data in memory or in transit (e.g. cryptographic secrets, credentials, session identifiers, personal and commercially-sensitive data), in use or in communications within the application, or between the application and users, or between the application and external systems</td>
<td></td>
<td>Gunter can intercept or modify encrypted data in transit because the protocol is poorly deployed, or weakly configured, or certificates are invalid, or certificates are not trusted, or the connection can be degraded to a weaker or un-encrypted communication</td>
</tr>
<tr class="even">
<td></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p><span class="smallcaps">37, 88, 143, 214</span></p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>7.12, 9.2</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>-</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>185, 186, 187</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>14, 29, 30</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>103, 145</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>7.2, 10.3</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>-</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>-</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>21, 29</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>36, 37, 143, 146, 147</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>2.16, 9.2, 9.11, 10.3, 19.2</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>-</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>31, 57, 102, 157, 158, 384, 466, 546</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p><span class="smallcaps">29</span></p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>75, 144, 145, 148</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>10.1, 10.5, 10.10, 10.11, 10.12, 10.13, 10.14</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>IE4</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>31, 216</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>14, 29, 30</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
</tr>
</tbody>
</table>

<table>
<tbody>
<tr class="odd">
<td></td>
<td><blockquote>
<p><strong><span class="smallcaps">Cryptography</span></strong></p>
</blockquote></td>
<td><strong>8</strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Cryptography</span></strong></p>
</blockquote></td>
<td><strong>9</strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Cryptography</span></strong></p>
</blockquote></td>
<td><strong>10</strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Cryptography</span></strong></p>
</blockquote></td>
<td><strong>J</strong></td>
</tr>
<tr class="even">
<td></td>
<td></td>
<td>Eoin can access stored business data (e.g. passwords, session identifiers, PII, cardholder data) because it is not securely encrypted or securely hashed</td>
<td></td>
<td>Andy can bypass random number generation, random GUID generation, hashing and encryption functions because they have been self-built and/or are weak</td>
<td></td>
<td>Susanna can break the cryptography in use because it is not strong enough for the degree of protection required, or it is not strong enough for the amount of effort the attacker is willing to make</td>
<td></td>
<td>Justin can read credentials for accessing internal or external resources, services and others systems because they are stored in an unencrypted format, or saved in the source code</td>
</tr>
<tr class="odd">
<td></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>30, 31, 70, 133, 135</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>2.13, 7.7, 7.8, 9.2</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>-</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>31, 37, 55</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>21, 29, 31</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>60, 104, 105</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>7.6, 7.7, 7.8, 7.15</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>-</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>97</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>14, 21, 29, 32, 33</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>104, 105</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>-</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>-</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>97, 463</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>14, 21, 29, 31, 32, 33</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>35, 90, 171, 172</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>2.29</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>-</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>116</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>21, 29</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
</tr>
<tr class="even">
<td></td>
<td><blockquote>
<p><strong><span class="smallcaps">Cryptography</span></strong></p>
</blockquote></td>
<td><strong>Q</strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Cryptography</span></strong></p>
</blockquote></td>
<td><strong>K</strong></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr class="odd">
<td></td>
<td></td>
<td>Randolph can access or predict the master cryptographic secrets</td>
<td></td>
<td>Dan can influence or alter cryptography code/routines (encryption, hashing, digital signatures, random number and GUID generation) and can therefore bypass them</td>
<td></td>
<td>(no card)</td>
<td></td>
<td>(no card)</td>
</tr>
<tr class="even">
<td></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>35, 102</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>7.8, 7.9, 7.11, 7.13, 7.14</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>-</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>116, 117</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>21, 29</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>31, 101</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>7.11</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>-</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>207, 554</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>14, 21, 29</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
</tbody>
</table>

<table>
<tbody>
<tr class="odd">
<td></td>
<td><blockquote>
<p><strong><span class="smallcaps">Cornucopia</span></strong></p>
</blockquote></td>
<td><strong>A</strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Cornucopia</span></strong></p>
</blockquote></td>
<td></td>
<td><blockquote>
<p><strong><span class="smallcaps">Cornucopia</span></strong></p>
</blockquote></td>
<td><strong>2</strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Cornucopia</span></strong></p>
</blockquote></td>
<td><strong>3</strong></td>
</tr>
<tr class="even">
<td></td>
<td></td>
<td>You have invented a new attack of any type</td>
<td></td>
<td>(no card)</td>
<td></td>
<td>Lee can bypass application controls because dangerous/risky programming language functions have been used instead of safer alternatives, or there are type conversion errors, or because the application is unreliable when an external resource is unavailable, or there are race conditions, or there are resource initialization or allocation issues, or overflows can occur</td>
<td></td>
<td>Andrew can access source code, or decompile, or otherwise access business logic to understand how the application works and any secrets contained</td>
</tr>
<tr class="odd">
<td></td>
<td></td>
<td><em>Read more about application security in OWASP’s free Guides on Requirements, Development, Code Review and Testing, the Cheat Sheet series, and the Open Software Assurance Maturity Model</em></td>
<td></td>
<td></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>194-202, 205-209</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>5.1</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>-</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>25, 26, 29, 96, 123-4, 128-9, 264-5</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>3, 5-7, 9, 22, 25-26, 34</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p><span class="smallcaps">134</span></p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>19.5</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>-</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>189, 207</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p><span class="smallcaps">-</span></p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
</tr>
<tr class="even">
<td></td>
<td><blockquote>
<p><strong><span class="smallcaps">Cornucopia</span></strong></p>
</blockquote></td>
<td><strong>4</strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Cornucopia</span></strong></p>
</blockquote></td>
<td><strong>5</strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Cornucopia</span></strong></p>
</blockquote></td>
<td><strong>6</strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Cornucopia</span></strong></p>
</blockquote></td>
<td><strong>7</strong></td>
</tr>
<tr class="odd">
<td></td>
<td></td>
<td>Keith can perform an action and it is not possible to attribute it to him</td>
<td></td>
<td>Larry can influence the trust other parties including users have in the application, or abuse that trust elsewhere (e.g. in another application)</td>
<td></td>
<td>Aaron can bypass controls because error/exception handling is missing, or is implemented inconsistently or partially, or does not deny access by default (i.e. errors should terminate access/execution), or relies on handling by some other service or system</td>
<td></td>
<td>Mwengu's actions cannot be investigated because there is not an adequate accurately time-stamped record of security events, or there is not a full audit trail, or these can be altered or deleted by Mwengu, or there is no centralized logging service</td>
</tr>
<tr class="even">
<td></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p><span class="smallcaps">23, 32, 34, 42, 51, 181</span></p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>8.10</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>-</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>-</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p><span class="smallcaps">-</span></p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p><span class="smallcaps">-</span></p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>-</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>-</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>89, 103, 181, 459</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p><span class="smallcaps">-</span></p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>109, 110, 111, 112, 155</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>8.2, 8.4</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>-</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>54, 98, 164</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>4, 11, 23</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>113-115, 117, 118, 121-130</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>2.12, 8.3-8.12, 9.10, 10.4</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>-</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>93</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p><span class="smallcaps">4</span></p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
</tr>
</tbody>
</table>

<table>
<tbody>
<tr class="odd">
<td></td>
<td><blockquote>
<p><strong><span class="smallcaps">Cornucopia</span></strong></p>
</blockquote></td>
<td><strong>8</strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Cornucopia</span></strong></p>
</blockquote></td>
<td><strong>9</strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Cornucopia</span></strong></p>
</blockquote></td>
<td><strong>10</strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Cornucopia</span></strong></p>
</blockquote></td>
<td><strong>J</strong></td>
</tr>
<tr class="even">
<td></td>
<td></td>
<td>David can bypass the application to gain access to data because the network and host infrastructure, and supporting services/applications, have not been securely configured, the configuration rechecked periodically and security patches applied, or the data is stored locally, or the data is not physically protected</td>
<td></td>
<td>Michael can bypass the application to gain access to data because administrative tools or administrative interfaces are not secured adequately</td>
<td></td>
<td>Xavier can circumvent the application's controls because code frameworks, libraries and components contain malicious code or vulnerabilities (e.g. in-house, commercial off the shelf, outsourced, open source, externally-located)</td>
<td></td>
<td>Roman can exploit the application because it was compiled using out-of-date tools, or its configuration is not secure by default, or security information was not documented and passed on to operational teams</td>
</tr>
<tr class="odd">
<td></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>151, 152, 156, 160, 161, 173-177</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>19.1, 19.4, 19.6, 19.7, 19.8</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>RE1, RE2</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>37, 220, 310, 436, 536</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p><span class="smallcaps">-</span></p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p><span class="smallcaps">23, 29, 56, 81, 82, 84-90</span></p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>2.1, 2.32</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>-</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>122, 233</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p><span class="smallcaps">-</span></p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p>57, 151, 152, 204, 205, 213, 214</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>1.11-</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>-</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>68, 438, 439, 442, 524, 538</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p><span class="smallcaps">15</span></p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p><span class="smallcaps">90, 137, 148, 151-154, 175-179, 186, 192</span></p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>19.5, 19.9</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>-</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>-</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p><span class="smallcaps">4</span></p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
</tr>
<tr class="even">
<td></td>
<td><blockquote>
<p><strong><span class="smallcaps">Cornucopia</span></strong></p>
</blockquote></td>
<td><strong>Q</strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Cornucopia</span></strong></p>
</blockquote></td>
<td><strong>K</strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Wild Card</span></strong></p>
</blockquote></td>
<td><strong>Joker</strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Wild Card</span></strong></p>
</blockquote></td>
<td><strong>Joker</strong></td>
</tr>
<tr class="odd">
<td></td>
<td></td>
<td>Jim can undertake malicious, non-normal, actions without real-time detection and response by the application</td>
<td></td>
<td>Gareth can utilize the application to deny service to some or all of its users</td>
<td></td>
<td>Alice can utilize the application to attack users' systems and data</td>
<td></td>
<td>Bob can influence, alter or affect the application so that it no longer complies with legal, regulatory, contractual or other organizational mandates</td>
</tr>
<tr class="even">
<td></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p><span class="smallcaps">-</span></p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>4.14, 9.8, 15.1, 15.2</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>(All)</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>-</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p>1, 27</p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
<td></td>
<td><table>
<thead>
<tr class="header">
<th><p><span class="smallcaps">OWASP SCP</span></p>
<p><span class="smallcaps">41, 55</span></p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OWASP ASVS</p>
<p>-</p></td>
</tr>
<tr class="even">
<td><p>OWASP AppSensor</p>
<p>UT1-4, STE3</p></td>
</tr>
<tr class="odd">
<td><p>CAPEC</p>
<p>2, 25, 119, 125</p></td>
</tr>
<tr class="even">
<td><p><span class="smallcaps">SAFECode</span></p>
<p><span class="smallcaps">1</span></p></td>
</tr>
<tr class="odd">
<td>OWASP Cornucopia Ecommerce Website Edition v1.20-EN</td>
</tr>
</tbody>
</table></td>
<td></td>
<td><em>Have you thought about becoming an individual OWASP member? All tools, guidance and local meetings are free for everyone, but individual membership helps support OWASP’s work</em></td>
<td></td>
<td><em>Examine vulnerabilities and discover how they can be fixed using training applications in the free OWASP Broken Web Applications VM, or using the online challenges in the free Hacking Lab</em></td>
</tr>
</tbody>
</table>

<table>
<thead>
<tr class="header">
<th>Cut here</th>
<th></th>
<th></th>
<th></th>
<th></th>
<th></th>
<th></th>
<th></th>
<th></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td></td>
<td><strong><span class="smallcaps">Cornucopia</span></strong></td>
<td><blockquote>
<p><strong><span class="smallcaps">Cornucopia</span></strong></p>
</blockquote></td>
<td></td>
<td><blockquote>
<p><strong><span class="smallcaps">Cornucopia</span></strong></p>
</blockquote></td>
<td></td>
<td><blockquote>
<p><strong><span class="smallcaps">Cornucopia</span></strong></p>
</blockquote></td>
<td><strong>J</strong></td>
<td></td>
</tr>
<tr class="even">
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr class="odd">
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr class="even">
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
</tbody>
</table>

![](media/image3.png)

Change Log

| Version / Date | Comments    |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| -------------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 0.10           | 30 Jul 2012 | Original draft.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| 0.20           | 10 Aug 2012 | Draft reviewed and updated.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| 0.30           | 15 Aug 2012 | Draft announced OWASP SCP mailing list for comment.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| 0.40           | 25 Feb 2013 | Play rules updated based on feedback during workshops. Added reference to PCI SSC Information Supplement: PCI DSS E-commerce Guidelines. Descriptive text extended and updated. Added contributors section, page numbering, FAQs and change log.                                                                                                                                                                                                                                                                                                                                                                                                                    |
| 1.00           | 25 Feb 2013 | Release.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| 1.01           | 03 Jun 2013 | Framework-specific card deck discussion added. Additional FAQs created. Descriptive text updated. New cover image, and previous cover image moved to back. Cut lines added. Alternative rules and deck subset descriptions added. Project website and mailing list added. Cornucopia King cross-reference to AppSensor updated.                                                                                                                                                                                                                                                                                                                                     |
| 1.02           | 14 Aug 2013 | Warning about time to print added. Additional alternative game rules added (twenty-one, play a deck over a week, play full hand and then discuss). Compliance deck concept added. FAQs 5 and 6 added. Attack descriptions on cards with tinted backgrounds changed to black (from dark grey). Project contributors added.                                                                                                                                                                                                                                                                                                                                           |
| 1.03           | 18 Sep 2013 | Minor attack wording changes on two cards. OWASP SCP and ASVS cross-references checked and updated. Code letters added for suits. All remaining attack descriptions on cards changed to black (from dark grey) and background colours amended to provide more contrast and increase readability.                                                                                                                                                                                                                                                                                                                                                                    |
| 1.04           | 01 Feb 2014 | Text “password change, password change,” corrected to “password change, password recovery,” on Queen of Authentication card.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| 1.05           | 21 Mar 2014 | Updates to alternative game rules. Additional FAQs created. Contributors updated. Podcast and video links added.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| 1.10           | 04 Mar 2015 | Change log date corrected for v1.05. Cross-references updated for 2014 version of ASVS. Contributors updated. Minor text changes to cards to improve readability.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| 1.20           | 29 Jun 2016 | Video mentioned/linked. Separate score sheet mentioned/linked. Previous embedded score sheet pages deleted. Correction (identified by Tom Brennan) and addition to text on card 8 Authentication. Oana Cornea and other participants at the AppSec EU 2015 project summit added to list of contributors. Darío De Filippis added as project co-leader. Wiki Deck link added. Cross-references updated for ASVS v3.0.1 and CAPEC v2.8. Minor text changes to a small number of cards. Added “-EN” to version number in preparation for “-ES” version. Susana Romaniz added as a contributor to the Spanish translation. Minor text changes to instructions and FAQs. |
| 1.21           | 13 Jul 2018 | References to new FR and PT-BR translations, and new contributors’ names. Corrections to hyperlinks.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
|                |             |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
|                |             |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
|                |             |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
|                |             |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
|                |             |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
|                |             |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
|                |             |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
|                |             |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
|                |             |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
|                |             |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |

<table>
<tbody>
<tr class="odd">
<td><p>Project contributors</p>
<p>All OWASP projects rely on the voluntary efforts of people in the software development and information security sectors. They have contributed their time and energy to make suggestions, provide feedback, write, review and edit documentation, give encouragement, trial the game, and promote the concept. Without all their efforts, the project would not have progressed to this point. Please contact the mailing list or project leaders directly, if anyone is missing from the below lists.</p>
<table>
<tbody>
<tr class="odd">
<td><ul>
<li><blockquote>
<p>Simon Bennetts</p>
</blockquote></li>
<li><blockquote>
<p>Thomas Berson</p>
</blockquote></li>
<li><blockquote>
<p>Tom Brennan</p>
</blockquote></li>
<li><blockquote>
<p>Fabio Cerullo</p>
</blockquote></li>
<li><blockquote>
<p>Oana Cornea</p>
</blockquote></li>
<li><blockquote>
<p>Johanna Curiel</p>
</blockquote></li>
<li><blockquote>
<p>Todd Dahl</p>
</blockquote></li>
<li><blockquote>
<p>Luis Enriquez</p>
</blockquote></li>
<li><blockquote>
<p>Ken Ferris</p>
</blockquote></li>
<li><blockquote>
<p>Darío De Filippis</p>
</blockquote></li>
</ul></td>
<td><ul>
<li><blockquote>
<p>Sebastien Gioria</p>
</blockquote></li>
<li><blockquote>
<p>Tobias Gondrom</p>
</blockquote></li>
<li><blockquote>
<p>Timo Goosen</p>
</blockquote></li>
<li><blockquote>
<p>Anthony Harrison</p>
</blockquote></li>
<li><blockquote>
<p>Martin Haslinger</p>
</blockquote></li>
<li><blockquote>
<p>John Herrlin</p>
</blockquote></li>
<li><blockquote>
<p>Jerry Hoff</p>
</blockquote></li>
<li><blockquote>
<p>Marios Kourtesis</p>
</blockquote></li>
<li><blockquote>
<p>Franck Lacosta</p>
</blockquote></li>
<li><blockquote>
<p>Mathias Lemaire</p>
</blockquote></li>
</ul></td>
<td><ul>
<li><blockquote>
<p>Antonis Manaras</p>
</blockquote></li>
<li><blockquote>
<p>Jim Manico</p>
</blockquote></li>
<li><blockquote>
<p>Mark Miller</p>
</blockquote></li>
<li><blockquote>
<p>Cam Morris</p>
</blockquote></li>
<li><blockquote>
<p>Susana Romaniz</p>
</blockquote></li>
<li><blockquote>
<p>Ravishankar Sahadevan</p>
</blockquote></li>
<li><blockquote>
<p>Tao Sauvage</p>
</blockquote></li>
<li><blockquote>
<p>Wagner Voltz</p>
</blockquote></li>
<li><blockquote>
<p>Stephen de Vries</p>
</blockquote></li>
<li><blockquote>
<p>Colin Watson</p>
</blockquote></li>
</ul></td>
</tr>
</tbody>
</table>
<ul>
<li><p>OWASP’s hard-working employees, especially Kate Hartmann</p></li>
<li><p>Attendees at OWASP London, OWASP Manchester, OWASP Netherlands and OWASP Scotland chapter meetings, and the London Gamification meetup, who made helpful suggestions and asked challenging questions</p></li>
<li><p>Blackfoot UK Limited for gifting print-ready design files and hundreds of professionally printed card decks for distribution by post and at OWASP chapter meetings</p></li>
<li><p>OWASP NYC for creating an OWASP box design and distributing packs at AppSec USA 2014.</p></li>
</ul>
<p>Podcasts and videos</p>
<p>The following supporting OWASP Cornucopia resources are available online:</p>
<ul>
<li><blockquote>
<p>Video - Using the cards, created during AppSec EU 2015 project summit, 20<sup>th</sup> May 2015<br />
<a href="https://www.youtube.com/watch?v=i5Y0akWj31k">https://www.youtube.com/watch?v=i5Y0akWj31k</a></p>
</blockquote></li>
<li><blockquote>
<p>Podcast interview, OWASP 24/7 Podcast channel, 21<sup>st</sup> March 2014<br />
https://soundcloud.com/owasp-podcast/the-owasp-cornucopia-project</p>
</blockquote></li>
<li><blockquote>
<p>Video of presentation, OWASP EU Tour 2013 London, 3<sup>rd</sup> June 2013<br />
<a href="https://www.youtube.com/watch?v=Q_LE-8xNXVk">https://www.youtube.com/watch?v=Q_LE-8xNXVk</a></p>
</blockquote></li>
</ul>
<p>See the project website for further information and presentation materials.</p></td>
<td><img src="media/image4.png" style="width:4.93026in;height:7.2397in" /></td>
</tr>
</tbody>
</table>
