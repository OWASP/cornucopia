<script lang="ts">
  interface Props {
    lang?: string;
    text: string;
  }

  let { lang = "javascript", text }: Props = $props();
  </script>

<div class="code-container">
  <p><strong>{lang}:</strong></p>
  <pre><code>{text}</code></pre>
</div>

<style>
  .code-container {
    margin: 1rem 0;
    border-radius: 0.5rem;
    background-color: #f8f9fa;
    border: 1px solid #e9ecef;
    overflow-x: auto;
    max-width: 100%;
    width: 100%;
  }

  .code-container p {
    margin: 0.5rem 1rem;
    font-family: ui-sans-serif, system-ui, sans-serif;
    font-size: 0.875rem;
    color: #6c757d;
  }

  pre {
    margin: 0;
    padding: 1rem;
    overflow-x: auto;
    font-family: 'Courier New', Courier, monospace;
    font-size: 0.875rem;
    line-height: 1.5;
    white-space: pre;
    word-wrap: normal;
    overflow-wrap: normal;
    max-width: 100%;
    width: 100%;
    box-sizing: border-box;
  }

  code {
    white-space: pre;
    word-wrap: normal;
    overflow-wrap: normal;
  }
</style>
