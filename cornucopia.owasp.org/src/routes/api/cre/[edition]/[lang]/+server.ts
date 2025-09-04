import { DeckService } from '$lib/services/deckService';
import { CreController } from '$domain/cre/creController';
import { json, error, type RequestHandler } from '@sveltejs/kit';
import { MappingController } from '$domain/mapping/mappingController';
// Header options
export const prerender = true;
const responseInit: ResponseInit = {
  headers: {
    "Content-Type": "application/json",
  },
};

const editions = ["webapp", "mobileapp"]
const languages = ["en", "no_nb", "nl", "es", "pt_pt", "pt_br", "ru", "fr", "it"]

export const GET: RequestHandler = ({ url }) => {
    const params = url.pathname.split('/');
    const edition =  params[params.length - 2] || 'webapp';
    const lang =  params[params.length - 1] || 'en';
    if (!languages.includes(lang)) error(404, 'Language not found. Only: ' + languages.join(', ') + ' are supported.');
    if (!editions.includes(edition)) error(404, 'Edition not found. Only: ' + editions.join(', ') + ' are supported.');
    const decks = new DeckService().getCardsForAllLanguages();
    if (!decks) error(500, "No decks retrieved.")
    const mappings = new DeckService().getCardMapping();
    if (!mappings) error(500, "No mappings retrieved.")
    return json((new CreController(decks.get(lang), new MappingController(mappings.get(edition)))).getCreMapping(edition));
};