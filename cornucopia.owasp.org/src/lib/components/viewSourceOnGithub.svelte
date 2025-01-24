<script lang="ts">

    let base : string = "https://github.com/OWASP/cornucopia/cornucopia.owasp.org/tree/master/data/cards/";
    //@TODO Would it be possible to link directly to the card?
    let href : string = base; //+ path;
</script>

<div>
    <a target="_blank" {href}>
        <img alt="Github logo" src="/icons/github.png"/>
        <span>View source on GitHub</span>
    </a>
</div>

<style>
    a
    {
        background: none;
        border: 1px white solid;
        display: flex;
        flex-shrink: 1;
        color:white;
        background-color: var(--background);
        border-radius: .5rem;
        margin:auto;
        padding: .5rem;
        margin-top: 4rem;
        margin-bottom: 2rem;
        cursor:pointer;
        width:max-content;
        text-decoration: none;
        transition: var(--transition);
        
    }

    a:hover
    {
        opacity: 50%;
    }

    a:active
    {
        font-weight: bold;
    }

    span
    {
        padding: .5rem;
    }
   
    img
    {
        width : 2rem;
    }
  </style>