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
    gap: 1.5rem;
    margin: 1rem 0;
    flex-wrap: wrap;
    align-items: center;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  }

  .picker-group {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }

  label {
    font-weight: 700;
    color: #1f2937; /* Dark slate text from screenshot */
    font-size: 1.1rem;
  }

  /* Container to handle the custom arrow */
  .select-wrapper {
    position: relative;
    display: inline-block;
  }

  select {
    appearance: none; /* Remove default browser styling */
    background-color: #ffffff;
    border: 1.5px solid #374151; /* Thicker, darker border per screenshot */
    border-radius: 8px; /* Rounded corners */
    padding: 0.5rem 2.5rem 0.5rem 1rem; /* Extra right padding for arrow */
    font-size: 1rem;
    color: #1f2937;
    cursor: pointer;
    min-width: 140px;
    transition: border-color 0.2s;
  }

  select:focus {
    outline: none;
    border-color: #2563eb;
    box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.1);
  }

  /* Custom Chevron Arrow matching the screenshot */
  .select-wrapper::after {
    content: "";
    position: absolute;
    right: 1rem;
    top: 50%;
    transform: translateY(-50%);
    width: 0.8rem;
    height: 0.8rem;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%231f2937' stroke-width='2.5'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' d='M19 9l-7 7-7-7'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    pointer-events: none;
  }

  @media (max-aspect-ratio: 1/1) {
    .pickers {
      flex-direction: column;
      align-items: flex-start;
      gap: 1rem;
    }

    .select-wrapper, select {
      width: 100%;
    }
  }
</style>
