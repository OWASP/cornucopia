import {expect, describe, it} from 'vitest';
import { MappingController } from './mappingController';


describe('MappingController tests', () => {
    it("should return web app card mapping data.", async () => {
        
        const mappingData = {
            suits: [
                {
                    name: "Test Suit",
                    cards: [
                        {
                            id: "webapp-1",
                            owasp_asvs: ["1.1", "1.2"],
                            name: "Test Card"
                        }
                    ]
                }
            ]
        };
        const controller = new MappingController(mappingData);

        const webAppMapping = controller.getWebAppCardMappings("webapp-1");
        expect(webAppMapping).toBeDefined();
        expect(webAppMapping.id).toBe("webapp-1");
        expect(webAppMapping.owasp_asvs).toEqual(["1.1", "1.2"]);
    });

    it("should return mobile app card mapping data.", async () => {
        
        const mappingData = {
            suits: [
                {
                    name: "Test Suit",
                    cards: [
                        {
                            id: "mobileapp-1",
                            owasp_masvs: ["MASVS-1", "MASVS-2"],
                            owasp_mastg: ["MASTG-1"],
                            capec: [1, 2],
                            safecode: [101, 102]
                        }
                    ]
                }
            ]
        };
        const controller = new MappingController(mappingData);
        const mobileAppMapping = controller.getMobileAppCardMappings("mobileapp-1");
        expect(mobileAppMapping).toBeDefined();
        expect(mobileAppMapping.id).toBe("mobileapp-1");
        expect(mobileAppMapping.owasp_masvs).toEqual(["MASVS-1", "MASVS-2"]);
        expect(mobileAppMapping.capec).toEqual([1, 2]);
        expect(mobileAppMapping.safecode).toEqual([101, 102]);

    });

    it("should return empty mapping for non-existing card.", async () => {
        const mappingData = {
            suits: []
        };
        const controller = new MappingController(mappingData);
        const webAppMapping = controller.getWebAppCardMappings("non-existing-card");
        expect(webAppMapping).toBeDefined();
        expect(Object.keys(webAppMapping).length).toBe(0);

        const controller2 = new MappingController({});
        const webAppMapping2 = controller2.getWebAppCardMappings("non-existing-card");
        expect(webAppMapping2).toBeDefined();
        expect(Object.keys(webAppMapping2).length).toBe(0);
    });

    it("should return meta information.", async () => {
        const mappingData = {
            meta: { version: "1.0", date: "2024-01-01" },
            suits: []
        };
        const controller = new MappingController(mappingData);
        const meta = controller.getMeta();
        expect(meta).toBeDefined();
        expect(meta.version).toBe("1.0");
        expect(meta.date).toBe("2024-01-01");
    });
});