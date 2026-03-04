<img src="./resources/logos/cornucopia_logo.svg?raw=true" width="150">

[![OWASP Production Project](https://img.shields.io/badge/owasp-production%20project-brightgreen)](https://owasp.org/other_projects/)
[![OpenSSF Best Practices](https://bestpractices.coreinfrastructure.org/projects/7125/badge)](https://bestpractices.coreinfrastructure.org/projects/7125)
[![Maintainability](https://qlty.sh/gh/OWASP/projects/cornucopia/maintainability.svg)](https://qlty.sh/gh/OWASP/projects/cornucopia)
[![Code Coverage](https://qlty.sh/gh/OWASP/projects/cornucopia/coverage.svg)](https://qlty.sh/gh/OWASP/projects/cornucopia)

# OWASP Cornucopia project

OWASP Cornucopia is a mechanism in the form of a card game to assist software development teams identify security requirements in Agile, conventional and formal development processes. It is language, platform and technology agnostic.. Visit: <https://cornucopia.owasp.org/>

## Quick Setup (5 minutes)

### Prerequisites

- **Git LFS** - Install from <https://git-lfs.com/>
- **Node.js 20+** and **pnpm** - For website
- **Elixir 1.19+** and **Erlang/OTP** - For game engine  
- **PostgreSQL** - Database for game engine
- **Docker Desktop** (recommended) - Easy PostgreSQL setup

### Step 1: Get the code

```bash
git lfs pull
```

### Step 2: Security setup

**Windows PowerShell:**

```powershell
python -m pip install pre-commit
python -m pre_commit install
```

**Mac/Linux:**

```bash
pip install pre-commit
pre-commit install
```

### Step 3: Start PostgreSQL (Docker)

```bash
docker run --name copi_dev -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=POSTGRES_LOCAL_PWD -d postgres
```

### Step 4: Setup Website (SvelteKit)

```bash
cd cornucopia.owasp.org
pnpm install
pnpm run dev
# Visit http://localhost:5173
```

### Step 5: Setup Game Engine (Phoenix/Elixir)

```bash
cd copi.owasp.org
mix deps.get
mix ecto.setup
cd assets && npm install && cd ..
mix phx.server
# Visit http://localhost:4000
```

## Project Structure

- **cornucopia.owasp.org/** - Card browser website (SvelteKit)
- **copi.owasp.org/** - Online game engine (Phoenix/Elixir + PostgreSQL)
- **scripts/** - Card generation utilities
- **resources/** - Printable cards and assets

## Verification

```bash
# Website should respond
curl http://localhost:5173

# Game engine should respond  
curl http://localhost:4000

# Database should have cards
docker exec copi_dev psql -U postgres -d copi_dev -c "SELECT count(*) FROM cards;"
```

## Troubleshooting

- `mix not found` → Restart terminal after Elixir install
- `nxdomain:5432` → Start PostgreSQL first (Step 3)
- `database does not exist` → Run `mix ecto.setup` (Step 5)
- `SECRET_KEY_BASE missing` → Only needed for production

## The cross-references on the Web App Edition deck relate to the following versions of other OWASP and external resources

- [OWASP Dev Guide Web Application Checklist](https://devguide.owasp.org/en/04-design/02-web-app-checklist/)
- OWASP ASVS OWASP_Application_Security_Verification_Standard v4 (2019)
- OWASP AppSensor AppSensor_DetectionPoints
- CAPEC™ Mitre Common Attack Pattern Enumeration and Classification v3.9
- SAFECode SAFECode Practical Security Stories and Security Tasks for Agile Development Environments July 2012
- MASTG OWASP Mobile Application Security Testing Guide 1.7
- MASVS OWASP Mobile Application Security Verification Standard 2.1

## Printing

Download printable files from [pre-release](https://github.com/OWASP/cornucopia/releases/tag/pre-release).

**Card decks:**

- Bridge: 2.25 x 3.5" (57mm x 88.8mm)
- Tarot: 2.75 x 4.75" (71mm x 121mm)

**Paper:** 300gsm for cards

## Release Process

```bash
make release-patch    # Patch release
make release-minor    # Minor release  
make release-major    # Major release
```

## Credits

Created by Colin Watson with contributions from worldwide volunteers. See [About Cornucopia](https://cornucopia.owasp.org/about#Acknowledgements).

## License

Main content: [CC-BY-SA-4.0](./LICENSE.md)  
Copi game engine: [GNU AGPL](copi.owasp.org/LICENSE)  
Fonts: See [resources/templates/Fonts/README.md](./resources/templates/Fonts/README.md)

## Our Threat Models

You may review the threat model for Cornucopia and Copi by using [OWASP Threat Dragon](https://www.threatdragon.com/#/dashboard) and opening copi.json or cornucopia.json at [ThreatDragonModels](ThreatDragonModels).

Note: If you are looking into using Copi, it may be worth looking at some of [Copi's known threats](copi.owasp.org/README.md#our-threat-model) before doing so to make sure you have prepared yourself accordingly and taken our known threats into account.
