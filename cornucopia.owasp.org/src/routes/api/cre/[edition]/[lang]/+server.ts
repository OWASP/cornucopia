import { json } from '@sveltejs/kit'
import { DeckService } from '$lib/services/deckService'
import type { RequestHandler } from './$types'
import { HTTP_STATUS } from '$lib/constants'

export const GET: RequestHandler = ({ params }) => {
  const { edition, lang } = params
  if (edition === '' || lang === '') {
    return json({ error: 'Missing params' }, { status: HTTP_STATUS.BAD_REQUEST })
  }

  const service = new DeckService()
  const version = DeckService.getLatestVersion(edition)
  const cards = service.getCardDataForEditionVersionLang(edition, version, lang)

  return json(Object.fromEntries(cards))
}
const editions = ["webapp", "mobileapp"]
const editions = ["webapp", "mobileapp", "dbd"]

export const GET: RequestHandler = ({ url }) => {
    const params = url.pathname.split('/');
    const edition =  params[params.length - 2] || 'webapp';
    const lang =  params[params.length - 1] || 'en';
    if (!(DeckService.getLanguages(edition)).includes(lang)) 
  error(404, 'Language not found. Only: ' + DeckService.getLanguages(edition).join(', ') + ' are supported.');
    if (!editions.includes(edition)) error(404, 'Edition not found. Only: ' + editions.join(', ') + ' are supported.');
    const deckService = new DeckService();
    const version = DeckService.getLatestVersion(edition);
    const cards = deckService.getCardDataForEditionVersionLang(edition, version, lang);
    
    if (!cards) error(500, "No cards retrieved.")
    const mappings = new MappingService().getCardMappingForLatestEdtions();
    if (!mappings) error(500, "No mappings retrieved.")
    return json((new CreController(cards, new MappingController(mappings.get(edition)))).getCreMapping(edition, lang));
};
