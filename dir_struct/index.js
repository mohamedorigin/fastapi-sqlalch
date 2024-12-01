import fs from 'fs-extra';
import path from 'path';
import { parseStructure } from './utils/parser.js';
import { createDirectory, createFile } from './utils/fileSystem.js';

async function buildDirectoryStructure(structureFile, outputPath = '.') {
  try {
    // Verify structure file exists
    if (!fs.existsSync(structureFile)) {
      throw new Error(`Structure file '${structureFile}' not found`);
    }

    // Read structure from file
    const structureContent = fs.readFileSync(structureFile, 'utf8');
    
    // Parse the structure
    const { baseDir, items } = parseStructure(structureContent);
    
    // Create base directory in the specified output path
    const basePath = path.join(outputPath, baseDir);
    
    // Remove existing directory if it exists
    if (fs.existsSync(basePath)) {
      await fs.remove(basePath);
    }
    
    // Create base directory
    await createDirectory(basePath);
    
    // Sort items to ensure directories are created before files
    const sortedItems = [...items].sort((a, b) => {
      if (!a.isFile && b.isFile) return -1;
      if (a.isFile && !b.isFile) return 1;
      return 0;
    });
    
    // Process all items in order
    for (const item of sortedItems) {
      const fullPath = path.join(outputPath, item.fullPath);
      if (item.isFile) {
        await createFile(fullPath);
      } else {
        await createDirectory(fullPath);
      }
    }
    
    console.log(`Directory structure created successfully in ${outputPath}/${baseDir}!`);
  } catch (error) {
    console.error('Error creating directory structure:', error);
    process.exit(1);
  }
}

// Get output path from command line arguments, default to current directory
const outputPath = process.argv[2] || '.';

// Execute the builder with the structure file and output path
buildDirectoryStructure('structure.txt', outputPath).catch(error => {
  console.error('Failed to build directory structure:', error);
  process.exit(1);
});