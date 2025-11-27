import React, {useEffect, useState} from "react";
import api from "../api/axios";

export default function Dashboard(){
  const [counts,setCounts] = useState({patients:0,consultations:0});
  useEffect(()=> {
    const run = async ()=> {
      try {
        const ps = await api.get("/patients");
        const cs = await api.get("/consultations");
        setCounts({ patients: ps.data.length, consultations: cs.data.length });
      } catch (err) {}
    }
    run();
  },[]);
  return (
    <div style={{display:"flex",gap:20}}>
      <div className="card"><h3>Patients</h3><div style={{fontSize:24}}>{counts.patients}</div></div>
      <div className="card"><h3>Consultations</h3><div style={{fontSize:24}}>{counts.consultations}</div></div>
    </div>
  );
}
