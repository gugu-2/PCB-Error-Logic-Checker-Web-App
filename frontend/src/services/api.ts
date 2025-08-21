
export async function analyze(files: File[]): Promise<{files:string[]; findings:any[]}> {
  const fd = new FormData()
  files.forEach(f=> fd.append('files', f, f.name))
  const res = await fetch('http://localhost:8000/analyze', { method:'POST', body: fd })
  if (!res.ok) throw new Error('Analysis failed')
  return res.json()
}
