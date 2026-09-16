import { Html, Head, Main, NextScript } from 'next/document'

// Run before the body is parsed, so every exported route paints in the saved palette.
const restorePalette = `(function(){var p='sage';try{var s=localStorage.getItem('kent-blog-palette');if(['sage','sand','sky','lavender','dark'].indexOf(s)!==-1)p=s;}catch(e){}var d=document.documentElement,t=p==='dark'?'dark':'light';d.dataset.palette=p;d.classList.remove('light','dark');d.classList.add(t);d.style.colorScheme=t;try{localStorage.setItem('theme',t);}catch(e){}})();`

export default function Document() {
  return (
    <Html lang="zh-CN">
      <Head>
        <script id="restore-blog-palette" dangerouslySetInnerHTML={{ __html: restorePalette }} />
      </Head>
      <body>
        <Main />
        <NextScript />
      </body>
    </Html>
  )
}