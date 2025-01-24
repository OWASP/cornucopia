<script>
    import SvelteMarkdown from 'svelte-markdown';
    import renderers from '$lib/components/renderers/renderers';
    import {readLang, readTranslation} from "$lib/stores/stores";

    /** @type {{data: any}} */
    let { data } = $props();
    let t = readTranslation();
    const lang = readLang();
    let content = data.content.get($lang) || data.content.get('en');
</script>

<div>
{#if content != ''}
<SvelteMarkdown {renderers} source={content}></SvelteMarkdown>
{/if}

    <h3>{$t('swags.h3.1')}</h3>
    <div class="image-container">
        <img alt="{$t('swags.alt.1')}" src="/images/swags/cornucopia_sticker_black_mobile.svg"/>
        <img alt="{$t('swags.alt.2')}" src="/images/swags/cornucopia_sticker_black.svg"/>
        <img alt="{$t('swags.alt.3')}" src="/images/swags/cornucopia_sticker_white.svg"/>
        <img alt="{$t('swags.alt.4')}" src="/images/swags/cornucopia_sticker_white_mobile.svg"/>
    </div>

    <h3>{$t('swags.h3.2')}</h3>
    <div class="image-container">
        <img alt="{$t('swags.alt.5')}" src="/images/swags/mc_version_in_devs_we_trust_back.png"/>
        <img alt="{$t('swags.alt.6')}" src="/images/swags/mc_version_in_devs_we_trust_front.png"/>
        <img alt="{$t('swags.alt.7')}" src="/images/swags/mc_version_in_devs_we_trust_mobile_left.png"/>
        <img alt="{$t('swags.alt.8')}" src="/images/swags/mc_version_in_devs_we_trust_mobile_right.png"/>
    </div>
    <h3>{$t('swags.h3.3')}</h3>
    <div class="image-container">
        <img alt="{$t('swags.alt.9')}" src="/images/swags/cornucopia_beer_glass.png"/>
        <img alt="{$t('swags.alt.10')}" src="/images/swags/cornucopia_beer_mug.png"/>
        <img alt="{$t('swags.alt.11')}" src="/images/swags/cornucopia_coffee_cup.png"/>
        <img alt="{$t('swags.alt.12')}" src="/images/swags/cornucopia_mugs.png"/>
        <img alt="{$t('swags.alt.13')}" src="/images/swags/cornucopia_october_fest_beer_mug.png"/>

    </div>
</div>

<style>
    
    .image-container
    {
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        justify-content: space-around;
        width: 100%;
    }

    img
    {
        width: 30%;
        margin-top: 1rem;
        filter: drop-shadow(0px 4px 5px #00000023);
    }

        @media (max-aspect-ratio: 1/1)
        {
            img
            {
                width : calc(100% - 4rem);
                margin-left: 2rem
            }
            div
            {
                margin: 0rem 1rem;
            }
        }
</style>