import { FileSystemHelper as _FileSystemHelper } from '$lib/filesystem/fileSystemHelper.js'
import { getAuthors } from '../../domain/author/authorController.js'

export function load({params: _params})
{
    return {
        authors : getAuthors()
    }
}

