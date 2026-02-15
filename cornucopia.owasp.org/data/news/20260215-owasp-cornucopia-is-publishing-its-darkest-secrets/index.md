__Why do we keep our darkest fears secret? Publish them, and bring light to the darkest corners of your web application.__

When Adam Schostack + associates last year urged everyone to [publish their threat model](https://shostack.org/blog/publish-your-threat-model/), we thought, «What a wonderful idea!»

![Publish your threat model, at https://shostack.org/blog/publish-your-threat-model/](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ivcsnbnbtq4qs0t4xzc6.webp)

So we went ahead and did just that. At cornucopia.owasp.org, you can now [find the threat model](https://cornucopia.owasp.org/copi#Our-Threat-Model) for the O[WASP Cornucopia Game Engine, Copi](https://copi.owasp.org/).
There we have listed all our darkest fears and secrets. Darkness is not a force of its own; it is simply the absence of light. When light is shed on our doubts and fears, making them visible, we find solutions and become stronger. This is why publishing your threat model is essential. If you refuse to disclose your vulnerabilities to anyone, they become liabilities that may one day lead to doubts, lies, and perhaps even conspiracies and litigation. Therefore, before building software, build trust and make it clear what others need to be aware of.

## Threat Dragon and EoP Games

![Threat Dragon and EoP Games](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/1ry2rze9wnftocimdkyo.png)

When choosing a tool for publishing our threat model, we chose [OWASP Threat Dragon](https://www.threatdragon.com/#/). OWASP Threat Dragon is a free, open-source, cross-platform threat modeling application. It is used to create threat modeling diagrams and list threats for elements within the diagrams. Mike Goodwin created Threat Dragon as an open-source community project that provides an intuitive, accessible way to model threats.

![How to choose to create a OWASP Cornucopia threat model](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/l25mz5xxzbt0a8t5627g.png)

Thanks to Gerardo Canedo and his students at Universidad Católica del Uruguay, it's now possible to create your OWASP Cornucopia Threat Model directly in OWASP Threat Dragon. When creating a new diagram for your threat model, simply choose to create an EoP Games diagram. We chose to call the diagram EoP Games for two reasons. One, OWASP Cornucopia is derived from the [Elevation of Privilege game](https://shostack.org/games/elevation-of-privilege) created by Adam Shostack. Two, we don't want to stop with OWASP Cornucopia. We also want to add other EoP games, such as the original EoP Game.

![Create a OWASP Cornucopia threat](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/1zl30hc63fie1wg6y7e3.png)

Once you have created an EoP Games diagram, you can add OWASP Cornucopia threats to your threat model. The specific threat you add will get a link reference to the [OWASP Cornucopia website](https://cornucopia.owasp.org/edition/webapp/AT3/2.2/en#Threat-Modeling), where you will find guidance on threat modeling and STRIDE, which will help you in identifying what can go wrong and what to do about it. You can also find a [complete mapping](https://cornucopia.owasp.org/edition/webapp/AT3/2.2/en#What-are-we-going-to-do-about-it?) to [OWASP ASVS](https://cornucopia.owasp.org/taxonomy/asvs-4.0.3/02-authentication/05-credential-recovery#V2.5.2), [OWASP Developer Guide](https://devguide.owasp.org/en/04-design/02-web-app-checklist/06-digital-identity/#1-authentication-a), and all [relevant CAPECs](https://cornucopia.owasp.org/taxonomy/capec-3.9).

![OWASP Corncupia Website](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/9mvjvggcpwkh58fix1bc.png)

I want to express my sincere appreciation to Gerardo Canedo, Sebastian Feirre, and their students at Universidad Católica del Uruguay for making this possible. With their dedication and effort, OWASP Cornucopia wouldn’t have had this possibility.

![Gerardo Canedo and his students at Universidad Católica del Uruguay](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/aabcyoarlrl9ogkvw601.JPG)

## Shostack's 4 Question Frame for Threat Modeling

OWASP Cornucopia, together with OWASP Threat Dragon, is helping us in answering:

- What we are working on
- What can go wrong?
- What are we going to do about it?

...but "Did we do a good enough job?"

At Admincontrol, where I work, we have always sent an anonymous survey after every OWASP Cornucopia threat modeling session. The aggregate score for how satisfied respondents have been with all sessions we've held since we started OWASP Cornucopia in 2023 is 4.5 out of 5. When asked how relevant the session was to the participant's job, the average score was 4.7 out of 5. When asked whether the OWASP Cornucopia session helped the participants understand which security controls (mitigations) they need to implement/test, the score was 4.5. When asked whether the session improved the overall awareness of application security requirements, the score was 4.0. When asked, "Did we do a good job?", the score was 4.3. So for sure, we can do better!

![Relevant for your job](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/n0iihqk4knhglpi3qo2l.png)

When asking the question, "Did we do a good enough job?", don’t just blurt it out during a session. Do you honestly think people will give you their honest criticism to your face directly? Send out an anonymous survey and ask for feedback!

OWASP Cornucopia welcomes any input or improvements you might be willing to share with us regarding our current threat model. Arguably, we created the system before we were able to identify all our threats, and several improvements need to be made to properly balance the inherent risks of compromise against the current security controls. For anyone hosting the game engine, please take this into account. For anyone wanting to share their opinion, please don't hesitate to [visit our repository](https://github.com/OWASP/cornucopia/issues), share your feedback, and, if appropriate, give us a star⭐️.

<noscript>
    <p>You cannot view this video directly because JavaScript is disabled. Click <a href="https://www.youtube.com/watch?v=XXTPXozIHow" title="How to play OWASP Cornucopia" target="_blank" rel="noopener">here</a> to watch the video on YouTube.</p>
</noscript>
<iframe credentialless anonymous class="how-to-play" frameborder="0" title="Youtube: How to play OWASP Cornucopia"
src="https://www.youtube.com/embed/XXTPXozIHow?si=uIi_VXDtSBkS027S" referrerpolicy="no-referrer" allowfullscreen >
<p>You cannot view this video directly because iframes are disabled. Click <a href="https://www.youtube.com/watch?v=XXTPXozIHow" title="How to play OWASP Cornucopia" target="_blank" rel="noopener">here</a> to watch the video on YouTube.</p></iframe>

---

[OWASP Foundation](https://owasp.org "[external]") is a non-profit foundation that envisions a world with no more insecure software. Our mission is to be the global open community that powers secure software through education, tools, and collaboration. We maintain hundreds of open source projects, run industry-leading educational and training conferences, and meet through over 250 chapters worldwide.
