---
date: 20240201
author: ive-verstappen
tags: scrum,agile
hidden: false
description: How to start with Cornucopia in a Scrum team Individually or as a team, you have decided that you want to improve the level of cybersecurity of your applications by integrating an Appsec process in your development workflow.
---

# How to start with Cornucopia in a Scrum team
Individually or as a team, you have decided that you want to improve the level of cybersecurity of your applications by integrating an Appsec process in your development workflow.

Our Owasp Cornucopia cards are a great way of starting your Appsec process!  But how do you start?

Here are some practical tips of how to integrate playing the Cornucopia cardgame in your Scrum process and start implementing dedicated Appsec:

## Start small - use only 2 or 3 Cornucopia suits

Cornucopia consists of 6 suits:
- Data Validation & Encoding
- Authentication
- Session Management
- Authorization
- Cryptography
- Cornucopia

Cornucopia was created by security professionals but often used by software development teams.  We noticed that most development teams tend to understand these suits the best:
- Authentication
- Authorization

**Data Validation & Encoding** is a third suit you could consider to include.

Why these suits?  We looked at the [Owasp top 10](https://cornucopia.dotnetlab.eu/taxonomy/OWASP-top-10).  The first one; [#1: Broken access controls](https://cornucopia.dotnetlab.eu/taxonomy/OWASP-top-10/01-broken-access-controls) corresponds with the suits Data Validation & Encoding and Authorization.  We feel like Authentication should always be part of a Cornucopia game.  If you look at the Owasp Top  10, [#2 Cryptographic failures](https://cornucopia.dotnetlab.eu/taxonomy/OWASP-top-10/02-cryptographic-failures) corresponds best with the suit cryptography.  So you're not only limiting the complexity of playing the game, but you're also focusing on the most important threats according to Owasp Top 10.

## How to integrate playing the cornucopia game in your Scrum planning process

Here it gets a little bit tricky.  There are a few routes you could take about how to introduce Cornucopia in your planning process:

1. You integrate playing Cornucopia into your Product Planning Meeting.
2. You integrate playing Cornucopia into your Sprint Planning Meeting.
3. You create a new planning meeting focused on Appsec by playing Cornucopia.

### Option 1: Integrate playing Cornucopia into the Product Planning Meeting
At first glance, integrating Cornucopia into the Product Planning Meeting seems like a logical option.  

Generally, the team will decide on the functional requirements during the Product Planning Meeting.  A lot of teams limit the attendees and focus of the product planning meeting to something around these lines:

- Attendees = Product Owner, (a representative of) the customer, Scrum Master
- Focus = Functional Requirements

When you recognize that your Product Planning meeting has the above characteristics, then I would be reluctant to integrate the Cornucopia game into this meeting.  When you play the game, you will quickly have some deep-dives into the technical discussions about how the software is built.  People playing Cornucopia need to have a detailed understanding of the technical ins and outs of how the software has been written.

IF - and this is a big IF - your team is used to discussing Nonfunctional requirements during the Product Planning meeting and the people attending this meeting are really technically sophisticated, then integrating playing Cornucopia during the Product Planning meeting could be a good idea.  However, be mindful not to overload your Product Planning meeting.  If you notice the attendees of the Product Planning meeting become overwhelmed by playing Cornucopia it is probably wise to choose another way to improve your Appsec processes.

To conclude, for most teams playing Cornucopia during the Product Planning meeting is probably not a great idea.  That is because most teams are focused on functional requirements during the Product Planning Meeting.  However, if the participants are used to take decisions about non-functional requirements during the Product Planning Meeting, then it could be considered to introduce Cornucopia in this meeting to discover Cybersecurity related Non-functional requirements together.  

### Option 2: Integrate playing cornucopia into the Sprint Planning Meeting
So then, why don't we integrate playing Cornucopia in the Sprint Planning meeting?

During the Sprint Planning meeting, the developers are present.  They can play Cornucopia, identify threats and directly plan them in the Sprint Backlog!  So, this seems like a logical choice, doesn't it?

**Wrong!  We strongly discourage teams to take the Sprint Planning route.**
While integrating Cornucopia inside the Sprint Planning Meeting seems like a logical choice, it immediately presents all involved parties (Customer, Product Owner, Scrum Master, Team) with issues, such as:
1. Can you fit playing Cornucopia within the Sprint Planning meeting timebox?
2. Can the team really focus on Appsec during the Sprint Planning meeting?

**Can you fit playing Cornucopia within the Sprint Planning meeting timebox?**
The answer to this question is probably "NO".  We don't want to complicate the implementation of a correct Scrum-process by overloading your Sprint Planning meeting.  Quite the contrary, our aim is to improve the quality of your Scrum Process and the quality of the software your team produces.

playing Cornucopia will overcomplicate your Sprint Planning Meeting.  This is not productive and will discourage your team from playing Cornucopia and improving the Security for your application.

**Can the team really focus on Appsec while it is planning its new sprint?**
Doing a good Sprint Planning meeting is already very complicated.  Maybe you already do "sprint planning poker" with planning poker cards, which is a good practice.   

The purpose of playing cornucopia really does not fit into a Sprint Planning Process.  This is because all the energy of the team should go to do a proper and well executed Sprint Planning meeting.  The Sprint Planning is probably the most complicated and tricky step in the Scrum Process and you should avoid taking any step that compromises this important process.

As a conclusion, we strongly advise against integrating Cornucopia into the Sprint Planning meeting.

### Option 3: create a new planning meeting focused on Appsec by playing Cornucopia
There are a few things to consider when you want to succesfully start your Appsec program by playing Cornucopia.  First of all, your team should be able to put all its energy into playing Cornucopia correctly.

Make sure all of your team-members have the Cornucopia cards and they have viewed the "how to play" video on our website.  This video explains how to play one round of Cornucopia.

**Properties of the Cornucopia meeting**
Who should attend?
Make sure you include the developers, architect and the Product Owner into the meeting.  If you have a dedicated Functional Analyst, then you could include him as well.

What is the agenda of the first Cornucopia-meeting?
- The purpose of Appsec and why Cornucopia is a good way to start
- Choosing the suits with which you will play
- Playing a hand of Cornucopia
- Writing down the threats
	
In future blogposts, I will elaborate further on how to best conduct a Cornucopia meeting.  For now, I want to stress one important point:

Limit yourself to writing down the possible threats by simply writing down the cards which are relevant to your project.

eg: 
- Authentication -5
- Authorization -9
- Authorization -5

**The result of the meeting should be a list of relevant cards.  These cards = threats.**  

More information about how to go from cards to Product Backlog Items will become available on this website in the course of 2024.

## Conclusion
Playing the Cornucopia cardgame is a great way to start your Appsec program.  You can integrate playing Cornucopia in your Scrum Process and we advise to do that by creating a dedicated meeting.  

The outcome of that meeting should be a list of relevant cards for your development project.  That means you identified threats and you can start the process of writing a threatmodel for those threats.

Good luck!

Ive

Please use the comment section below to give feedback or ask questions.