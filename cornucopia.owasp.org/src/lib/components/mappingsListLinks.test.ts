import { describe, expect, it, vi } from "vitest";
import { isLocalMappingLink, resolveMappingLink } from "./mappingsListLinks";

describe("mappings list link resolution", () => {
    it("identifies root-relative links as local", () => {
        expect(isLocalMappingLink("/taxonomy/capec/1")).toBe(true);
    });

    it("identifies hash links as local", () => {
        expect(isLocalMappingLink("#mapping")).toBe(true);
    });

    it("does not identify external links as local", () => {
        expect(isLocalMappingLink("https://example.com/mapping")).toBe(false);
    });

    it("does not identify missing links as local", () => {
        expect(isLocalMappingLink(undefined)).toBe(false);
    });

    it("resolves local links with the configured path resolver", () => {
        const resolvePath = vi.fn((path: string) => `/base${path}`);

        expect(resolveMappingLink("/taxonomy/capec/1", resolvePath)).toBe(
            "/base/taxonomy/capec/1",
        );
        expect(resolvePath).toHaveBeenCalledWith("/taxonomy/capec/1");
    });

    it("resolves hash links with the configured path resolver", () => {
        const resolvePath = vi.fn((path: string) => `/base${path}`);

        expect(resolveMappingLink("#mapping", resolvePath)).toBe("/base#mapping");
    });

    it("leaves external links unchanged", () => {
        const resolvePath = vi.fn((path: string) => `/base${path}`);

        expect(resolveMappingLink("https://example.com/mapping", resolvePath)).toBe(
            "https://example.com/mapping",
        );
        expect(resolvePath).not.toHaveBeenCalled();
    });

    it("returns missing links unchanged", () => {
        const resolvePath = vi.fn((path: string) => `/base${path}`);

        expect(resolveMappingLink(undefined, resolvePath)).toBeUndefined();
        expect(resolvePath).not.toHaveBeenCalled();
    });
});
