import fs from 'node:fs'
import type { Route } from '../../domain/routes/route'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { ZERO, ONE } from '$lib/constants'

export function getFileSystemRoot (): string {
  if (import.meta.url.includes('.svelte-kit')) {
    return path.normalize(`${path.dirname(fileURLToPath(import.meta.url))}/../../../../`)
  }
  return path.normalize(`${path.dirname(fileURLToPath(import.meta.url))}/../../../`)
}

export const fileSystemRoot = getFileSystemRoot()

export function hasDir (dirPath: string): boolean {
  return fs.existsSync(dirPath)
}

export function hasFile (filePath: string): boolean {
  return fs.existsSync(filePath) && fs.lstatSync(filePath).isFile()
}

export function getDirectories (dirPath: string): string[] {
  return fs
    .readdirSync(dirPath, { withFileTypes: true })
    .filter((x) => x.isDirectory())
    .map((dirent) => dirent.name)
}

export function getFiles (dirPath: string): string[] {
  return fs
    .readdirSync(dirPath, { withFileTypes: true })
    .filter((x) => x.isFile())
    .map((dirent) => dirent.name)
}

export function resolveCaseInsensitivePath (basePath: string, relativePath: string): string {
  const parts = relativePath.split('/').filter(p => p.length > ZERO)
  let currentPath = path.normalize(basePath)
  for (const part of parts) {
    const resolvedPart = fs.existsSync(currentPath)
      ? (fs.readdirSync(currentPath, { withFileTypes: true })
          .find(entry => entry.name.toLowerCase() === part.toLowerCase())
          ?.name ?? part)
      : null
    if (resolvedPart === null) return path.join(basePath, relativePath)
    currentPath = path.join(currentPath, resolvedPart)
  }
  return currentPath
}

export function ASVSRouteMap (version = '4.0.3'): Route[] {
  const basePath = `data/taxonomy/en/ASVS-${version}`
  const sectionRegex = /^(?:\d{2})-/
  const captureRegex = /^(?<section>\d{2})-/
  const routes: Route[] = []
  const firstLevelDirs = getDirectories(fileSystemRoot + basePath).filter(dir => sectionRegex.test(dir))
  for (const firstLevelDir of firstLevelDirs) {
    const firstLevelPath = `${basePath}/${firstLevelDir}`
    const firstPart = captureRegex.exec(firstLevelDir)?.groups?.section
    const secondLevelDirs = getDirectories(fileSystemRoot + firstLevelPath).filter(dir => sectionRegex.test(dir))
    for (const secondLevelDir of secondLevelDirs) {
      const secondPart = captureRegex.exec(secondLevelDir)?.groups?.section
      const section = `${firstPart ?? ''}.${secondPart ?? ''}`
      const fullPath = `${firstLevelPath}/${secondLevelDir}`.replace('data/taxonomy/en', '/taxonomy')
      routes.push({ Path: fullPath, Section: section })
    }
  }
  return routes
}

export function getCurrentPageNameByRoute (route: string): string {
  return route === '' ? 'Requirements Mapping' : route.split('/').slice(-ONE)[ZERO]
}

export function getDataByRoute (route: string, lang = 'en'): [string[], string] {
  const categories: string[] = []
  const baseDataPath = `${fileSystemRoot}data`
  const langPattern = `taxonomy/${lang}`
  const routeHasLang = route.includes(langPattern)
  const resolvedRoute = routeHasLang
    ? route
    : route.replace(/taxonomy\/?/, `${langPattern}/`)
  const defaultLangRoute = resolvedRoute.replace(`/taxonomy/${lang}`, '/taxonomy/en')
  let content = getDataFromPath(`data${resolvedRoute}`).get(`data${resolvedRoute}`) ?? ''
  if (content === '') {
    content = getDataFromPath(`data${defaultLangRoute}`).get(`data${defaultLangRoute}`) ?? ''
  }
  const resolvedPath = resolveCaseInsensitivePath(baseDataPath, defaultLangRoute)
  if (fs.existsSync(resolvedPath) && fs.lstatSync(resolvedPath).isDirectory()) {
    for (const folder of getDirectories(resolvedPath)) categories.push(folder)
  }
  return [categories, content]
}

export function getDataFromPath (filePath: string): Map<string, string> {
  const content = new Map<string, string>()
  const resolvedPath = resolveCaseInsensitivePath(fileSystemRoot, filePath)
  const indexFile = path.join(resolvedPath, 'index.md')
  if (fs.existsSync(indexFile)) content.set(filePath, fs.readFileSync(indexFile, 'utf8'))
  const folders = (() => {
    try { return getDirectories(resolvedPath) } catch { return [] }
  })()
  for (const folder of folders) {
    const folderIndexFile = path.join(resolvedPath, folder, 'index.md')
    if (fs.existsSync(folderIndexFile)) content.set(folder, fs.readFileSync(folderIndexFile, 'utf8'))
  }
  return content
}

export const FileSystemHelper = {
  root: fileSystemRoot,
  hasDir,
  hasFile,
  getDirectories,
  getFiles,
  resolveCaseInsensitivePath,
  ASVSRouteMap,
  getCurrentPageNameByRoute,
  getDataByRoute,
  getDataFromPath
}