import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper";
import { error } from '@sveltejs/kit';
import { DeckService } from "$lib/services/deckService";
import type { Route } from "$domain/routes/route";
import { MappingService } from "$lib/services/mappingService";
import { CapecService } from "$lib/services/capecService";
import { DeckConfigService } from "$lib/services/deckConfigService";
import { getCardImagesByEdition, getSuitStylingByEdition } from "$lib/services/cardAppearanceLoader";
import { Text } from "$lib/utils/text.js";
import type { PageMetadata } from "$lib/types/metadata.js";
import type { PageServerLoad } from './$types';

export const load = (({ params }) => {
    const edition = params?.edition;
    const version = DeckService.getLatestVersion(edition);
    const asvsVersion = DeckConfigService.getAsvsVersion(edition, version);
    if (!DeckService.hasEdition(edition)) error(
      404, 'Edition not found. Only: ' + DeckService.getLatestEditions().join(', ') + ' are supported.');

    let capecData = undefined;
    if (DeckConfigService.hasCapecData(edition, version)) {
      capecData = CapecService.getCapecData(edition, version);
    }

    const fixedCode = legacyCardCodeFix(params.card.toUpperCase());
    const cards = new DeckService().getCardDataForEditionVersionLang(edition, version, 'en');
    const card = cards.get(fixedCode);

    const metadata: PageMetadata = {
        title: card
            ? `OWASP Cornucopia - ${Text.convertToTitleCase(card.suitName)} (${fixedCode})`
            : `OWASP Cornucopia - ${edition}`,
        description: card?.desc || `OWASP Cornucopia ${edition} card ${fixedCode}`,
        keywords: `OWASP, Cornucopia, ${edition}, ${fixedCode}`,
        canonicalUrl: `https://cornucopia.owasp.org/edition/${encodeURIComponent(edition)}/${encodeURIComponent(fixedCode)}`,
        type: 'website',
    };

    return {
      metadata,
      edition,
      version,
      versions: DeckService.getVersions(edition),
      lang: 'en',
      card: fixedCode,
      cards,
      routes: new Map<string, Route[]>([
        ['ASVSRoutes', FileSystemHelper.ASVSRouteMap(asvsVersion)]
      ]),
      mappingData: (new MappingService()).getCardMappingForLatestEdtions(),
      languages: DeckService.getLanguagesForEditionVersion(edition, version),
      capecData,
      cardImages: getCardImagesByEdition(),
      suitStyling: getSuitStylingByEdition(),
      editionName: DeckConfigService.getFullName(edition)
    };

    function legacyCardCodeFix(card: string) {
      return card.replace('COM', 'CM').replace('CO', 'C').replace('DVE', 'VE').replace('AC', 'AT');
    }

}) satisfies PageServerLoad;