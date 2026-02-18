<script lang="ts">
    interface Props {
        path?: string;
    }

    let { path = "" }: Props = $props();

    const REPO_BASE = "https://github.com/OWASP/cornucopia";
    const BRANCH = "master";
    const SUBFOLDER = "cornucopia.owasp.org";

    let href = $derived.by(() => {
        if (!path) {
            return `${REPO_BASE}/tree/${BRANCH}/${SUBFOLDER}/data/cards/`;
        }
        // Normalize path: ensure no double slashes and correct path format
        let cleanPath = path.startsWith('./') ? path.substring(2) : path;
        cleanPath = cleanPath.startsWith('/') ? cleanPath.substring(1) : cleanPath;
        
        return `${REPO_BASE}/blob/${BRANCH}/${SUBFOLDER}/${cleanPath}`;
    });
</script>

<div>
    <a target="_blank" {href}>
        <img alt="Github logo" title="Github logo" src="/icons/github.png"/>
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
