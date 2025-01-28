<script>
    import SvelteMarkdown from 'svelte-markdown'
    import renderers from '$lib/components/renderers/renderers';
    import BlogpostMetadata from '$lib/components/blogpostMetadata.svelte';
    import {readTranslation} from "$lib/stores/stores";
    let t = readTranslation();
    /** @type {{data: any}} */
    let { data } = $props();
    let blogpost = data.blogpost;
</script>
<div>
<BlogpostMetadata {blogpost}></BlogpostMetadata>
<SvelteMarkdown {renderers} source={blogpost.markdown}></SvelteMarkdown>
<p>
    <a rel="noopener" href="https://github.com/OWASP/cornucopia/tree/master/cornucopia.owasp.org/data/news/{blogpost.path}/index.md">{$t('news.slug.p1')}</a>
</p>
</div>
<style>
    p
    {
        text-align: center;
    }

    @media (max-aspect-ratio: 1/1) 
    {
       div
       {
        margin: 0rem 1rem;
       }
    }
</style>