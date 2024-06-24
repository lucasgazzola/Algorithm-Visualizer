import { Link } from 'react-router-dom'
import BackArrow from '../components/BackArrow'

type AlgorithmLayoutProps = {
  children: React.ReactNode
  name: string
}

export default function AlgorithmLayout({
  children,
  name,
}: AlgorithmLayoutProps) {
  return (
    <main className="h-full flex flex-col py-10">
      <header className="flex items-center gap-20">
        <Link to="/">
          <BackArrow />
        </Link>
        <h1>
          <span className="font-bold text-xl text-cyan-400">Algoritmo:</span>{' '}
          <span className="font-bold text-lg text-cyan-50">{name}</span>
        </h1>
      </header>
      {children}
    </main>
  )
}
