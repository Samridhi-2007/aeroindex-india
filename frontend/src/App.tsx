import React from 'react'

export function App() {
  return (
    <main className="min-h-screen flex items-center justify-center p-8">
      <section className="w-full max-w-3xl rounded-2xl border border-slate-700 bg-slate-900/70 p-8 shadow-xl">
        <h1 className="text-3xl font-bold tracking-tight text-cyan-300">AeroIndex India</h1>
        <p className="mt-3 text-slate-300">
          React + TypeScript + Vite + Tailwind scaffold is ready.
        </p>
        <div className="mt-6 rounded-lg border border-slate-700 bg-slate-800 p-4 text-sm text-slate-300">
          Next: wire frontend routes and connect backend APIs.
        </div>
      </section>
    </main>
  )
}

export default App
