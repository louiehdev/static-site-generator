from enum import Enum


class BlockType(Enum):
    PARAGRAPH = 1
    HEADING = 2
    CODE = 3
    QUOTE = 4
    UNORDERED_LIST = 5
    ORDERED_LIST = 6


def markdown_to_blocks(markdown):
    blocks = []
    split_blocks = markdown.split("\n\n")
    for block in split_blocks:
        if block:
            blocks.append(block.strip())
    return blocks

def block_to_blocktype(markdown):
    if is_heading_block(markdown):
        return BlockType.HEADING
    elif is_code_block(markdown):
        return BlockType.CODE
    elif is_quote_block(markdown):
        return BlockType.QUOTE
    elif is_unordered_list_block(markdown):
        return BlockType.UNORDERED_LIST
    elif is_ordered_list_block(markdown):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def is_heading_block(markdown):
    if markdown.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return True
    return False

def is_code_block(markdown):
    if markdown.startswith("```") and markdown.endswith("```"):
        return True
    return False

def is_quote_block(markdown):
    for split in markdown.splitlines():
        if not split.startswith(">"):
            return False
    return True

def is_unordered_list_block(markdown):
    for split in markdown.splitlines():
        if not split.startswith("- "):
            return False
    return True

def is_ordered_list_block(markdown):
    split_lines = markdown.splitlines()
    for i in range(len(split_lines)):
        if not split_lines[i].startswith(f"{i + 1}. "):
            return False
    return True

def get_header_number(text):
    counter = 0
    for i in range(5):
        if text[i] == "#":
            counter += 1
    return counter