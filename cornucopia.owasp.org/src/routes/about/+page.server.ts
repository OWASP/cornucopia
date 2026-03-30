import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper.js";
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = () => {
    const content = FileSystemHelper.getDataFromPath('data/website/pages/about');
    return {
        content
    };
};