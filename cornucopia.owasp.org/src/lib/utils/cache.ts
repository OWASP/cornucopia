import fs from 'node:fs'
import { CACHE } from '$lib/constants'

export async function LocalCache (func: () => unknown, cacheSeconds: number, description: string): Promise<unknown> {
  const filename: string = generateFilename(`async-${description}`)
  const [cacheStatusOk, cacheAge] = cacheIsOk(filename, cacheSeconds)
  let logMessage = `[LocalCacheAsync] Age is ${cacheAge} seconds.`

  if (cacheStatusOk) {
    logMessage += ` Found [${description}] in cache.`
    const responseAsString = fs.readFileSync(filename).toString()
    const kiloBytes = Math.round(Buffer.byteLength(responseAsString) / CACHE.KB)
    logMessage += `\t${kiloBytes} kb.`
    console.log(logMessage)
    return JSON.parse(responseAsString) as unknown
  }

  logMessage += ` ${description} not in cache, got from API`
  const result = func()
  const response: unknown = await Promise.resolve(result)
  const responseAsJSON = JSON.stringify(response)
  const kiloBytes = Math.round(Buffer.byteLength(responseAsJSON) / CACHE.KB)
  logMessage += `\t${kiloBytes} kb.`
  fs.writeFileSync(filename, responseAsJSON)
  console.log(logMessage)
  return response
}

export function LocalCacheSync (func: () => unknown, cacheSeconds: number, description: string): unknown {
  const filename: string = generateFilename(`sync-${description}`)
  const [cacheStatusOk, cacheAge] = cacheIsOk(filename, cacheSeconds)
  let logMessage = `[LocalCacheSync] Age is ${cacheAge} seconds.`

  if (cacheStatusOk) {
    logMessage += ` Found [${description}] in cache.`
    const responseAsString = fs.readFileSync(filename).toString()
    const kiloBytes = Math.round(Buffer.byteLength(responseAsString) / CACHE.KB)
    logMessage += `\t${kiloBytes} kb.`
    console.log(logMessage)
    return JSON.parse(responseAsString) as unknown
  }

  logMessage += ` ${description} not in cache, got from API`
  const result = func()
  const responseAsJSON = JSON.stringify(result)
  const kiloBytes = Math.round(Buffer.byteLength(responseAsJSON) / CACHE.KB)
  logMessage += `\t${kiloBytes} kb.`
  fs.writeFileSync(filename, responseAsJSON)
  console.log(logMessage)
  return result
}

function getSecondsAge (input: Date): number {
  const today = new Date()
  return Math.round(Math.abs(today.getTime() - input.getTime()) / CACHE.TIMEOUT_MS)
}

function generateFilename (input: string): string {
  return `cache/${input}.cache`
}

function cacheIsOk (path: string, maximumAge: number): [boolean, number] {
  const fileExists: boolean = fs.existsSync(path)
  if (!fileExists) return [false, CACHE.NO_RESULT]
  const stats = fs.statSync(path)
  const diff: number = getSecondsAge(stats.mtime)
  if (diff > maximumAge) return [false, diff]
  return [true, diff]
}