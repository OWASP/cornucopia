<script lang="ts">
  interface Props {
    edition: string;
    cardId: string;
    version: string;
    currentLanguage: string;
    languages: string[];
    versions: string[];
  }

  let { edition, cardId, version, currentLanguage, languages, versions }: Props = $props();

  let filteredLanguages =
  version === "3.0"
    ? ["en"]
    : Array.from(new Set(languages));

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

<div class="pickers">

  <div>
    <label for="version-select">Version:</label>
    <select
      id="version-select"
      value={version}
onchange={(e) => {
  const selectedVersion = (e.target as HTMLSelectElement).value;

  const targetLanguage =
    selectedVersion === "3.0" ? "en" : currentLanguage;

  window.location.href =
    `/edition/${edition}/${cardId}/${selectedVersion}/${targetLanguage}`;
}}
    >
      {#each versions as v}
        <option value={v} selected={v === version}>
          v{v}
        </option>
      {/each}
    </select>
  </div>

  <div>
    <label for="language-select">Language:</label>
    <select
      id="language-select"
      value={currentLanguage}
onchange={(e) => {
  const selectedLanguage = (e.target as HTMLSelectElement).value;

  window.location.href =
    `/edition/${edition}/${cardId}/${version}/${selectedLanguage}`;
}}
    >
      {#each filteredLanguages as lang}
        <option value={lang} selected={lang === currentLanguage}>
          {getLanguageName(lang)}
        </option>
      {/each}
    </select>
  </div>

</div>


<style>

.pickers {
  display: flex;
  gap: 1rem;
  margin: 1rem 0;
  flex-wrap: wrap;
  align-items: center;
}

.pickers > div {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

@media (max-aspect-ratio: 1/1) {
  .pickers {
    flex-direction: column;
    align-items: flex-start;
  }

  select {
    width: 100%;
  }
}

</style>
