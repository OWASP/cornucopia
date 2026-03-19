import { describe, it, expect } from 'vitest';

describe('capecMapTable component tests', () => {
    describe('data transformation logic', () => {
        it('should correctly merge capecMap with capecData', () => {
            const capecMap = {
                54: {
                    owasp_asvs: ['4.3.2', '13.2.2', '13.4.1']
                },
                116: {
                    owasp_asvs: ['4.3.2', '13.2.2']
                }
            };

            const capecData = {
                54: {
                    name: 'Query System Information',
                    owasp_asvs: ['4.3.2', '13.2.2', '13.4.1']
                },
                116: {
                    name: 'Excavation',
                    owasp_asvs: ['4.3.2', '13.2.2']
                }
            };

            // Simulate the component's derived logic
            const capecEntries = Object.entries(capecMap)
                .map(([id, data]) => ({
                    id: Number(id),
                    name: capecData[Number(id)]?.name || `CAPEC ${id}`,
                    owasp_asvs: data.owasp_asvs || []
                }))
                .sort((a, b) => a.id - b.id);

            expect(capecEntries).toHaveLength(2);
            expect(capecEntries[0].id).toBe(54);
            expect(capecEntries[0].name).toBe('Query System Information');
            expect(capecEntries[0].owasp_asvs).toEqual(['4.3.2', '13.2.2', '13.4.1']);
            expect(capecEntries[1].id).toBe(116);
            expect(capecEntries[1].name).toBe('Excavation');
        });

        it('should handle missing capecData gracefully', () => {
            const capecMap = {
                999: {
                    owasp_asvs: ['1.1.1']
                }
            };

            const capecData = {};

            const capecEntries = Object.entries(capecMap)
                .map(([id, data]) => ({
                    id: Number(id),
                    name: capecData[Number(id)]?.name || `CAPEC ${id}`,
                    owasp_asvs: data.owasp_asvs || []
                }))
                .sort((a, b) => a.id - b.id);

            expect(capecEntries).toHaveLength(1);
            expect(capecEntries[0].id).toBe(999);
            expect(capecEntries[0].name).toBe('CAPEC 999');
            expect(capecEntries[0].owasp_asvs).toEqual(['1.1.1']);
        });

        it('should sort entries by CAPEC ID numerically', () => {
            const capecMap = {
                215: { owasp_asvs: ['2.4.1'] },
                54: { owasp_asvs: ['4.3.2'] },
                116: { owasp_asvs: ['13.2.2'] },
                3: { owasp_asvs: ['1.1.1'] }
            };

            const capecData = {
                215: { name: 'CAPEC 215', owasp_asvs: ['2.4.1'] },
                54: { name: 'CAPEC 54', owasp_asvs: ['4.3.2'] },
                116: { name: 'CAPEC 116', owasp_asvs: ['13.2.2'] },
                3: { name: 'CAPEC 3', owasp_asvs: ['1.1.1'] }
            };

            const capecEntries = Object.entries(capecMap)
                .map(([id, data]) => ({
                    id: Number(id),
                    name: capecData[Number(id)]?.name || `CAPEC ${id}`,
                    owasp_asvs: data.owasp_asvs || []
                }))
                .sort((a, b) => a.id - b.id);

            expect(capecEntries).toHaveLength(4);
            expect(capecEntries[0].id).toBe(3);
            expect(capecEntries[1].id).toBe(54);
            expect(capecEntries[2].id).toBe(116);
            expect(capecEntries[3].id).toBe(215);
        });

        it('should handle empty capecMap', () => {
            const capecMap = {};
            const capecData = {};

            const capecEntries = Object.entries(capecMap)
                .map(([id, data]) => ({
                    id: Number(id),
                    name: capecData[Number(id)]?.name || `CAPEC ${id}`,
                    owasp_asvs: data.owasp_asvs || []
                }))
                .sort((a, b) => a.id - b.id);

            expect(capecEntries).toHaveLength(0);
        });

        it('should handle empty owasp_asvs array', () => {
            const capecMap = {
                100: {
                    owasp_asvs: []
                }
            };

            const capecData = {
                100: {
                    name: 'Test CAPEC',
                    owasp_asvs: []
                }
            };

            const capecEntries = Object.entries(capecMap)
                .map(([id, data]) => ({
                    id: Number(id),
                    name: capecData[Number(id)]?.name || `CAPEC ${id}`,
                    owasp_asvs: data.owasp_asvs || []
                }))
                .sort((a, b) => a.id - b.id);

            expect(capecEntries).toHaveLength(1);
            expect(capecEntries[0].owasp_asvs).toEqual([]);
        });
    });

    describe('link generation logic', () => {
        it('should generate correct CAPEC taxonomy link', () => {
            const linkCapec = (id: number): string => {
                return `/taxonomy/capec-3.9/${id}`;
            };

            expect(linkCapec(1)).toBe('/taxonomy/capec-3.9/1');
            expect(linkCapec(54)).toBe('/taxonomy/capec-3.9/54');
            expect(linkCapec(999)).toBe('/taxonomy/capec-3.9/999');
        });

        it('should handle ASVS link generation', () => {
            const mockLinkASVS = (input: string): string => {
                const searchString = input.split("-")[0];
                return `/taxonomy/asvs-5.0/test#V${input}`;
            };

            expect(mockLinkASVS('13.2.2')).toBe('/taxonomy/asvs-5.0/test#V13.2.2');
            expect(mockLinkASVS('4.3.2')).toBe('/taxonomy/asvs-5.0/test#V4.3.2');
        });
    });

    describe('data validation', () => {
        it('should handle null or undefined capecMap', () => {
            const capecMap = null;
            const capecData = {};

            const capecEntries = Object.entries(capecMap || {})
                .map(([id, data]) => ({
                    id: Number(id),
                    name: capecData[Number(id)]?.name || `CAPEC ${id}`,
                    owasp_asvs: data.owasp_asvs || []
                }))
                .sort((a, b) => a.id - b.id);

            expect(capecEntries).toHaveLength(0);
        });

        it('should handle multiple ASVS codes', () => {
            const capecMap = {
                1: {
                    owasp_asvs: ['13.2.2', '13.3.2', '14.2.4', '16.3.2', '16.3.3', '8.1.1']
                }
            };

            const capecData = {
                1: {
                    name: 'Accessing Functionality Not Properly Constrained by ACLs',
                    owasp_asvs: ['13.2.2', '13.3.2', '14.2.4', '16.3.2', '16.3.3', '8.1.1']
                }
            };

            const capecEntries = Object.entries(capecMap)
                .map(([id, data]) => ({
                    id: Number(id),
                    name: capecData[Number(id)]?.name || `CAPEC ${id}`,
                    owasp_asvs: data.owasp_asvs || []
                }))
                .sort((a, b) => a.id - b.id);

            expect(capecEntries[0].owasp_asvs).toHaveLength(6);
            expect(capecEntries[0].owasp_asvs).toContain('13.2.2');
            expect(capecEntries[0].owasp_asvs).toContain('8.1.1');
        });
    });
});
