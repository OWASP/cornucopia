import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper.js";
import type { ServerLoadEvent } from '@sveltejs/kit';

export function load({ params }: ServerLoadEvent): Record<string, unknown> {
    return {
        content: FileSystemHelper.getDataFromPath('data/website/pages/source')
    };
}