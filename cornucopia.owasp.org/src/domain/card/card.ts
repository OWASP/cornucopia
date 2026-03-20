export interface Card {
  id: string
  edition: string
  version: string
  language: string
  suit: string
  suitId: string
  suitName: string
  suitNameLocal: string
  name: string
  url: string
  githubUrl: string
  concept: string
  summary: string
  desc: string
  prevous: string
  next: string
  [key: string]: unknown
}