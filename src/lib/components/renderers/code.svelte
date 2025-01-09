<script lang="ts">
  interface Props {
    lang?: string;
    text: string;
  }

  let { lang = "javascript", text }: Props = $props();
  </script>

<p><strong>{lang}:</strong></p>
<p>{text}</p>
<style>
  p {
    font-family: 'Courier New', Courier, monospace;
    white-space: pre;
  }
</style>