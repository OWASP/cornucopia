import { describe, expect, it } from "vitest";
import { getTaxonomyDisplayMappings } from "./taxonomyMapping";

describe("Taxonomy mapping display data", () => {
    it("keeps webapp mapping labels and values", () => {
        expect(
            getTaxonomyDisplayMappings(
                {
                    id: "VE2",
                    stride: ["I"],
                    capec: [54, 113],
                    owasp_asvs: ["2.4.1"],
                    stride_print: ["Information Disclosure"],
                },
                {
                    stride: "STRIDE",
                    capec: "CAPEC",
                    owasp_asvs: "OWASP ASVS",
                    stride_print: "",
                },
            ),
        ).toEqual([
            { attribute: "stride", label: "STRIDE:", values: ["I"] },
            { attribute: "capec", label: "CAPEC:", values: ["54", "113"] },
        ]);
    });

    it("keeps mobileapp mapping labels and values", () => {
        expect(
            getTaxonomyDisplayMappings(
                {
                    id: "PC2",
                    owasp_masvs: ["PLATFORM-3"],
                    owasp_mastg: ["MASTG-TEST-0010"],
                    safecode: ["-"],
                },
                {
                    owasp_masvs: "OWASP MASVS",
                    owasp_mastg: "OWASP MASTG",
                    safecode: "SAFECode",
                },
            ),
        ).toEqual([
            { attribute: "owasp_masvs", label: "OWASP MASVS:", values: ["PLATFORM-3"] },
            { attribute: "owasp_mastg", label: "OWASP MASTG:", values: ["MASTG-TEST-0010"] },
            { attribute: "safecode", label: "SAFECode:", values: ["-"] },
        ]);
    });

    it("keeps companion mapping labels and values", () => {
        expect(
            getTaxonomyDisplayMappings(
                {
                    id: "LLM2",
                    stride: ["D"],
                    "phantom-b": ["M"],
                    owasp_asvs: ["2.3.2"],
                    "phantom-b_print": ["Missing security engineering"],
                },
                {
                    stride: "STRIDE",
                    "phantom-b": "Phantom B",
                    owasp_asvs: "ASVS",
                    "phantom-b_print": "",
                },
            ),
        ).toEqual([
            { attribute: "stride", label: "STRIDE:", values: ["D"] },
            { attribute: "phantom-b", label: "Phantom B:", values: ["M"] },
        ]);
    });

    it("returns a placeholder for empty array values", () => {
        expect(
            getTaxonomyDisplayMappings(
                {
                    stride: [],
                },
                {
                    stride: "STRIDE",
                },
            ),
        ).toEqual([{ attribute: "stride", label: "STRIDE:", values: ["-"] }]);
    });
});
