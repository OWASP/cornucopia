<script>
    import { Text } from "$lib/utils/text";
    import {readLang, readTranslation} from "$lib/stores/stores";

    export let data;
    let t = readTranslation();
    const lang = readLang();
</script>
<div>
<h1 id="taxonomy">{$t('taxonomy.h1')}</h1>

{#each data.categories as category}
    <p>├──<a href="/taxonomy/{category}">{Text.Format(category)}</a></p>
{/each}
</div>
<style>
    p
    {
        font-size: 1.5rem;
        margin:0;
    }

    div
    {
        padding-left : 1rem;
        width : 95%;
        margin: auto;
        font-size: 1.2rem;
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
</style>