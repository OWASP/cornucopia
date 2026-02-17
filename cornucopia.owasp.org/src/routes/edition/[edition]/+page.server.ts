import { DeckService } from '$lib/services/deckService';
import { error } from '@sveltejs/kit';
import { SuitController } from '$domain/suit/suitController';
import { FileSystemHelper } from '$lib/filesystem/fileSystemHelper';
import { MappingService } from '$lib/services/mappingService.js';

export const prerender = false;


export const load = (({ params }) => {
  const edition = params?.edition;

  if (!DeckService.hasEdition(edition)) {
    error(
      404,
      'Edition not found. Only: ' +
        DeckService.getLatestEditions().join(', ') +
        ' are supported.'
    );
  }

  const deckService = new DeckService();
  const version = DeckService.getLatestVersion(edition);

  const languages = DeckService.getLanguagesForEditionVersion(
    edition,
    version
  );

  const decks = new Map<string, any>();

  for (const lang of languages) {
    decks.set(
      lang,
      deckService.getCardDataForEditionVersionLang(
        edition,
        version,
        lang
      )
    );
  }

  return {
    suits: SuitController.getSuits(),
    decks: decks,
    mappingData: new MappingService().getCardMappingForLatestEdtions(),
    edition: edition,
    version: version,
    languages: languages,
    content: FileSystemHelper.getDataFromPath('data/website/pages/cards')
  };
});

