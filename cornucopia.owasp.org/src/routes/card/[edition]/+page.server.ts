import { DeckService } from '$lib/services/deckService';
import { error } from '@sveltejs/kit';
import { SuitController } from '$domain/suit/suitController';
import { FileSystemHelper } from '$lib/filesystem/fileSystemHelper';

const editions = ["webapp", "mobileapp"];
export const load = (({ params }) => {
  const edition = params?.edition;
  if (!DeckService.hasEdition(edition)) error(
      404, 'Edition not found. Only: ' + DeckService.getEditions().join(', ') + ' are supported.');
  return {
    suits : SuitController.getSuits(),
    decks :new DeckService().getCardsForAllLanguages(),
    mappingData: (new DeckService()).getCardMapping(),
    edition: params.edition,
    content: FileSystemHelper.getDataFromPath('data/website/pages/cards')
  };
});