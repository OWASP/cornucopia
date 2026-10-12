export type PageMetadata = {
    title: string;
    description: string;
    keywords: string;
    canonicalUrl: string;
    type?: 'website' | 'article';
    imageUrl?: string;
};