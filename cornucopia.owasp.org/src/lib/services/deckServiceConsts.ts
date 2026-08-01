/**
 * Constants for deck versions used throughout the application
 */
export const VERSION_WEBAPP = "webapp";
export const VERSION_MOBILEAPP = "mobileapp";
export const VERSION_COMPANION = "companion";
export const VERSION_DBD = "dbd";
export const VERSION_EOP = "eop";

export const EXTERNAL_DECK_EDITIONS = new Set<string>([VERSION_DBD]);

/**
 * Display name prefix for each edition, this is used for titles.
 */
export const EDITION_NAMES: Record<string, string> = {
    [VERSION_WEBAPP]: "OWASP Cornucopia",
    [VERSION_MOBILEAPP]: "OWASP Cornucopia",
    [VERSION_COMPANION]: "OWASP Cornucopia",
    [VERSION_DBD]: "Cornucopia",
    [VERSION_EOP]: "Elevation of Privilege"
};
