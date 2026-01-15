<script lang="ts">
  interface Props {
    edition: string;
    cardId: string;
    version: string;
    currentLanguage: string;
    languages: string[];
  }

  let { edition, cardId, version, currentLanguage, languages }: Props = $props();

  // Map language codes to display names
  const languageNames: Record<string, string> = {
    en: "English",
    es: "Español",
    fr: "Français",
    nl: "Nederlands",
    no_nb: "Norsk",
    pt_pt: "Português (PT)",
    pt_br: "Português (BR)",
    ru: "Русский",
    it: "Italiano",
    hu: "Magyar"
  };

  function getLanguageName(code: string): string {
    return languageNames[code] || code;
  }
</script>

<div class="language-picker">
  <label for="language-select">Language:</label>
  <select 
    id="language-select" 
    value={currentLanguage}
    onchange={(e) => {
      const selectedLanguage = (e.target as HTMLSelectElement).value;
      window.location.href = `/card/${edition}/${cardId}/${version}/${selectedLanguage}`;
    }}
  >
    {#each languages as lang}
      <option value={lang} selected={lang === currentLanguage}>
        {getLanguageName(lang)}
      </option>
    {/each}
  </select>
</div>

<style>
  .language-picker {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin: 1rem 0;
  }

  label {
    font-weight: bold;
    font-size: 1rem;
  }

  select {
    padding: 0.5rem;
    font-size: 1rem;
    border: 1px solid var(--background, #333);
    background-color: white;
    color: var(--background, #333);
    cursor: pointer;
    border-radius: 4px;
  }

  select:hover {
    opacity: 0.8;
  }

  select:focus {
    outline: 2px solid var(--background, #333);
    outline-offset: 2px;
  }

  @media (max-aspect-ratio: 1/1) {
    .language-picker {
      flex-direction: column;
      align-items: flex-start;
    }

    select {
      width: 100%;
    }
  }
</style>
