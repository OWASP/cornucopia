<script>
    import CookieNotice from "$lib/components/cookieNotice.svelte";
    import Footer from "$lib/components/footer.svelte";
    import Metadata from "$lib/components/metadata.svelte";
    import Navbar from "$lib/components/navigation/navbar.svelte";
    import {updateTranslation, updateLang} from "$lib/stores/stores";
    export let data;
    updateTranslation(data.translation, data.fallbackTranslation);
    updateLang(data.lang);
</script>

<Metadata></Metadata>
<CookieNotice></CookieNotice>

<div>
    <Navbar></Navbar>
    <div class="slot-container">
        <slot></slot>
    </div>
    <Footer timestamp={data.timestamp}></Footer>
</div>

<style>
    .slot-container
    {
        min-height: 100vh;
    }

    div
    {
        min-height: 100vh;
        background-color:var(--background-color);
    }
</style>