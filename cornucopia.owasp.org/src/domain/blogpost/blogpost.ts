export interface Blogpost {
  readonly title: string;
  readonly path: string;
  readonly author: string;
  readonly markdown: string;
  readonly tags: string[];
  readonly hidden: boolean;
  readonly date: string;
  readonly description?: string;
}