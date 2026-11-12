// Copies the pipeline output (../data) into public/data so pages can fetch it in the browser.
import { cpSync, existsSync, rmSync } from "node:fs";
const src = new URL("../../data", import.meta.url);
const dst = new URL("../public/data", import.meta.url);
if (!existsSync(src)) throw new Error("../data not found: run the pipeline first");
rmSync(dst, { recursive: true, force: true });
cpSync(src, dst, { recursive: true });
console.log("copied data -> public/data");
