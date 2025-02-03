<script lang="ts">
    interface Props {
        mapping: any;
        style?: string;
    }

    let { mapping, style }: Props = $props();

    let mappingStyle = $state('');

    if (style) {
        mappingStyle = ' ' + style;
    }

</script>
        <p class="mapping-title{mappingStyle}">OWASP ASVS</p>
        <p class="mapping-value{mappingStyle}">{mapping.owasp_masvs || '-'}</p>
        <p class="mapping-title{mappingStyle}">OWASP AppSensor</p>
        <p class="mapping-value{mappingStyle}">{mapping.owasp_mastg || '-'}</p>
        <p class="mapping-title{mappingStyle}">CAPEC</p>
        <p class="mapping-value{mappingStyle}">{mapping.owasp_capec || '-'}</p>        
        <p class="mapping-title{mappingStyle}">SAFECODE</p>
<style>
    .mapping-title, .mapping-value
    {
        font-size: 1.1vw;
        margin:0;
        margin-left: .25rem;
        margin-right: .25rem;
    }

    .mapping-title
    {
        font-weight: bold;
    }

    .mapping-value
    {
        border-bottom: 1px rgb(192, 192, 192) solid;
    }

    .mapping-title.browser-card-container, .mapping-value.browser-card-container
    {
        font-size: 0.7vw;
        margin-left: 1vw;
        margin-right: 1vw;
    }

    @media (max-aspect-ratio: 1.5/1) 
    {
        .mapping-title.browser-card-container, .mapping-value.browser-card-container
        {
            font-size: 2vw;
            margin-left: 1vw;
            margin-right: 1vw;
        }
    }
</style>