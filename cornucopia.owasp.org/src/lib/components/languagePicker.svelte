<script lang="ts">
  interface Props {
    edition: string;
    cardId: string;
    version: string;
    currentLanguage: string;
    languages: string[];
  }

  let { edition, cardId, version, currentLanguage, languages }: Props = $props();

  const languageNames: Record<string, string> = {
    en: "English", es: "Español", fr: "Français", nl: "Nederlands",
    no_nb: "Norsk", pt_pt: "Português (PT)", pt_br: "Português (BR)",
    ru: "Русский", it: "Italiano", hu: "Magyar"
  };

  function getLanguageName(code: string): string {
    return languageNames[code] || code;
  }

  function changeLanguage(e: Event) {
    const selectedLanguage = (e.target as HTMLSelectElement).value;
    // Navigate using full route format
    window.location.href = `/edition/${edition}/${cardId}/${version}/${selectedLanguage}`;
  }
</script>

<div class="language-picker">
  <label for="language-select">Language:</label>
  <select id="language-select" bind:value={currentLanguage} on:change={changeLanguage}>
    {#each languages as lang}
      <option value={lang}>{getLanguageName(lang)}</option>
    {/each}
  </select>
</div>


<style>
.language-picker {
  display: flex;
  flex-direction: column; /* label on top, dropdown below */
  gap: -0.5rem; /* increased from 0.25rem for more spacing */
  min-width: 150px;
}

.language-picker label {
  font-weight: bold;
  font-size: 0.95rem;
  text-align: left;
  margin-bottom: 0.5rem; /* added space below label */
}

.language-picker select {
  padding: 0.5rem 0.6rem;
  font-size: 0.95rem;
  border: 1px solid var(--background, #333);
  border-radius: 5px;
  background-color: white;
  color: var(--background, #333);
  cursor: pointer;
  width: 100%;
  box-sizing: border-box;
}

.language-picker select:hover {
  opacity: 0.9;
}

.language-picker select:focus {
  outline: 2px solid var(--background, #333);
  outline-offset: 2px;
}

/* Horizontal alignment with version dropdown */
.selectors {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  align-items: flex-end;
}

.selector {
  display: flex;
  flex-direction: column;
  min-width: 150px;
}

/* Mobile / narrow screens */
@media (max-width: 768px) {
  .selectors {
    flex-direction: column;
    align-items: flex-start;
  }
  .selector {
    width: 100%;
  }
}
</style>
