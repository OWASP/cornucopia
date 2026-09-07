import { expect, describe, it, vi, afterEach } from 'vitest';
import { DeckService } from './deckService';
import { MappingService } from './mappingService';
import { MappingController } from '$domain/mapping/mappingController';
import { getTaxonomyDisplayMappings } from '$lib/components/taxonomyMapping';

describe('MappingService tests', () => {

    afterEach(() => {
        vi.restoreAllMocks();
        MappingService.clear();
    });

    it("should return card mapping data.", async () => {
        expect((new MappingService()).getCardMappingForLatestEdtions()).toBeDefined();
        MappingService.clear();
        expect((new MappingService()).getCardMappingForAllVersions().get('webapp-2.2')).toBeDefined();
        expect((new MappingService()).getCardMappingForAllVersions().get('webapp-3.0')).toBeDefined();
        expect((new MappingService()).getCardMappingForAllVersions().get('mobileapp-1.1')).toBeDefined();
    }); 

    it('should handle missing mapping file gracefully', () => {
        const service = new MappingService();
        expect(service.getCardMapping('invalid-edition', '0.0')).toBeUndefined();
    });

    it('should return empty or default mapping for unknown data', () => {
        const service = new MappingService();
        expect(service.getCardMapping('webapp', 'invalid-version')).toBeUndefined();
    });

    it('should skip missing mapping files', () => {
        const service = new MappingService();
        const decks = DeckService.getDecks();

        service.getCardMappingForAllVersions();

        vi.spyOn(console, 'error').mockImplementation(() => undefined);
        vi.spyOn(DeckService, 'getDecks').mockReturnValue([
            ...decks,
            { edition: 'missing', version: '9.9', lang: ['en'] }
        ]);

        expect(service.getCardMappingForAllVersions().get('missing-9.9')).toBeUndefined();
    });

    it('should expose mobileapp labels and URL templates to the shared taxonomy', () => {
        const mappings = new MappingService().getCardMappingForAllVersions();

        for (const version of ['1.1', '2.0']) {
            const mapping = mappings.get(`mobileapp-${version}`);
            expect(mapping).toBeDefined();

            const controller = new MappingController(mapping as Record<string, unknown>);
            const cardMappings = controller.getCardMappings('PC4');
            const displayMappings = getTaxonomyDisplayMappings(cardMappings, controller.getLabels());

            expect(controller.getLabels()).toEqual(expect.objectContaining({
                capec: 'CAPEC™',
                safecode: 'SAFECode™',
            }));
            expect(controller.getUrlTemplates()).toEqual(expect.objectContaining({
                capec: '/taxonomy/capec-3.9/{code}',
                safecode: 'https://safecode.org/publication/SAFECode_Agile_Dev_Security0712.pdf',
            }));
            expect(displayMappings.map((item) => item.attribute)).toContain('capec');
            expect(displayMappings.map((item) => item.attribute)).not.toContain('threat');
            expect(displayMappings.map((item) => item.attribute)).not.toContain('attack_vector');
        }
    });

    it('should expose companion labels to the shared taxonomy', () => {
        const mapping = new MappingService().getCardMappingForAllVersions().get('companion-1.0');
        expect(mapping).toBeDefined();

        const controller = new MappingController(mapping as Record<string, unknown>);
        const displayMappings = getTaxonomyDisplayMappings(
            controller.getCardMappings('LLM3'),
            controller.getLabels(),
        );

        expect(controller.getLabels()).toEqual(expect.objectContaining({
            stride: 'STRIDE',
            owasp_aisvs: 'AISVS (1.0)',
            owasp_aitg: 'AITG (1.0)',
        }));
        expect(displayMappings.map((item) => item.attribute)).toEqual(expect.arrayContaining([
            'stride',
            'phantom-b',
            'cia',
            'owasp_aisvs',
            'owasp_aitg',
            'mitre_atlas',
            'owasp_llm_top10',
            'cwe',
        ]));

        const frontendMappings = getTaxonomyDisplayMappings(
            controller.getCardMappings('FRE7'),
            controller.getLabels(),
        );
        expect(frontendMappings.map((item) => item.attribute)).toEqual(expect.arrayContaining([
            'stride',
            'owasp_top-10_client_side',
            'owasp_top-10',
            'asvs',
            'mitre_attack',
        ]));
    });
});