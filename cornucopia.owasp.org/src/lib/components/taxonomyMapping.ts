export interface TaxonomyDisplayMapping {
    attribute: string;
    label: string;
    values: string[];
}

const NON_DISPLAY = new Set([
    "id",
    "value",
    "url",
    "capec_map",
    "owasp_asvs",
    "owasp_dev_guide",
    "threat",
    "attack_vector",
]);

export function formatTaxonomyValue(value: unknown): string[] {
    if (value === undefined || value === null) return ["-"];
    if (Array.isArray(value)) return value.length ? value.map((item) => String(item)) : ["-"];
    return [String(value)];
}

export function getTaxonomyDisplayMappings(
    mappings: Record<string, unknown>,
    labels: Record<string, string>,
): TaxonomyDisplayMapping[] {
    return Object.keys(mappings)
        .filter((attribute) => !NON_DISPLAY.has(attribute) && !attribute.endsWith("_print"))
        .filter((attribute) => labels[attribute] !== undefined)
        .map((attribute) => ({
            attribute,
            label: labels[attribute] ? `${labels[attribute]}:` : "",
            values: formatTaxonomyValue(mappings[attribute]),
        }));
}
