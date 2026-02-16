import { DeckService } from "$lib/services/deckService";
import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper";
import { MappingService } from "$lib/services/mappingService";
import type { PageServerLoad } from "./$types";
import type { Route } from "$domain/routes/route";
import type { Card } from "$domain/card/card";
import { error } from "@sveltejs/kit";
import { redirect } from "@sveltejs/kit";

export const load: PageServerLoad = ({ params }) => {
  const edition = "webapp";
  const version = "2.2";
  const lang = "en";

  throw redirect(
    302,
    `/edition/${edition}/${params.card?.toUpperCase()}/${version}/${lang}`
  );

  const card = cards.get(cardId) as Card;

  if (!card) {
    throw error(404, "Card not found");
  }

  return {
    edition,
    card: cardId,
    version,
    lang,
    cards,
    versions: DeckService.getVersions(edition),
    languages: DeckService.getLanguages(edition),
    routes: new Map<string, Route[]>([
      ["ASVSRoutes", FileSystemHelper.ASVSRouteMap()]
    ]),
    mappingData: new MappingService().getCardMappingForLatestEdtions()
  };

  function legacyCardCodeFix(card: string) {
    return card.replace("COM", "CM")
               .replace("CO", "C")
               .replace("DVE", "VE")
               .replace("AC", "AT");
  }
};

