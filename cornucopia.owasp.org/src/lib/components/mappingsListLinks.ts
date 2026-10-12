export type PathResolver = (path: string) => string;

export function isLocalMappingLink(link: string | undefined): boolean {
    return link?.startsWith("/") === true || link?.startsWith("#") === true;
}

export function resolveMappingLink(
    link: string | undefined,
    resolvePath: PathResolver,
): string | undefined {
    if (link === undefined) return undefined;
    return isLocalMappingLink(link) ? resolvePath(link) : link;
}
