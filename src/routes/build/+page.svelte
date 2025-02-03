<script>
    import GithubCommit from "$lib/components/githubCommit.svelte";
    import ViewSourceOnGithub from "$lib/components/viewSourceOnGithub.svelte";
    export let data;
</script>

<div>
    <h1>Build information</h1>
    <p>This website is a static build from source.</p>
    <p>Latest build timestamp: {data.renderTimestamp}</p>
    <!--
    <h1>Latest deployments</h1>
    {#each data.commits as commit}
        <GithubCommit {commit}></GithubCommit>
    {/each}
    <ViewSourceOnGithub path=""></ViewSourceOnGithub>
    -->
</div>

<style>
        div
    {
        width : 50%;
        margin:auto;
        margin-top: 2rem;
    }

    p
    {
        font-family: var(--font-body);
    }

    h1
    {
      font-family: var(--font-title);
      background-color:var(--white);
      color: var(--background);
      padding: .5rem;
    }

    @media (max-aspect-ratio: 1/1) 
    {
       div
       {
        margin:auto;
        width : 90%;
       } 
    }
</style>