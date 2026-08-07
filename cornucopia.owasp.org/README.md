# OWASP Cornucopia website

https://cornucopia.owasp.org contains the card browser for each of the cards in the cornucopia suits together with the taxonomy and in depth explaination for each of the cards in the suits.

## Production build

    npm run productionbuild

## Release to Cloudflare

To deploy the pages on a Cloudflare account, use the account id and the cloudflare api token with the following rights:

- Cloudflare Pages:Edit
- Workers Scripts:Edit
- Workers Routes:Edit
- User Details: Read

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

## Adding a new deck's images and styling

To add a deck with this image-based card style (a picture for each card, shown behind suit colors for the tab, watermark, and royal cards, like how the EoP deck looks), just add three files (no code changes needed):

- `source/{edition}-styling-{version}.yaml`: suit colors (tab, watermark, royal)

  ```yaml
  suits:
    <suit-name>:
      tab: "#hexcolor"
      watermark: "#hexcolor"
      royal: "#hexcolor"
  ```

- `source/{edition}-card-images-{version}.yaml`: image path for each card

  ```yaml
  cards:
    <cardId>:
      image: "/images/<edition>-cards/<file>.png"
  ```

- `src/lib/components/{edition}Card.css`: how that specific deck looks, using the `.card-render.{edition}` class and the `--tab` / `--watermark` / `--royal` colors. It loads automatically as long as the filename ends in `Card.css` (e.g. `eopCard.css`).

## Our Threat Model

You may review the threat model for cornucopia.owasp.org by using [OWASP Threat Dragon](https://www.threatdragon.com/#/dashboard) and opening [../ThreatDragonModels/cornucopia.json](../ThreatDragonModels/cornucopia.json).
