import BlockQuote from '$lib/components/renderers/blockQuote.svelte';
import Code from '$lib/components/renderers/code.svelte';
import Heading from '$lib/components/renderers/heading.svelte';
import Image from '$lib/components/renderers/image.svelte';
import Link from '$lib/components/renderers/link.svelte';
import List from '$lib/components/renderers/list.svelte';
import ListForGeneralUse from '$lib/components/renderers/listForGeneralUse.svelte';
import ListItem from '$lib/components/renderers/listItem.svelte';
import ListItemForGeneralUse from '$lib/components/renderers/listItemForGeneralUse.svelte';
import Paragraph from '$lib/components/renderers/paragraph.svelte';
import Strong from '$lib/components/renderers/strong.svelte';
import Table from '$lib/components/renderers/table.svelte';
import TableCell from '$lib/components/renderers/tableCell.svelte';
import Em from '$lib/components/renderers/Em.svelte';

export const renderers =
{
    em: Em,
    code : Code,
    heading : Heading,
    paragraph : Paragraph,
    list : List,
    listItem : ListItem,
    image : Image,
    blockquote : BlockQuote,
    link : Link,
    strong : Strong,
    table : Table,
    tablecell: TableCell,
}

export const renderersForGeneralUse =
{
    em: Em,
    code : Code,
    heading : Heading,
    paragraph : Paragraph,
    list : ListForGeneralUse,
    listItem : ListItemForGeneralUse,
    image : Image,
    blockquote : BlockQuote,
    link : Link,
    strong : Strong,
    table : Table,
    tablecell: TableCell,
}