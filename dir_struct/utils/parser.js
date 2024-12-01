import path from 'path';

function parseStructureLine(line) {
  if (!line.trim()) return null;
  
  // Count the depth based on leading spaces and tree characters
  const depth = Math.floor((line.match(/^[\s│├└]+/)[0].length) / 2);
  
  // Clean the line by removing tree characters and trim
  const cleanPath = line
    .replace(/[│├└─\s]/g, '')
    .trim();
    
  if (!cleanPath) return null;
  
  return {
    path: cleanPath,
    depth,
    isFile: !cleanPath.endsWith('/')
  };
}

function buildFullPath(items, index) {
  const current = items[index];
  const pathParts = [];
  let currentDepth = current.depth;
  let currentPath = current.path.replace(/\/$/, ''); // Remove trailing slash
  pathParts.unshift(currentPath);
  
  // Look backwards through items to build the full path
  for (let i = index - 1; i >= 0; i--) {
    const item = items[i];
    if (item.depth < currentDepth) {
      currentDepth = item.depth;
      currentPath = item.path.replace(/\/$/, '');
      pathParts.unshift(currentPath);
    }
  }
  
  return path.join(...pathParts);
}

function parseStructure(content) {
  const lines = content.split('\n').filter(line => line.trim());
  const baseDir = lines[0].replace(/\/$/, '');
  
  // First pass: get all items with their depth
  const items = lines
    .slice(1)
    .map(line => parseStructureLine(line))
    .filter(item => item !== null);
    
  // Second pass: build full paths
  const processedItems = items.map((item, index) => ({
    ...item,
    fullPath: path.join(baseDir, buildFullPath(items, index))
  }));

  return {
    baseDir,
    items: processedItems
  };
}

export { parseStructure };