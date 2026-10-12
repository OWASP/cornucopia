import { createMobileMappingHandler } from '../../../mobileMapping.server';
import { MastgService } from '$lib/services/mastgService';

export const prerender = true;

export const GET = createMobileMappingHandler({
    component: 'mastg',
    dataLoader: (edition, version) => MastgService.getMastgData(edition, version),
    missingDataMessage: 'No MASTG data found.'
});
