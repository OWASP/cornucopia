<script lang="ts">
  interface Props {
    lang?: string;
    text: string;
  }

  let { lang = "javascript", text }: Props = $props();
  </script>

<p>{lang}</p>
<p>{text}</p>