<script lang="ts">
    export let url : string;
</script>

<div class="card-preview" data-umami-event="card-browser-card">
    <div class="card" style="background-image:linear-gradient(to bottom, rgba(255, 255, 255, 0.3), rgba(0, 0, 0, 0.2)),url('{url}')"/>
</div>

<style>
    .card
    {
        width : 100%;
        aspect-ratio: 20/32;
        border-radius: 1.2rem;
        background-position: 50% 50%;
        background-size: 117%;
        transition: var(--transition);
        margin-top: 2rem;
        box-shadow: rgba(255, 255, 255, 0.1) 0px 1px 1px 0px inset, rgba(50, 50, 93, 0.15) 0px 50px 100px -20px, rgba(0, 0, 0, 0.2) 0px 30px 60px -30px;
    }
</style>