## Scenario: Ferranti Mercury's flash-mob scenario

### Example

Ferranti Mercury likes to disrupt certain online retailers for political reasons. Ferranti Mercury's favourite tactic is to target app queuing systems (which limit access to the ordering/payment process for sought-after items) by taking up all the available places - like a flash-mob suddenly appearing somewhere. This disrupts the targetted company's sales, upsets its customers by making the shopping experience worse and, thus negatively affects its reputation. This is "win win win" in Ferranti Mercury's opinion! The disruption is undertaken by using scripted processes to automatically join the purchase queue (line) multiple times, preventing potential real humans from doing so because all the slots are filled. When one of Ferranti Mercury's places gets to the front of the queue, it just leaves, without making a purchase, and joins the queue again to repeat the manoeuvre.

## Threat Modeling

### STRIDE

This scenario falls into the **Tampering** category of STRIDE. Ferranti Mercury fills the purchase queue with fake 'shoppers' preventing real customers from doing so.

### What can go wrong?

Functionality, like queues, shopping baskets, reservations and the like, which remove options, places, slots, stock or other limited availability items can be abused to prevent others from performing valid transactions. These exhaustion of inventory attacks affect business processes and can reduce conversion rates, can lead to poorer customer experiences and can increase complaints. Many apps use the same queuing services, making it simpler to undertake the attack against many retailers. 

For further explanation, examples, possible symptoms,  and other closely-related automation threats which target inherent intended functionality and related design flaws, rather than implementation bugs, see the OWASP Automated Threat (OAT) identifiers in the mapping section, and the reference [OWASP Automated Threat Handbook](https://owasp.org/www-project-automated-threats-to-web-applications/).

### What are we going to do about it?

- Monitor held inventory, queue/basket/order/payment abandonment rates, and sales conversion ratios.
- Limit time-period for holding items and number of items that can be held.
- Identify and block bots being used to access relevant functionality.
- Detect anomalous automated behaviour and respond to detected attacks in real-time.

For detailed advice on relevant countermeasures, see further documentation in the [OWASP Automated Threat Handbook](https://owasp.org/www-project-automated-threats-to-web-applications/).
