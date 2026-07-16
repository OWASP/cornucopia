## Scenario: Garth can reduce app users' privacy because the app is not transparent about its data collection and usage in a concise, easily accessible, and understandable way

Consider a scenario where Garth downloads a popular recipe app. The app collects his precise location, device identifiers, dietary preferences, and behavioural patterns. All of this is disclosed — somewhere — in a 47-page privacy policy that requires a law degree to interpret. The app presents no concise, in-context explanation of what data is collected or why. Garth clicks "Accept" because everyone clicks "Accept." He has no meaningful understanding of what he agreed to.

1. A privacy policy buried in settings and written in legal language does not constitute meaningful transparency.
2. In-context data collection without a timely explanation violates the transparency principle of most privacy regulations.
3. Users cannot exercise their data rights if they do not know what data is being collected.

### Example

Garth uses the recipe app for three months. He later reads a news article explaining that the app sells precise location data to advertisers. He had no idea — the in-app privacy notice was a single sentence: "We may collect data to improve your experience." No details of what data, with whom it is shared, or for how long it is retained were provided in the app itself. Garth's right to be informed was nominally satisfied by a dense document nobody read. His meaningful privacy was not.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure**.

Users are effectively uninformed of data collection practices. Decisions made without meaningful information are not informed decisions. The harm is reputational, regulatory, and to user autonomy.

### What can go wrong?

- Users are unaware of data collection practices and cannot make informed consent decisions.
- Regulatory bodies (GDPR, CCPA, PIPEDA) require clear, accessible privacy notices; failure is a compliance risk.
- Users who discover undisclosed data practices lose trust and may file complaints or leave negative reviews.

### What are we going to do about it?

- Provide concise, context-sensitive privacy notices at or before the point of data collection.
- Summarise the key points of data practices in plain language in the app itself; link to the full policy for detail.
- Disclose: what is collected, why it is needed, who it is shared with, and how long it is retained.
- Ensure the privacy notice is accessible from within the app in no more than two taps.
