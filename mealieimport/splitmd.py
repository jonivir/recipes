import re
import os
 
def slugify(text):
    """Convert heading text to a valid filename (e.g., "Chapter 1" → "chapter-1")."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)  # Remove special chars
    text = re.sub(r'[\s_-]+', '-', text)  # Replace spaces/hyphens with single hyphen
    return text + ".md"  # Add .md extension
 
def split_markdown_book(input_file, heading_level=1):
    """Split a Markdown book into chapters at the specified heading level."""
    # Regex pattern to match headings (e.g., ^#{1} for H1, ^#{2} for H2)
    heading_pattern = re.compile(rf'^{"#" * heading_level}\s+(.*)$')
    current_chapter = None
    current_file = None
 
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            # Check if the line is a heading of the target level
            match = heading_pattern.match(line)
            if match:
                # Close the previous chapter file (if open)
                if current_file:
                    current_file.close()
                # Extract heading text and create a filename
                heading_text = match.group(1).strip()
                chapter_filename = slugify(heading_text)
                # Avoid overwriting existing files (optional)
                if os.path.exists(chapter_filename):
                    print(f"Warning: {chapter_filename} already exists. Skipping...")
                    current_file = None
                    continue
                # Open a new file for the current chapter
                current_file = open(chapter_filename, 'w', encoding='utf-8')
                print(f"Created: {chapter_filename}")
                # Write the heading to the new chapter file
                current_file.write(line)
            else:
                # Write non-heading lines to the current chapter (if active)
                if current_file:
                    current_file.write(line)
 
    # Close the last chapter file
    if current_file:
        current_file.close()
 
if __name__ == "__main__":
    # Split at H1 headings by default; change heading_level=2 for H2, etc.
    split_markdown_book("recipes.md", heading_level=2)