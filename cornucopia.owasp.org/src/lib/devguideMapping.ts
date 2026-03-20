/**
 * Mapping for the OWASP Developer Guide.
 * Renamed to DevGuideMapping to match the expected import in the Svelte UI components.
 */
export const DevGuideMapping: Record<string, string[]> = {
  "1.1": ["0x01h-Configuration"],
  "1.2": ["0x01h-Configuration", "0x01b-File-System-Permissions"],
  "2.1": ["0x02h-Authentication"],
  "2.2": ["0x02h-Authentication", "0x02a-Passwords"],
  // Add other mappings here as needed
};

export type DevGuideKey = keyof typeof DevGuideMapping;