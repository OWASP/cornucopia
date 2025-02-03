<script lang="ts">
    import { Text } from "$lib/utils/text";

    export let commit : any;
    let date = new Date(commit.commit.committer.date);
</script>

<div class="container">
    <div class="heading">
        <div class="heading-left">
            <a target="_blank" href="{commit.committer?.html_url ?? ''}">
                <img title={commit.commit.author.name} alt={commit.commit.author.name} src={commit.committer.avatar_url}/>
            </a>
        </div>
        <div class="heading-center">
            <p>
                <a target="_blank" href="{commit.committer?.html_url ?? ''}">
                    {commit.commit.author.name} (<i>{commit.committer.login}</i>) {Text.FormatDateAsDate(date)}
                </a>

            </p>
        </div>
        <div class="heading-right">
            <button data-umami-event="github-commit-button" on:click={()=>window.open(commit.html_url,'_blank')}>
                {#if commit.status == 'success' || commit.status == 'pending'}
                    <img class="status" alt="success" src="/icons/success.png">
                {:else}
                    <img class="status" alt="failure" src="/icons/failure.png">
                {/if}
            </button>
        </div>
    </div>

    <p class="message" title="View commit details on GitHub">
        <a target="_blank" href="{commit.html_url}">
            {commit.commit.message}
        </a>
    </p>
</div>

<style>
    .message
    {
        padding: .5rem;
    }

    p
    {
        margin:1rem;
    }
    .status
    {
        width : 1rem;
        margin: 1rem;
    }

    *
    {
        font-family: var(--font-body);
    }
    .heading
    {
        display: flex;
        border-bottom: 1px rgba(255, 255, 255, 0.314) solid;
    }

    .heading-center
    {
        padding-left: 1rem;
    }

    .heading-right
    {
        margin-left: auto;
        order: 2;
    }

    img
    {
        width : 3rem;
    }

    .container
    {
        width : 100%;
        margin-bottom: 4rem;
        outline: 1px rgba(255, 255, 255, 0.314) solid;
        background-color: var(--background);
    }

    a
    {
        text-decoration: none;
        cursor:pointer;
        padding: 0;
        margin : 0;
    }

    a:hover
    {
        opacity: 70%;
    }

    button
    {
        padding: 0;
        margin: 0;
        background: none;
        border:none;
        cursor:pointer;
    }

    button:hover
    {
        opacity: 70%;
    }
</style>