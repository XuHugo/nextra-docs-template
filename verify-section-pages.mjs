import { readFileSync } from 'node:fs'

// Fail deployment if either section landing page is missing from the export.
for (const [section, title] of [['tech', '技术笔记'], ['work', '工作札记']]) {
  const html = readFileSync(new URL(`./out/${section}/index.html`, import.meta.url), 'utf8')
  const match = html.match(/<script id="__NEXT_DATA__"[^>]*>([\s\S]*?)<\/script>/)
  if (!html.includes(title) || !match || JSON.parse(match[1]).page !== `/${section}`) {
    throw new Error(`Invalid exported landing page: /${section}/`)
  }
  console.log(`Verified /${section}/ → out/${section}/index.html`)
}
