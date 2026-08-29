import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper";
import { error } from '@sveltejs/kit';
import { DeckService } from "$lib/services/deckService";
import type { Route } from "$domain/routes/route";
import { MappingService } from "$lib/services/mappingService";
import { CapecService } from "$lib/services/capecService";
import { getCardImagesByEdition, getSuitStylingByEdition } from "$lib/services/cardAppearanceLoader";
import { Text } from "$lib/utils/text.js";
import type { PageMetadata } from "$lib/types/metadata.js";
import type { PageServerLoad } from './$types';

export const load = (({ params }) => {
    const edition = params?.edition;
    const version = params?.version;
    const requestedLang = params?.lang ?? 'en';
    const availableLanguages = DeckService.getLanguagesForEditionVersion(edition, version);
    const lang = availableLanguages.includes(requestedLang) ? requestedLang : 'en';
    let asvsVersion: string = "4.0.3";
    if (params.version === '3.0') asvsVersion = '5.0';
    if (!DeckService.hasEdition(edition)) error(
      404, 'Edition not found. Only: ' + DeckService.getLatestEditions().join(', ') + ' are supported.');
    if (!DeckService.hasVersion(edition, version)) error(
      404, "Version not found for " + edition + ". Only: " + DeckService.getVersions(edition).join(', ') + " are supported.");

    let capecData = undefined;
    if (edition === 'webapp' && parseFloat(version) >= 3.0) {
      capecData = CapecService.getCapecData(edition, version);
    }

    const fixedCode = legacyCardCodeFix(params.card.toUpperCase());
    const cards = new DeckService().getCardDataForEditionVersionLang(edition, version, lang);
    const card = cards.get(fixedCode);

    const metadata: PageMetadata = {
        title: card
            ? `OWASP Cornucopia - ${Text.convertToTitleCase(card.suitName)} (${fixedCode})`
            : `OWASP Cornucopia - ${edition}`,
        description: card?.desc || `OWASP Cornucopia ${edition} card ${fixedCode}`,
        keywords: `OWASP, Cornucopia, ${edition}, ${fixedCode}`,
        canonicalUrl: `https://cornucopia.owasp.org/edition/${encodeURIComponent(edition)}/${encodeURIComponent(fixedCode)}/${encodeURIComponent(version)}`,
        type: 'website',
    };

    return {
      metadata,
      edition,
      version,
      versions: DeckService.getVersions(edition),
      lang,
      card: fixedCode,
      cards,
      routes: new Map<string, Route[]>([
        ['ASVSRoutes', FileSystemHelper.ASVSRouteMap(asvsVersion)]
      ]),
      mappingData: new Map<string, unknown>([
        [`${edition}`, (new MappingService()).getCardMappingForAllVersions().get(`${edition}-${version}`)]
      ]),
      languages: availableLanguages,
      capecData,
      cardImages: getCardImagesByEdition(),
      suitStyling: getSuitStylingByEdition()
    };

    function legacyCardCodeFix(card: string) {
      return card.replace('COM', 'CM').replace('CO', 'C').replace('DVE', 'VE').replace('AC', 'AT');
    }

}) satisfies PageServerLoad;