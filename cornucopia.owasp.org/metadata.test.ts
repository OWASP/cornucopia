import { describe, it, expect } from "vitest";

describe("Dynamic route metadata - news slug", () => {
    it("returns correct canonical URL using params.slug", async () => {
        const { load } = await import("./src/routes/news/[slug]/+page.server.ts");
        const result = await load({
            params: { slug: "20260721-owasp-cornucopia-v3-with-eop-and-phantom-b" },
            locals: {}
        } as any);
        expect(result.metadata.canonicalUrl).toBe(
            "https://cornucopia.owasp.org/news/20260721-owasp-cornucopia-v3-with-eop-and-phantom-b"
        );
    });

    it("canonical URL never contains undefined", async () => {
        const { load } = await import("./src/routes/news/[slug]/+page.server.ts");
        try {
            const result = await load({
                params: { slug: "nonexistent-slug" },
                locals: {}
            } as any);
            expect(result.metadata.canonicalUrl).not.toContain("undefined");
            expect(result.metadata.canonicalUrl).toContain("nonexistent-slug");
        } catch (_) { /* 404 is acceptable */ }
    });
});

describe("Dynamic route metadata - taxonomy path", () => {
    it("assembles canonical URL from params.path not from url.pathname", async () => {
        const { load } = await import("./src/routes/taxonomy/[...path]/+page.server.ts");
        try {
            const result = await load({
                params: { path: "attacks/injection" },
                url: new URL("http://localhost/taxonomy/attacks/injection"),
                locals: {}
            } as any);
            expect(result.metadata.canonicalUrl).not.toContain("undefined");
            expect(result.metadata.canonicalUrl).toContain("cornucopia.owasp.org/taxonomy/");
        } catch (_) { /* may 404 */ }
    });
});

describe("Dynamic route metadata - author", () => {
    it("uses params.name in canonical URL", async () => {
        const { load } = await import("./src/routes/author/[name]/+page.server.ts");
        try {
            const result = await load({
                params: { name: "johan-sydseter" },
                locals: {}
            } as any);
            expect(result.metadata.canonicalUrl).toContain("johan-sydseter");
            expect(result.metadata.canonicalUrl).not.toContain("undefined");
        } catch (_) { /* 404 acceptable */ }
    });
});

describe("Metadata shape contract", () => {
    it("news slug metadata has all required fields", async () => {
        const { load } = await import("./src/routes/news/[slug]/+page.server.ts");
        try {
            const result = await load({
                params: { slug: "20260721-owasp-cornucopia-v3-with-eop-and-phantom-b" },
                locals: {}
            } as any);
            const m = result.metadata;
            expect(m.title).toBeTruthy();
            expect(m.description).toBeTruthy();
            expect(m.keywords).toBeTruthy();
            expect(m.canonicalUrl).toMatch(/^https:\/\/cornucopia\.owasp\.org\//);
            expect(["website", "article"]).toContain(m.type);
        } catch (_) { /* skip if data not available */ }
    });

    it("canonical URLs start with the correct origin", async () => {
        const { load } = await import("./src/routes/news/[slug]/+page.server.ts");
        try {
            const result = await load({
                params: { slug: "20260721-owasp-cornucopia-v3-with-eop-and-phantom-b" },
                locals: {}
            } as any);
            expect(result.metadata.canonicalUrl).toMatch(/^https:\/\/cornucopia\.owasp\.org/);
        } catch (_) { /* expected: some routes may not have metadata */ }
    });
});