/**
 * Mapping for the OWASP Developer Guide.
 */
export const DEV_GUIDE_MAPPING: Record<string, string[]> = {
  "1.1": ["0x01h-Configuration"],
  "1.2": ["0x01h-Configuration", "0x01b-File-System-Permissions"],
  "2.1": ["0x02h-Authentication"],
  "2.2": ["0x02h-Authentication", "0x02a-Passwords"],
  // ... (Add your other mappings here as needed)
} as const;

export type DevGuideKey = keyof typeof DEV_GUIDE_MAPPING;