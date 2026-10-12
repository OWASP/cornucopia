import {expect, describe, it} from 'vitest';
import { getMappingLabel, getMappingUrl, MappingController } from './mappingController';


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

        const mappingDataWithCards = {
            suits: [
                {
                    name: "Test Suit",
                    cards: [
                        {
                            id: "existing-card",
                            owasp_asvs: ["1.1"]
                        }
                    ]
                }
            ]
        };
        const controller3 = new MappingController(mappingDataWithCards);
        const webAppMapping3 = controller3.getWebAppCardMappings("non-existing-card");
        expect(webAppMapping3).toBeDefined();
        expect(Object.keys(webAppMapping3).length).toBe(0);
    });

    it("should return empty mapping when card id does not match existing cards.", async () => {
        const mappingData = {
            suits: [
                {
                    cards: [
                        {
                            id: "different-card"
                        }
                    ]
                }
            ]
        };
        const controller = new MappingController(mappingData);
        const mapping = controller.getCardMappings("missing-card");
        expect(mapping).toBeDefined();
        expect(Object.keys(mapping).length).toBe(0);
    });

    it("should return empty mapping when a suit is not a record or has no cards array.", async () => {
        const mappingData = {
            suits: [
                null,
                "not-a-suit",
                { name: "No cards array" },
                {
                    cards: [
                        { id: "match-me" }
                    ]
                }
            ]
        };
        const controller = new MappingController(mappingData);
        const mapping = controller.getCardMappings("match-me");
        expect(mapping.id).toBe("match-me");
    });

    it("should return undefined URL when attribute is undefined or template is missing.", () => {
        const controller = new MappingController({
            url_templates: { capec: "/taxonomy/capec/{code}" },
            suits: []
        });

        expect(getMappingUrl(controller.getUrlTemplates(), undefined, "1")).toBeUndefined();
        expect(getMappingUrl(controller.getUrlTemplates(), "missing", "1")).toBeUndefined();
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

    it("should return empty meta when meta is missing or not a record.", async () => {
        const controllerMissing = new MappingController({ suits: [] });
        expect(controllerMissing.getMeta()).toEqual({});

        const controllerArray = new MappingController({ meta: [1, 2], suits: [] });
        expect(controllerArray.getMeta()).toEqual({});
    });

    it("should return empty labels/url templates when missing, not an object, or an array.", () => {
        const missing = new MappingController({ suits: [] });
        expect(missing.getLabels()).toEqual({});
        expect(missing.getUrlTemplates()).toEqual({});

        const notObject = new MappingController({ labels: "invalid", url_templates: 42, suits: [] });
        expect(notObject.getLabels()).toEqual({});
        expect(notObject.getUrlTemplates()).toEqual({});

        const isArray = new MappingController({ labels: ["a"], url_templates: ["b"], suits: [] });
        expect(isArray.getLabels()).toEqual({});
        expect(isArray.getUrlTemplates()).toEqual({});
    });

    it("should return mapping labels and URL templates.", () => {
        const controller = new MappingController({
            labels: {
                capec: "CAPEC",
                invalid: 42
            },
            url_templates: {
                capec: "/taxonomy/capec/{code}",
                safecode: "https://example.com/safecode",
                invalid: false
            },
            suits: []
        });

        expect(controller.getLabels()).toEqual({ capec: "CAPEC" });
        expect(controller.getUrlTemplates()).toEqual({
            capec: "/taxonomy/capec/{code}",
            safecode: "https://example.com/safecode"
        });
        expect(getMappingLabel(controller.getLabels(), "capec")).toBe("CAPEC");
        expect(getMappingUrl(controller.getUrlTemplates(), "capec", "A/B")).toBe(
            "/taxonomy/capec/A%2FB"
        );
        expect(getMappingUrl(controller.getUrlTemplates(), "safecode", "ignored")).toBe(
            "https://example.com/safecode"
        );
    });
});
