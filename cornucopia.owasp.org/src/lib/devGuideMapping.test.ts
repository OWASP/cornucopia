import {expect, describe, it} from 'vitest';
import { DevGuideMapping } from './devguideMapping';

describe('DevGuideMapping tests', () => {
    it("should return a valid url for a given code.", async () => {
        expect(DevGuideMapping.getUrl("SC1-2")).toBe("https://devguide.owasp.org/en/04-design/02-web-app-checklist/01-secure-by-default/#1-system-configuration-sc");
        expect(DevGuideMapping.getUrl("SC")).toBe("https://devguide.owasp.org/en/04-design/02-web-app-checklist/01-secure-by-default/#1-system-configuration-sc");
        expect(DevGuideMapping.getUrl("SC3")).toBe("https://devguide.owasp.org/en/04-design/02-web-app-checklist/01-secure-by-default/#1-system-configuration-sc");
        expect(DevGuideMapping.getUrl("SDC1-3")).toBe("https://devguide.owasp.org/en/04-design/02-web-app-checklist/03-secure-database-access/#2-secure-database-configuration-sdc");
        expect(DevGuideMapping.getUrl("DOESNOTEXIST1-3")).toBe("");
    });
});