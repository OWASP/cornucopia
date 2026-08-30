<script>
    import Metadata from "$lib/components/metadata.svelte";
    import { Text } from "$lib/utils/text";
    import { resolve } from "$app/paths";
    import {readLang} from "$lib/stores/stores";
    import { renderersForGeneralUse } from '$lib/components/renderers/renderers';
    import SvelteMarkdown from "svelte-markdown";
    /** @type {{data: any}} */
    let { data } = $props();
    const lang = readLang();
    let content = $derived(data.content.get($lang) || data.content.get('en'));
</script>
{#if data.metadata}<Metadata metadata={data.metadata} />{/if}
<div>
{#if content != ''}
    <SvelteMarkdown renderers={renderersForGeneralUse} source={content}></SvelteMarkdown>
{/if}
{#each data.categories as category (category)}
    <p>ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚ÂÃƒÆ’Ã¢â‚¬Â¦ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚ÂÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚ÂÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬<a title="{Text.Format(category)}" href={resolve('/taxonomy/' + category.toLowerCase())}>{Text.Format(category)}</a></p>
{/each}
</div>
<style>
    p
    {
        margin:0;
    }

    a
    {
        text-decoration: none;
        font-weight: bold;
        color:var(--background);
        transition: var(--transition);
    }

    a:hover
    {
        opacity:50%;
    }
    @media (max-width: 767px)
    {
        div
        {
            margin: 0rem 1rem;
        }
    }
</style>

