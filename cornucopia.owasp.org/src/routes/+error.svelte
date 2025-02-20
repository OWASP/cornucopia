<script lang="ts">
    import { page } from '$app/state';
    import TextImage from '$lib/components/textImage.svelte';
</script>

<div class="error-message">
    <TextImage title="OWASP Cornucopia - In devs we trust" src="/images/cornucopia_logo_in_devs_we_trust.svg" align="left">
        <h2>Request failed. Even Cornucopia can't cope with infinity ∞</h2>
        <p>Status: {page.status}</p>
        <p>Message: {page.error?.message}</p>
    </TextImage>
</div>

<style>
    .error-message
    {
        min-height: 80vh;
    }
</style>