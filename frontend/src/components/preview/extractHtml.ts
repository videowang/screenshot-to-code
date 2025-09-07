// Robust function to extract HTML content, supporting attributes like <html lang='en'>
export function extractHtml(code: string): string {
  // Use regex to find the last complete HTML block with attributes support
  const htmlRegex = /<html[^>]*>[\s\S]*?<\/html>/gi;
  const matches = code.match(htmlRegex);
  
  if (matches && matches.length > 0) {
    // Return the last complete HTML block
    return matches[matches.length - 1];
  }
  
  // Fallback: try to find incomplete HTML block (without closing tag)
  const incompleteHtmlRegex = /<html[^>]*>[\s\S]*$/i;
  const incompleteMatch = code.match(incompleteHtmlRegex);
  
  if (incompleteMatch) {
    return incompleteMatch[0];
  }
  
  return "";
}
