const ENTITIES: Record<string, string> = {
  "&lt;": "<",
  "&gt;": ">",
  "&quot;": '"',
  "&#39;": "'",
  "&#x27;": "'",
  "&amp;": "&",
};

/**
 * Turn a Telegram HTML message into plain text lines.
 * We never put this HTML in the page, so a strange product name cannot run code.
 */
export function htmlToLines(html: string): string[] {
  const text = html
    .replace(/<[^>]*>/g, "")
    .replace(/&(lt|gt|quot|amp|#39|#x27);/g, (entity) => ENTITIES[entity] ?? entity);
  return text
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean);
}
