import { FileSystemHelper } from '$lib/filesystem/fileSystemHelper.js'
import { getAuthors } from '../../domain/author/authorController.js'

export function load({params})
{
    return {
        authors : getAuthors()
    }
}