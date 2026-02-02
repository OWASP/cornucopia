# OWASP Cornucopia website

https://cornucopia.owasp.org contains the card browser for each of the cards in the cornucopia suits together with the taxonomy and in depth explaination for each of the cards in the suits.

## Production buid

    npm run productionbuild

## Release to Cloudflare

To deploy the pages on a Cloudflare account, use the account id and the cloudflare api token with the following rights:

- Cloudflare Pages:Edit
- Workers Scripts:Edit
- Workers Routes:Edit

Github action is used for the deployment: https://github.com/OWASP/cornucopia/blob/b07827c4b7cf5fbd965d50144b51216cfdc6e214/.github/workflows/deploy-website-production.yml#L57

NB: The CLOUDFLARE_API_TOKEN needs to be renewed once a year.

## Development server

    # npm install will raise a conflict
    pnpm install # https://pnpm.io/installation
    npm run dev

## Testing and Code Coverage

Run tests with coverage reporting:

    npm run test

View coverage thresholds and results in the terminal output. Coverage reports are generated in the `./coverage` directory with the following formats:

- **Text**: Summary in terminal output
- **JSON**: `coverage/coverage-final.json`
- **LCOV**: `coverage/lcov.info` (for IDE integration)
- **HTML**: Open `coverage/index.html` in a browser for detailed line-by-line coverage

### Coverage Thresholds

The project enforces minimum coverage requirements:

- **Statements**: 95%
- **Branches**: 90%
- **Functions**: 100%
- **Lines**: 95%

Tests will fail if coverage drops below these thresholds.

## Our Threat Model

You may review the threat model for cornucopia.owasp.org by using [OWASP Threat Dragon](https://www.threatdragon.com/#/dashboard) and opening [../ThreatDragonModels/cornucopia.json](../ThreatDragonModels/cornucopia.json).
