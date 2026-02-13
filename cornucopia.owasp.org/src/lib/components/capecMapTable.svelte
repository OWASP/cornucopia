<script lang="ts">
  interface CapecMapEntry {
    id: number;
    name: string;
    owasp_asvs: string[];
  }

  interface Props {
    capecMap: { [key: number]: { owasp_asvs: string[] } };
    capecData: { [key: number]: { name: string; owasp_asvs: string[] } };
    linkASVS: (input: string) => string;
  }

  let { capecMap, capecData, linkASVS }: Props = $props();

  const capecEntries = $derived(
    Object.entries(capecMap || {})
      .map(([id, data]) => ({
        id: Number(id),
        name: capecData[Number(id)]?.name || `CAPEC ${id}`,
        owasp_asvs: data.owasp_asvs || []
      }))
      .sort((a, b) => a.id - b.id)
  );

  function linkCapec(id: number): string {
    return `/taxonomy/capec-3.9/${id}`;
  }
</script>

{#if capecEntries.length > 0}
  <div class="capec-map-table">
    <table>
      <thead>
        <tr>
          <th>Code</th>
          <th>Title</th>
          <th>ASVS</th>
        </tr>
      </thead>
      <tbody>
        {#each capecEntries as entry}
          <tr>
            <td>
              <a href={linkCapec(entry.id)} title="CAPEC {entry.id}">{entry.id}</a>
            </td>
            <td>{entry.name}</td>
            <td class="asvs-links">
              {#each entry.owasp_asvs as asvs, index}
                <a href={linkASVS(asvs)} title="ASVS {asvs}">{asvs}</a>{#if index < entry.owasp_asvs.length - 1}, {/if}
              {/each}
            </td>
          </tr>
        {/each}
      </tbody>
    </table>
  </div>
{/if}

<style>
  .capec-map-table {
    width: 100%;
    overflow-x: auto;
    margin: 1rem 0;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    background: white;
    color: var(--background);
    font-family: var(--font-title);
  }

  thead {
    background: var(--background);
    color: white;
  }

  th,
  td {
    padding: 0.75rem;
    text-align: left;
    border: 1px solid #ddd;
    font-size: 1.5rem;
    font-weight: 400;
  }

  th {
    font-weight: 600;
  }

  tbody tr:nth-child(even) {
    background-color: #f9f9f9;
  }

  tbody tr:hover {
    background-color: #f0f0f0;
  }

  a {
    color: var(--background);
    text-decoration: underline;
  }

  a:hover {
    opacity: 0.8;
  }

  .asvs-links {
    word-break: break-word;
  }

  td:first-child {
    white-space: nowrap;
    width: 80px;
  }

  td:nth-child(2) {
    min-width: 200px;
  }
</style>
