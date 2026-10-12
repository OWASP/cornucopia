<script lang="ts">
    import Metadata from "$lib/components/metadata.svelte";
    import TextImage from '$lib/components/textImage.svelte';
    /** @type {{data: any}} */
    let { data } = $props();
</script>
{#if data.metadata}<Metadata metadata={data.metadata} />{/if}
<div class="error-message">
    <TextImage src="/images/cornucopia_logo_in_devs_we_trust.svg" align="left">
        <h2>Request failed. Even Cornucopia can't cope with infinity &infin;</h2>
        <p>Status: 404</p>
    </TextImage>
</div>
<style>
    .error-message
    {
        min-height: 80vh;
    }
</style>