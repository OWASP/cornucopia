import { MappingService } from '$lib/services/mappingService'
import type { LayoutServerLoad } from './$types'

export const load: LayoutServerLoad = () => {
  const service = new MappingService()
  const mappingData = service.getCardMappingForLatestEdtions()
  const result: Record<string, unknown> = {}

  for (const [key, value] of mappingData.entries()) {
    result[key] = value
  }

  return { mappings: result }
}