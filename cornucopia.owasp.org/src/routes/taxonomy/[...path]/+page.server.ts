import { FileSystemHelper } from '$lib/filesystem/fileSystemHelper'
import type { PageServerLoad } from './$types'
import { ZERO } from '$lib/constants'

export const load: PageServerLoad = ({ params }) => {
  const { path: currentPath } = params;
  const pathParts = currentPath.split('/').filter(p => p !== '')

  if (pathParts.length === ZERO) {
    return { 
      title: 'Taxonomy', 
      items: FileSystemHelper.ASVSRouteMap() 
    }
  }

  return {
    title: FileSystemHelper.getCurrentPageNameByRoute(currentPath),
    path: currentPath,
    items: FileSystemHelper.ASVSRouteMap().filter(item => item.Path.includes(currentPath))
  }
}