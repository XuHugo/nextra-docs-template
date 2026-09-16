import { useEffect, useState } from 'react'
import { useTheme } from 'nextra-theme-docs'

const palettes = [
  ['sage', '鼠尾草绿'], ['sand', '暖沙米色'],
  ['sky', '晴空浅蓝'], ['lavender', '柔雾淡紫'], ['dark', '经典深黑']
]
const key = 'kent-blog-palette'
const valid = value => palettes.some(([id]) => id === value)

export default function PalettePicker({ lite = false, className = '' }) {
  const { setTheme } = useTheme()
  const [palette, setPalette] = useState('sage')
  useEffect(() => {
    try {
      const saved = document.documentElement.dataset.palette || localStorage.getItem(key)
      if (valid(saved)) {
        setPalette(saved)
        document.documentElement.dataset.palette = saved
        setTheme(saved === 'dark' ? 'dark' : 'light')
      }
    } catch {}
    function sync(event) {
      if (event.key !== key) return
      const value = valid(event.newValue) ? event.newValue : 'sage'
      setPalette(value)
      document.documentElement.dataset.palette = value
    setTheme(value === 'dark' ? 'dark' : 'light')
    }
    window.addEventListener('storage', sync)
    return () => window.removeEventListener('storage', sync)
  }, [setTheme])
  function change(event) {
    const value = event.target.value
    setPalette(value)
    document.documentElement.dataset.palette = value
    setTheme(value === 'dark' ? 'dark' : 'light')
    try { localStorage.setItem(key, value) } catch {}
  }
  return (
    <label className={`palette-picker ${lite ? 'palette-compact' : ''} ${className}`}>
      <span aria-hidden="true" className="palette-dot" />
      {!lite && <span>配色</span>}
      <select aria-label="博客配色" value={palette} onChange={change}>
        {palettes.map(([id, name]) => <option value={id} key={id}>{name}</option>)}
      </select>
    </label>
  )
}
