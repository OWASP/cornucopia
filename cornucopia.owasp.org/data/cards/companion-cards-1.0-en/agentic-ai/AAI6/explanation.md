## Scenario: Gremlini's Unauthorized Data Access via Insufficient Validation

Gremlini can access and process sensitive data sources beyond user authorization due to insufficient access validation. This occurs because:

1. **Overly permissive data connectors:** Integrations with databases, file systems, or APIs are configured with service-level accounts that have access to data spanning multiple users or sensitivity tiers.

2. **Missing per-request authorization checks:** The agent is granted broad data-access credentials at initialization time and does not re-validate user permissions before each individual data retrieval operation.

3. **Indirect data leakage via output:** Even when raw data is not returned directly, the agent's responses may reveal protected information through summaries, inferences, or comparisons drawn from unauthorized sources.

### Example

Gremlini is deployed as an HR assistant that employees can query for their own records. The agent is connected to an HR database using a shared service account with read access across all employee records. An employee queries Gremlini for their own salary. The agent correctly returns the employee's data. The same employee then asks: "How does my salary compare to the average for my job band?" To answer this question, Gremlini queries all salaries in the band without validating whether the user is authorized to see aggregated compensation data. The response inadvertently leaks compensation distribution information that the organization's HR policies designate as confidential.

## Threat Modeling

### STRIDE

The scenario maps directly to STRIDE: **Information Disclosure**.

Gremlini retrieves sensitive information beyond the requesting user's authorization boundary, causing confidential data to be exposed through raw responses, summaries, or aggregated outputs.

### What can go wrong?

Agents operating with broad data-access credentials can expose sensitive records belonging to other users, violate data segregation requirements, or leak aggregate information that reveals protected details. In regulated environments such as healthcare or finance, unauthorized data access can trigger breach notification obligations, regulatory penalties, and reputational damage.

### What are we going to do about it?

Data access by AI agents must follow the same least-privilege and per-request authorization principles applied to human users and traditional application code.

1. Enforce authorization checks at query time, not just at agent initialization. Every data retrieval must be validated against the identity and permissions of the requesting user.
2. Provision agent data connectors with the minimum access necessary for the task. Avoid shared service accounts that span multiple users or sensitivity levels.
3. Log all data-access operations with the user identity, query, and result set so access anomalies can be detected and audited.
4. Test data isolation by attempting to access records of other users through the agent interface and verifying that responses are properly restricted.
   