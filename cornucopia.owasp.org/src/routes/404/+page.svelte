<script lang="ts">
    import TextImage from '$lib/components/textImage.svelte';
</script>
<div class="error-message">

    <TextImage src="/images/cornucopia_logo_in_devs_we_trust.svg" align="left">
        <h2>Request failed. Even Cornucopia can't cope with infinity ∞</h2>
        <p>Status: 404</p>
    </TextImage>
</div>

<style>
    .error-message
    {
        min-height: 80vh;
    }
</style>
