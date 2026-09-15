import PalettePicker from '../components/palette-picker'
import '../palette.css'

export default function App({ Component, pageProps }) {
  return (
    <>
      <Component {...pageProps} />
      <PalettePicker />
    </>
  )
}
