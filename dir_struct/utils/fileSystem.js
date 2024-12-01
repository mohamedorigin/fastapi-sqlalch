import fs from 'fs-extra';
import path from 'path';
import { mkdirp } from 'mkdirp';
import templates from './fileTemplates.js';

async function createDirectory(dirPath) {
  try {
    await mkdirp(dirPath);
  } catch (error) {
    console.error(`Error creating directory ${dirPath}:`, error);
    throw error;
  }
}

async function createFile(filePath) {
  try {
    // Ensure the directory exists first
    const dirPath = path.dirname(filePath);
    await mkdirp(dirPath);
    
    // Get the file name and determine if we have a template
    const fileName = path.basename(filePath);
    const content = templates[fileName] || templates['__init__.py'] || '';
    
    // Write the file with appropriate content
    await fs.writeFile(filePath, content, { encoding: 'utf8', flag: 'w' });
  } catch (error) {
    console.error(`Error creating file ${filePath}:`, error);
    throw error;
  }
}

export { createDirectory, createFile };