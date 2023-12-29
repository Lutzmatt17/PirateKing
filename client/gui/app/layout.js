import { Inter } from 'next/font/google'
import { UsernameProvider } from "@/components/Context/username-context";
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'Dead Man\'s Folly',
  description: 'The best online alternative to Skull King!',
}

export default function RootLayout({ children }) {
  return (
      <html lang="en">
        <body className={inter.className}>
            <UsernameProvider>
              {children}
            </UsernameProvider>
        </body>
      </html>
  )
}
