import { FileSystemHelper } from '$lib/filesystem/fileSystemHelper.js';
import type { ServerLoadEvent } from '@sveltejs/kit';

export function load({ params }: ServerLoadEvent): Record<string, unknown> {
    return {
        content: FileSystemHelper.getDataFromPath('data/website/pages/taxonomy'),
        categories: getCategories()
    };
}

function getCategories(): string[] {
    return FileSystemHelper.getDirectories("./data/taxonomy/en");
}