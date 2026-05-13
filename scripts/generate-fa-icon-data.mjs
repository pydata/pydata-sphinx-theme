/**
 * Generate fa-icon-data.json — a lookup table of all free FA icon SVG data.
 * Used by fontawesome.py at sphinx build time to produce per-build user-icons JS.
 * This file is never sent to the browser.
 *
 * Run: node scripts/generate-fa-icon-data.mjs
 */

import { writeFileSync } from "fs";
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";
import * as solid from "@fortawesome/free-solid-svg-icons";
import * as brands from "@fortawesome/free-brands-svg-icons";

const __dirname = dirname(fileURLToPath(import.meta.url));

function extractIcons(module, prefix) {
  const result = {};
  for (const [key, value] of Object.entries(module)) {
    if (
      value &&
      typeof value === "object" &&
      value.prefix === prefix &&
      value.iconName &&
      Array.isArray(value.icon)
    ) {
      result[value.iconName] = value.icon;
    }
  }
  return result;
}

const data = {
  solid: extractIcons(solid, "fas"),
  brands: extractIcons(brands, "fab"),
};

const outPath = resolve(__dirname, "../src/pydata_sphinx_theme/fa-icon-data.json");
writeFileSync(outPath, JSON.stringify(data));

const solidCount = Object.keys(data.solid).length;
const brandsCount = Object.keys(data.brands).length;
const sizeKB = Math.round(Buffer.byteLength(JSON.stringify(data)) / 1024);
console.log(`fa-icon-data.json: ${solidCount} solid + ${brandsCount} brands icons, ${sizeKB} KB`);
