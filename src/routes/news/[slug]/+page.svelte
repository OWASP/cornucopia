<script>
    import SvelteMarkdown from 'svelte-markdown'
    import renderers from '$lib/components/renderers/renderers';
    import BlogpostMetadata from '$lib/components/blogpostMetadata.svelte';
    import Utterances from '$lib/components/utterances.svelte';
    export let data;
    let blogpost = data.blogpost;
</script>

<BlogpostMetadata {blogpost}></BlogpostMetadata>
<SvelteMarkdown {renderers} source={blogpost.markdown}></SvelteMarkdown>
<Utterances delay={100} name={blogpost.title + ''}></Utterances>
<p>
    <a href="https://github.com/jefmeijvis/cornucopia.dotnetlab.eu/tree/master/data/news/{blogpost.path}/index.md">View this post on Github</a>
</p>

<style>
    p
    {
        text-align: center;
    }
</style>