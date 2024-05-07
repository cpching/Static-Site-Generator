from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import text_to_textnodes, text_node_to_html_node

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"

class Blcok():
    def __init__(self, text) -> None:
        self.text = text
        # self.
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_types = [block_to_block_type(block) for block in blocks]
    children_htmlnodes = []
    for block_type, block_text in zip(block_types, blocks):
        # print(f"block_type: {block_type}")
        # print(f"block_text: {block_text}")
        children_htmlnodes.append(block_type_to_htmlnode(block_type, block_text))
    return ParentNode("div", children_htmlnodes)

def markdown_to_blocks(text):
    blocks = text.split("\n\n")
    return [block.strip() for block in blocks if block.strip()]

def block_to_block_type(block_text):
    lines = block_text.split('\n')

    if len(lines) == 1 and all(c == '#' for c in lines[0].split()[0]):
        return block_type_heading

    elif len(block_text) >=6 and block_text[:3] == block_text[-3:] == "```":
        return block_type_code

    elif all( line[:2] == "> " for line in lines ):
        return block_type_quote

    elif all( line[:2] == "- " or line[:2] == "* " for line in lines ):
        return block_type_unordered_list
    
    elif all( line[:3]==f"{i+1}. "  for i, line in enumerate(lines)):
        return block_type_ordered_list

    else:
        return block_type_paragraph

def block_type_to_htmlnode(block_type, block_text):
    if block_type == "paragraph":
        return block_type_paragraph_to_htmlnode(block_text)

    if block_type == "heading":
        return block_type_heading_to_htmlnode(block_text)

    if block_type == "code":
        return block_type_code_to_htmlnode(block_text)

    if block_type == "quote":
        return block_type_quote_to_htmlnode(block_text)

    if block_type == "unordered_list":
        return block_type_unordered_list_to_htmlnode(block_text)

    if block_type == "ordered_list":
        return block_type_ordered_list_to_htmlnode(block_text)

def block_type_paragraph_to_htmlnode(block_text):
    text_nodes = text_to_textnodes(block_text)
    return ParentNode("p", [text_node_to_html_node(text_node) for text_node in text_nodes])

def block_type_heading_to_htmlnode(block_text):
    heading_num = len(block_text.split()[0])
    text_nodes = text_to_textnodes(" ".join(block_text.split()[1:]))
    return ParentNode(f"h{heading_num}", [text_node_to_html_node(text_node) for text_node in text_nodes])

def block_type_code_to_htmlnode(block_text):
    text_nodes = text_to_textnodes(block_text)
    return ParentNode("pre", [ParentNode("code", [text_node_to_html_node(text_node) for text_node in text_nodes])])

def block_type_quote_to_htmlnode(block_text):
    text_nodes = text_to_textnodes(block_text)
    return ParentNode(f"blockquote", [text_node_to_html_node(text_node) for text_node in text_nodes])

def block_type_unordered_list_to_htmlnode(block_text):
    items = block_text.split('\n')
    item_texts = [" ".join(item.split(' ')[1:]) for item in items]
    children_nodes = [ ParentNode("li", [text_node_to_html_node(text_node) for text_node in text_to_textnodes(item_text)]) for item_text in item_texts ]
    return ParentNode("ul", children_nodes)

def block_type_ordered_list_to_htmlnode(block_text):
    items = block_text.split('\n')
    item_texts = [" ".join(item.split(' ')[1:]) for item in items]
    children_nodes = [ ParentNode("li", [text_node_to_html_node(text_node) for text_node in text_to_textnodes(item_text)]) for item_text in item_texts ]
    return ParentNode("ol", children_nodes)

