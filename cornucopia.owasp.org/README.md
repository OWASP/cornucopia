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

## Registering a deck

To publish a new edition/version, add a block under `decks:` in `decks.yaml`:

```yaml
decks:
  - edition: newdeck                    # matches source/newdeck-cards-*.yaml filenames
    displayName: "OWASP Cornucopia"     # short name, prefixed on card-browser titles
    fullName: "New Deck Edition"        # full name, used in card-detail page titles
    cre:
      name: "OWASP Cornucopia New Deck Edition"  # edition name in the CRE export
      category: "New Deck"                         # edition category in the CRE export
    external: false                     # true = links out to another site, no /edition/... pages here (see dbd)

    # only needed when external is false - render the deck's button/intro text on
    # /cards and /edition/[edition]; the translation keys must already exist in the locale files
    defaultPreviewCard: AB1
    buttonLabelKey: cards.button.5
    descriptionHeadingKey: cards.h2.5
    descriptionBodyKey: cards.p6

    # optional - only if this deck has ASVS/CAPEC requirement mappings (see webapp in decks.yaml)
    standards:
      asvs:
        versionMap:
          "1.0": "4.0.3"
      capec:
        minVersion: "1.0"

    versions:
      - version: "1.0"                  # a version not listed here stays a draft, invisible to
                                         # the site, even if its source/newdeck-cards-1.0-*.yaml
                                         # files already exist
        draftLanguages: [de]            # optional - keep one language of a published version
                                         
```

All languages of a listed version are picked up automatically, unless listed under `draftLanguages`.

### Order matters

Two things are picked positionally, not computed, so getting the order wrong fails silently
instead of throwing an error:

- The first non-external deck under `decks:` is the one the card browser defaults to.
- Under `versions:`, the **last** entry is the "latest" - list them oldest-first.

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
