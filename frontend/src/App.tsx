
import React, { useState } from 'react'
import FileDrop from './components/FileDrop'
import ErrorTable from './components/ErrorTable'
import { analyze } from './services/api'

export default function App(){
  const [findings, setFindings] = useState<any[]>([])
  const [busy, setBusy] = useState(false)
  const [files, setFiles] = useState<File[]>([])

  async function run(){
    setBusy(true)
    try{
      const res = await analyze(files)
      setFindings(res.findings)
    }catch(e){
      alert((e as Error).message)
    }finally{
      setBusy(false)
    }
  }

  return (
    <div style={{ maxWidth:900, margin:'40px auto', padding:'0 16px', fontFamily:'ui-sans-serif, system-ui' }}>
      <h1>PCB Error & Logic Checker</h1>
      <p style={{opacity:0.8}}>Upload Gerber & netlist files to run basic DRC/ERC checks.</p>
      <FileDrop onFiles={setFiles} />
      <div style={{ display:'flex', gap:12, marginTop:12, alignItems:'center' }}>
        <button onClick={run} disabled={!files.length || busy} style={{ padding:'8px 14px', borderRadius:8, border:'1px solid #ddd' }}>
          {busy ? 'Analyzing…' : 'Analyze'}
        </button>
        <button onClick={()=>{
          const blob = new Blob([JSON.stringify(findings, null, 2)], { type:'application/json' })
          const url = URL.createObjectURL(blob)
          const a = document.createElement('a')
          a.href = url; a.download = 'pcb-findings.json'; a.click()
          URL.revokeObjectURL(url)
        }} disabled={!findings.length} style={{ padding:'8px 14px', borderRadius:8, border:'1px solid #ddd' }}>
          Download JSON
        </button>
        <span style={{opacity:0.7}}>{files.length ? `${files.length} file(s) selected` : 'No files selected'}</span>
      </div>
      <div style={{ marginTop:24 }}>
        <ErrorTable findings={findings} />
      </div>
    </div>
  )
}
