import type { Metadata } from 'next';
import './globals.css';
export const metadata:Metadata={title:'馬蓋先 · MacGyver Engineering Academy',description:'從一個工序，理解世界級工程。工程課程、師徒組合工作台、個人進度與技術來源。',icons:{icon:'/academy/assets/icon.svg'}};
export default function RootLayout({children}:{children:React.ReactNode}){return <html lang="zh-Hant"><body>{children}</body></html>}
