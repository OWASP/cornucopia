<script lang="ts">
    export let mapping : any;
    export let hero : string = '';
    let heroStyle = '';

    if (hero == 'yes') {
        heroStyle = ' hero-card-container';
    }

</script>
        <p class="mapping-title{heroStyle}">OWASP SCP</p>
        <p class="mapping-value{heroStyle}">{mapping.owasp_scp || '-'}</p>
        <p class="mapping-title{heroStyle}">OWASP ASVS</p>
        <p class="mapping-value{heroStyle}">{mapping.owasp_asvs || '-'}</p>
        <p class="mapping-title{heroStyle}">OWASP AppSensor</p>
        <p class="mapping-value{heroStyle}">{mapping.owasp_appsensor || '-'}</p>
        <p class="mapping-title{heroStyle}">CAPEC</p>
        <p class="mapping-value{heroStyle}">{mapping.owasp_capec || '-'}</p>        
        <p class="mapping-title{heroStyle}">SAFECODE</p>
        <p class="mapping-value{heroStyle}">{mapping.safecode || '-'}</p>
<style>
    .mapping-title, .mapping-value
    {
        font-size: max(.90vw,1vh);
        margin:0;
        margin-left: .25rem;
        margin-right: .25rem;
        word-wrap: break-word;
        white-space: initial;
    }
    .hero-card-container
    {
        font-size: max(0.3vh, 0.6vw);
    }

    .mapping-title
    {
        font-weight: bold;
    }

    .mapping-value
    {
        border-bottom: 1px rgb(192, 192, 192) solid;
    }
</style>