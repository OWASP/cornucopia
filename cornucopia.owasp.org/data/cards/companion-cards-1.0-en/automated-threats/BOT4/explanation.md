## Scenario: IBM 701's last-minute killer-shots scenario

### Example

IBM 701 undertakes last-minute bids for items in auctions, without participating earlier, to hide their interest. IBM 701 targets online property auctions to buy up selected homes, targetted using its proprietary market data, which can be resold later at a higher price. Timing is absolutely vital, and IBM 701 attunes itself to each application's patterns of use, latency and configurations. Just at the right moment IBM 701 pounces very quickly to make the winning bid for a home at the lowest margin above any current highest offer, or at the minimum price if there have been no other bids.

## Threat Modeling

### STRIDE

This scenario falls into the **Tampering** category of STRIDE. IBM 701 does not participate until a fraction before the end of the auction, preventing others from making any higher bids.

### What can go wrong?

The process is not operating in the competitive way intended, because there is insufficient time for another user to bid/offer. This may also be considered a type of user denial of service.

For further explanation, examples, possible symptoms,  and other closely-related automation threats which target inherent intended functionality and related design flaws, rather than implementation bugs, see the OWASP Automated Threat (OAT) identifiers in the mapping section and the reference [OWASP Automated Threat Handbook](https://owasp.org/www-project-automated-threats-to-web-applications/).

### What are we going to do about it?

- Monitor successful/unsuccessful bids, timing of bids/offers and success rates.
- Limit rapid/repeated purchases by users.
- Consider penalising later bids/offers/purchases and/or encouraging earlier ones.
- Consider requiring identification, re-authentication or some other increased authentication assurance for relevant functionality.
- Identify and block bots being used to access relevant functionality.
- Detect anomalous automated behaviour and respond to detected attacks in real-time.

For detailed advice on relevant countermeasures, see further documentation in the [OWASP Automated Threat Handbook](https://owasp.org/www-project-automated-threats-to-web-applications/).
