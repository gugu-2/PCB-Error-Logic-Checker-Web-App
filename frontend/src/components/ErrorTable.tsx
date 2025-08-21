
import React from 'react'

type Finding = { severity:string; file:string; line:number|null; code:string; message:string; suggestion?:string|null }

export default function ErrorTable({ findings }: { findings: Finding[] }){
  if (!findings.length) return <p style={{opacity:0.7}}>No findings yet.</p>
  return (
    <table style={{ width:'100%', borderCollapse:'collapse' }}>
      <thead>
        <tr>
          <th align="left">Severity</th>
          <th align="left">File</th>
          <th align="left">Code</th>
          <th align="left">Message</th>
          <th align="left">Suggestion</th>
        </tr>
      </thead>
      <tbody>
        {findings.map((f,i)=> (
          <tr key={i} style={{ borderTop:'1px solid #eee' }}>
            <td>{f.severity}</td>
            <td>{f.file}</td>
            <td>{f.code}</td>
            <td>{f.message}</td>
            <td>{f.suggestion}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}
