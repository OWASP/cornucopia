import { createMobileMappingHandler } from '../../../mobileMapping.server';
import { MasweService } from '$lib/services/masweService';

export const prerender = true;

export const GET = createMobileMappingHandler({
    component: 'maswe',
    dataLoader: (edition, version) => MasweService.getMasweData(edition, version),
    missingDataMessage: 'No MASWE data found.'
});
