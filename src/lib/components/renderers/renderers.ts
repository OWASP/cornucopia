import BlockQuote from '$lib/components/renderers/blockQuote.svelte';
import Code from '$lib/components/renderers/code.svelte';
import Heading from '$lib/components/renderers/heading.svelte';
import Image from '$lib/components/renderers/image.svelte';
import Link from '$lib/components/renderers/link.svelte';
import List from '$lib/components/renderers/list.svelte';
import ListItem from '$lib/components/renderers/listItem.svelte';
import Paragraph from '$lib/components/renderers/paragraph.svelte';
import Table from '$lib/components/renderers/table.svelte';
import TableCell from '$lib/components/renderers/tableCell.svelte';

let renderers =
{
    code : Code,
    heading : Heading,
    paragraph : Paragraph,
    list : List,
    listItem : ListItem,
    image : Image,
    blockquote : BlockQuote,
    link : Link,
    table : Table,
    tablecell: TableCell,
}

export default renderers;