test_markdown = \
"""# The Unparalleled Majesty of "The Lord of the Rings"

[Back Home](/)

![LOTR image artistmonkeys](/images/rivendell.png)

> "I cordially dislike allegory in all its manifestations, and always have done so since I grew old and wary enough to detect its presence.
> I much prefer history, true or feigned, with its varied applicability to the thought and experience of readers.
> I think that many confuse 'applicability' with 'allegory'; but the one resides in the freedom of the reader, and the other in the purposed domination of the author."

In the annals of fantasy literature and the broader realm of creative world-building, few sagas can rival the intricate tapestry woven by J.R.R. Tolkien in *The Lord of the Rings*. You can find the [wiki here](https://lotr.fandom.com/wiki/Main_Page).

## Introduction

This series, a cornerstone of what I, in my many years as an **Archmage**, have come to recognize as the pinnacle of imaginative creation, stands unrivaled in its depth, complexity, and the sheer scope of its *legendarium*. As we embark on this exploration, let us delve into the reasons why this monumental work is celebrated as the finest in the world.

## A Rich Tapestry of Lore

One cannot simply discuss *The Lord of the Rings* without acknowledging the bedrock upon which it stands: **The Silmarillion**. This compendium of mythopoeic tales sets the stage for Middle-earth's history, from the creation myth of Eä to the epic sagas of the Elder Days. It is a testament to Tolkien's unparalleled skill as a linguist and myth-maker, crafting:

1. An elaborate pantheon of deities (the `Valar` and `Maiar`)
2. The tragic saga of the Noldor Elves
3. The rise and fall of great kingdoms such as Gondolin and Númenor

```
print("Lord")
print("of")
print("the")
print("Rings")
```

## The Art of **World-Building**

### Crafting Middle-earth
Tolkien's Middle-earth is a realm of breathtaking diversity and realism, brought to life by his meticulous attention to detail. This world is characterized by:

- **Diverse Cultures and Languages**: Each race, from the noble Elves to the sturdy Dwarves, is endowed with its own rich history, customs, and language. Tolkien, leveraging his expertise in philology, constructed languages such as Quenya and Sindarin, each with its own grammar and lexicon.
- **Geographical Realism**: The landscape of Middle-earth, from the Shire's pastoral hills to the shadowy depths of Mordor, is depicted with such vividness that it feels as tangible as our own world.
- **Historical Depth**: The legendarium is imbued with a sense of history, with ruins, artifacts, and lore that hint at bygone eras, giving the world a lived-in, authentic feel.

## Themes of *Timeless* Relevance

### The *Struggle* of Good vs. Evil

At its heart, *The Lord of the Rings* is a timeless narrative of the perennial struggle between light and darkness, a theme that resonates deeply with the human experience. The saga explores:

- The resilience of the human (and hobbit) spirit in the face of overwhelming odds
- The corrupting influence of power, epitomized by the One Ring
- The importance of friendship, loyalty, and sacrifice

These universal themes lend the series a profound philosophical depth, making it a beacon of wisdom and insight for generations of readers.

## A Legacy **Unmatched**

### The Influence on Modern Fantasy

The shadow that *The Lord of the Rings* casts over the fantasy genre is both vast and deep, having inspired countless authors, artists, and filmmakers. Its legacy is evident in:

- The archetypal "hero's journey" that has become a staple of fantasy narratives
- The trope of the "fellowship," a diverse group banding together to face a common foe
- The concept of a richly detailed fantasy world, which has become a benchmark for the genre

## Conclusion

As we stand at the threshold of this mystical realm, it is clear that *The Lord of the Rings* is not merely a series but a gateway to a world that continues to enchant and inspire. It is a beacon of imagination, a wellspring of wisdom, and a testament to the power of myth. In the grand tapestry of fantasy literature, Tolkien's masterpiece is the gleaming jewel in the crown, unmatched in its majesty and enduring in its legacy. As an Archmage who has traversed the myriad realms of magic and lore, I declare with utmost conviction: *The Lord of the Rings* reigns supreme as the greatest legendarium our world has ever known.

Splendid! Then we have an accord: in the realm of fantasy and beyond, Tolkien's creation is unparalleled, a treasure trove of wisdom, wonder, and the indomitable spirit of adventure that dwells within us all."""

markdown_to_html_node(test_markdown)

